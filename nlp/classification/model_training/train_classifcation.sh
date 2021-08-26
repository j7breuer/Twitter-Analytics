#!/bin/bash

# Train spacy multilabel classification model on GPU
# Run from the oupt folder
python -m prodigy train ../oupt --textcat-multilabel tweet_identification_filtered --eval-split 0.2 --gpu-id 0
