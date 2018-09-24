# LipNet: End-to-End Sentence-level Lipreading from: https://github.com/rizkiarm/LipNet
## Installation
To use the model, first you need to clone the repository:
```
git clone https://github.com/anhqpho/SilentSound/LipNet
```
Then you can install the package:
```
cd LipNet/
For Windows:
* Please use Anaconda and install dlib: conda install -c conda-forge dlib
For Linux: 
* pip install --upgrade  dlib
pip install -e .
```
**Note:** if you don't want to use CUDA, you need to edit the ``setup.py`` and change ``tensorflow-gpu`` to ``tensorflow``
