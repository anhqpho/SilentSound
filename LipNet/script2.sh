#!/bin/bash

for i in {21..25}
do
    PYTHONPATH=./ python2 scripts/extract_mouth_batch.py datasets/s$i/ *.mpg . common/predictors/shape_predictor_68_face_landmarks.dat
done
