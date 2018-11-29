# SilentSound
  Project description
  
## Afectiva SDK
This is a sample web app using of Affectiva Java SDK. Some of the codes here are based on Affectiva instructions. I nade some modifications to run it locally. In the future, our team will develop more features and intergrate this module into the main app.

### Instruction

* Use Chrome browser to install and run https://chrome.google.com/webstore/detail/web-server-for-chrome/ofhbbkphhbklhfoeikjpcbhemlocgigb
* In "Choose Folder" button, open your local repo that contains "index.html" file. Check "Automatically show index.html"
* "Stop" then "Start" the switch right under "Choose Folder" button

## LipNet


### Instruction
Having installed dependencies, run the prediction, passing trained model as well as a path to the file you want to evaluate. In my case, I developed the model in a conda environment.

Invocation is performed as follows:
$ ./predict path/to/model.h5 path-to/file.mpg

example:
$ ./predict evaluation/models/unseen-weights178.h5 id2_vcd_swwp2s.mpg

If the dasta is already preprocessed (mouth is cropped and frames extracted):
$ ./predict path/to/model.h5 path/to/folder

example:
$ ./predict evaluation/models/unseen-weights178.h5 evaluation/samples/bbaf2n
