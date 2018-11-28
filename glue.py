#!/usr/bin/env python3

import os, signal, socketserver, sys, threading, time

_ids = {}
_lock = threading.Lock()
_wt = None
_ff = 'ffmpeg -i {pipe_in} -vf fps="fps=1/3" {pipe_face_in} -r 30 {pipe_lip_in}'
# NOTE _lp may need to be replaced: 'LipNet/evaluation/predict.py ...'
_lp = 'LipNet/predict {_wt} {pipe_lip_in} | tee {pipe_txt_out} {pipe_voice_in}'
_addr = ('localhost', 2121)
_tmp = '/tmp'
_full_stop = threading.Event() # tell all threads to finish up when set

def handle_connections(weights_path, address=_addr, fd_dir=_tmp):
  _wt = weights_path
  _tmp = fd_dir
  try:
    srv = socketserver.ThreadingTCPServer(address, Handler)
    ip, port = srv.server_address
    srv_thread = threading.Thread(target=srv.serve_forever)
    _full_stop.clear()
    srv_thread.start()
  except:
    stop(srv)
    raise
  else:
    return srv

def stop(srv: socketserver.ThreadingTCPServer):
  srv.shutdown()
  srv.close()

class Handler(socketserver.StreamRequestHandler):
  def setup(self):
    self.pipes = make_fifos(7)

  def handle(self):
    fifos = [get_fifo_name(id) for id in self.pipes]
    # fifos[0]: video_in
    # fifos[1]: face_in
    # fifos[2]: lip_in
    # fifos[3]: text_out
    # fifos[4]: voice_in
    # fifos[5]: face_out
    # fifos[6]: voice_out
    event = threading.Event()
    split_th = threading.Thread(target=mpeg_split, args=tuple(fifos[0:3]))
    lip_th = threading.Thread(target=lip, args=tuple(fifos[2:5]))
    face_th = threading.Thread(target=emotion, args=(event, fifos[1], fifos[5]))
    voice_th = threading.Thread(target=voice, args=tuple(fifos[4:]))
    # TODO connect self.rfile to video_in; text_out, voice_out to self.wfile
    split_th.start()
    lip_th.start()
    face_th.start()
    voice_th.start()
    # TODO read from self.rfile until stream ends
    event.set()
    split_th.join()
    lip_th.join()
    face_th.join()
    voice_th.join()

  def finish(self):
    for id in self.pipes:
      free_fifo(id)

# create a unique named pipe
# returns index in _ids
def make_fifo(path=_tmp):
  id = 0
  with _lock:
    while id in _ids:
      id += 1
    name = os.path.join(path, str(id))
    _ids[id] = name
  os.mkfifo(name)
  return id

# create arbitrarily many named pipes
# returns list of indices in _ids
def make_fifos(count=1, path=_tmp):
  if count == 1:
    return [make_fifo(path)]
  temp = 0
  all = []
  with _lock:
    while count > 0:
      if temp in _ids:
        temp += 1
      else:
        count -= 1
        f = os.path.join(path, str(temp))
        _ids[temp] = f
        os.mkfifo(f)
        all.append(temp)
  return all;

# get file-descriptor-like fifo name from an index
def get_fifo_name(index: int):
  with _lock:
    if index in _ids:
      return _ids[index]
  return None

# deallocate a named pipe
def free_fifo(index: int):
  with _lock:
    if index in _ids:
      os.unlink(_ids[index])
      del _ids[index]
      return True
    return False

# split video from socket to Affectiva and LipNet
# video_in takes streamed mpeg video
# face_in takes images; lip_in takes streamed mpeg video
# terminates after input stream closes
def mpeg_split(video_in, face_in, lip_in):
  with open(video_in,'rb') as pipe_in, open(face_in,'wb') as pipe_face_in, \
       open(lip_in,'wb') as pipe_lip_in:
    os.system(_ff.format(pipe_in, pipe_face_in, pipe_lip_in))

# identify emotions with Affectiva; supply to Polly
# face_in takes images
# face_out takes text
# terminates after done is set
def emotion(done: threading.Event, face_in, face_out):
  t = 0 # milliseconds from start of stream
  loop = True
  with open(face_in,'rb') as pipe_face_in, open(face_out,'w') as pipe_face_out:
    while loop:
      loop = not done.wait(0.5)
      # TODO replace dummy affectiva function with proper invocation
#      emotion = affectiva(pipe_face_in)
#      if emotion:
#        pipe_face_out.write('{} {}\n'.format(t, emotion))
#        t += 3000

# predict words with LipNet; supply text to Polly and socket
# face_in takes streamed mpeg video
# txt_out and voice_in take text
# terminates after input stream is closed
def lip(lip_in, text_out, voice_in):
  with open(lip_in,'rb') as pipe_lip_in, open(txt_out,'w') as pipe_txt_out, \
       open(voice_in,'w') as pipe_voice_in:
    # TODO timestamping?
    os.system(_lp.format(_wt, pipe_lip_in, pipe_txt_out, pipe_voice_in))

# TODO merge words and emotions into SSML, pass to Polly
def voice(voice_in, face_out, voice_out):
  pass



if __name__ == '__main__':
  l = len(sys.argv)
  if l < 2 or l == 3:
    print('Usage: glue.py <weights_path> [ip_address port]')
  else:
    signal.signal(signal.SIGHUP, lambda sig, frame: print('ignoring hangup'))
    w_path = sys.argv[1]
    addr = (sys.argv[2], sys.argv[3]) if l > 2 else ('localhost', 2121)
    srv = handle_connections(w_path, addr)
    while True:
      try:
        time.sleep(3600)
      except KeyboardInterrupt:
        _full_stop.set()
        break
    srv.shutdown()
