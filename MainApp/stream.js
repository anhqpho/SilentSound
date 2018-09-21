const constraints = {
    audio: true,
    video: {width: {min: 1280}, height: {min: 720}}
};

function beginStream() {
    navigator.mediaDevices.getUserMedia(constraints).then(stream => {
        var video = document.querySelector('video');
        video.src = window.URL.createObjectURL(stream)
        video.onloadedmetadata = (e) => {
            
        }
    });
}
