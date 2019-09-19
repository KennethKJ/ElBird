import argparse
from train_model import model
from tensorflow.python.estimator.export import export as ex
import tensorflow as tf
from train_model.model import create_estimator
from train_model.input_fn import get_image
from tensorflow.contrib import predictor
import numpy as np
import os
from matplotlib import pyplot as plt
from PIL import Image

if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     '--datapath',
    #     help='GCS path to data',
    #     required=False,
    #     default='gs://electric-birder-71281-bird-db/Birds_dB/Images/'
    # )
    # parser.add_argument(
    #     '--output_dir',
    #     help='GCS location to write checkpoints and export models',
    #     required=False,
    #     default='gs://electric-birder-71281/Estimator_Output/3/'
    # )
    # parser.add_argument(
    #     '--batch_size',
    #     help='Number of examples to compute gradient over.',
    #     type=int,
    #     default=10
    # )
    # parser.add_argument(
    #     '--job-dir',
    #     help='this model ignores this field, but it is required by gcloud',
    #     default='junk'
    # )
    # parser.add_argument(
    #     '--num_classes',
    #     help='Number of classes',  # TODO: This should be auto deduced from train set in future
    #     nargs='+',
    #     type=int,
    #     default=10
    # )
    # parser.add_argument(
    #     '--train_steps',
    #     help='Number of steps to train',
    #     type=int,
    #     default=None  # None = indefinately
    # )
    # parser.add_argument(
    #     '--eval_steps',
    #     help='Positive number of steps for which to evaluate model. Default to None, which means to evaluate until input_fn raises an end-of-input exception',
    #     type=int,
    #     default=10
    # )
    # parser.add_argument(
    #     '--train_csv',
    #     help='CSV filename/path containing list over images and labels for training',
    #     default="gs://electric-birder-71281-bird-db/Birds_dB/Mappings/train_set_cloud.csv"
    # )
    # parser.add_argument(
    #     '--eval_csv',
    #     help='CSV filename/path containing list over images and labels for evaluation',
    #     default="gs://electric-birder-71281-bird-db/Birds_dB/Mappings/eval_set_cloud.csv"
    # )
    # parser.add_argument(
    #     '--learning_rate',
    #     help='Learning rate',
    #     type=float,
    #     default=0.0001
    # )
    # parser.add_argument(
    #     '--apply_augment',
    #     help='Use data augmentation?',
    #     type=bool,
    #     default=True
    # )
    # parser.add_argument(
    #     '--dropout_rate',
    #     help='Rate of dropout',
    #     type=float,
    #     default=0.25
    # )
    # parser.add_argument(
    #     '--run_on_cloud',
    #     help='Switch to indicate if training is done on the cloud or not',
    #     type=bool,
    #     default=True
    # )
    # parser.add_argument(
    #     '--eval_throttle_secs',
    #     help='Switch to indicate if training is done on the cloud or not',
    #     type=int,
    #     default=600
    # )
    #
    # ## parse all arguments
    # args = parser.parse_args()
    # arguments = args.__dict__
    #
    # # unused args provided by service
    # arguments.pop('job_dir', None)
    # arguments.pop('job-dir', None)
    #
    # import json
    # import os
    #
    # # Append trial_id to path if we are doing hptuning
    # # This code can be removed if you are not using hyperparameter tuning
    # # output_dir = os.path.join(
    # #     output_dir,
    # #     json.loads(
    # #         os.environ.get('TF_CONFIG', '{}')
    # #     ).get('task', {}).get('trial', '')
    # # )
    model_num = 13
    # Throw properties into params dict to pass to other functions
    params = {}
    params['train csv'] = "C:/Users/alert/Google Drive/ML/ElBird/Data_proc/train_set_local.csv"
    params['eval csv'] = "C:/Users/alert/Google Drive/ML/ElBird/Data_proc/eval_set_local.csv"
    params['output path'] = "C:/EstimatorOutput/" + str(model_num) + "/"
    params['data path'] = "C:/Users/alert/Google Drive/ML/Databases/Birds_dB/Images"
    params['image size'] = [244, 224]
    params["batch size"] = 16*2
    params['use random flip'] = True
    params['learning rate'] = 0.000001  # 0.000000000002 #
    params['dropout rate'] = 0.50
    params['num classes'] = 123
    params['train steps'] = 65000
    params['eval steps'] = 20
    params['eval_throttle_secs'] = 600
    params['isRunOnCloud'] = False
    params['num parallel calls'] = 4

    print("Hi, this is task.py talking")
    print("Will train for {} steps using batch_size={}".format(params['train steps'], params['batch size']))
    print("********************************")
    print("PARAMETER SETTINGS:")
    for key, value in params.items():
        print(key + ": " + str(value))
    print("********************************")

    # Run the training job

    model.go_train(params)

    print("Done training!")

    save_model = False

    if save_model:
        feature_spec = {'input_1': tf.placeholder(shape=[None, 224, 224, 3], dtype=tf.int32)}
        serving_input_fn = ex.build_raw_serving_input_receiver_fn(feature_spec)

        Est = create_estimator(params)

        export_dir = "C:/EstimatorOutput/" + str(model_num) + "/saved model/"

        Est.export_savedmodel(export_dir, serving_input_fn)

        print("Model saved")

