#!/usr/bin/env bash

#conda list cudnn
#
#echo "Starting gcloud local training"
#export PYTHONPATH=${PYTHONPATH}:'/media/kennethkj/Data/Google Drive/ML/ElBird/'
#
#gcloud config set project 'electric-birder-71281'
#gcloud config set compute/region 'us-east1-c'
#
#gcloud ai-platform local train \
#    --module-name=train_model.task \
#    --package-path="/media/kennethkj/Data/Google Drive/ML/ElBird/train_model/" \
#    -- \
#    --batch_size=20 \
#    --output_dir="/home/kennethkj/Downloads/"


export PYTHONPATH=${PYTHONPATH}:${PWD}
python -m train_model.task \
  --output_dir="/home/kennethkj/Downloads/" \
  --datapath="/media/kennethkj/Data/Google Drive/ML/Databases/Birds_dB/"