import argparse
from train_model import model

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--datapath',
        help='GCS path to data',
        required=False,
        default='gs://electric-birder-71281-bird-db/Birds_dB/Images/'
    )
    parser.add_argument(
        '--output_dir',
        help='GCS location to write checkpoints and export models',
        required=False,
        default='gs://electric-birder-71281/Estimator_Output/3/'
    )
    parser.add_argument(
        '--batch_size',
        help='Number of examples to compute gradient over.',
        type=int,
        default=10
    )
    parser.add_argument(
        '--job-dir',
        help='this model ignores this field, but it is required by gcloud',
        default='junk'
    )
    parser.add_argument(
        '--num_classes',
        help='Number of classes',  # TODO: This should be auto deduced from train set in future
        nargs='+',
        type=int,
        default=10
    )
    parser.add_argument(
        '--train_steps',
        help='Number of steps to train',
        type=int,
        default=None  # None = indefinately
    )
    parser.add_argument(
        '--eval_steps',
        help='Positive number of steps for which to evaluate model. Default to None, which means to evaluate until input_fn raises an end-of-input exception',
        type=int,
        default=10
    )
    parser.add_argument(
        '--train_csv',
        help='CSV filename/path containing list over images and labels for training',
        default="gs://electric-birder-71281-bird-db/Birds_dB/Mappings/train_set_cloud.csv"
    )
    parser.add_argument(
        '--eval_csv',
        help='CSV filename/path containing list over images and labels for evaluation',
        default="gs://electric-birder-71281-bird-db/Birds_dB/Mappings/eval_set_cloud.csv"
    )
    parser.add_argument(
        '--learning_rate',
        help='Learning rate',
        type=float,
        default=0.0001
    )
    parser.add_argument(
        '--apply_augment',
        help='Use data augmentation?',
        type=bool,
        default=True
    )
    parser.add_argument(
        '--dropout_rate',
        help='Rate of dropout',
        type=float,
        default=0.25
    )
    parser.add_argument(
        '--run_on_cloud',
        help='Switch to indicate if training is done on the cloud or not',
        type=bool,
        default=True
    )
    parser.add_argument(
        '--eval_throttle_secs',
        help='Switch to indicate if training is done on the cloud or not',
        type=int,
        default=600
    )

    ## parse all arguments
    args = parser.parse_args()
    arguments = args.__dict__

    # unused args provided by service
    arguments.pop('job_dir', None)
    arguments.pop('job-dir', None)

    import json
    import os

    # Append trial_id to path if we are doing hptuning
    # This code can be removed if you are not using hyperparameter tuning
    # output_dir = os.path.join(
    #     output_dir,
    #     json.loads(
    #         os.environ.get('TF_CONFIG', '{}')
    #     ).get('task', {}).get('trial', '')
    # )

    # Throw properties into params dict to pass to other functions
    params = {}
    params['train csv'] = arguments.pop('train_csv')
    params['eval csv'] = arguments.pop('eval_csv')
    params['output path'] = arguments.pop('output_dir')
    params['data path'] = arguments.pop('datapath')
    params['image size'] = [244, 224]
    params["batch size"] = arguments.pop('batch_size')
    params['use random flip'] = True
    params['learning rate'] = arguments.pop('learning_rate')
    params['dropout rate'] = arguments.pop('dropout_rate')
    params['num classes'] = arguments.pop('num_classes')
    params['train steps'] = arguments.pop('train_steps')
    params['eval steps'] = arguments.pop('eval_steps')
    params['eval_throttle_secs'] = arguments.pop('eval_throttle_secs')
    params['isRunOnCloud'] = arguments.pop('run_on_cloud')
    params['num parallel calls'] = 4

    print("Hi, this is task.py talking")
    print("Will train for {} steps using batch_size={}".format(params['train steps'], params['batch size']))
    print("PARAMETER SETTINGS:")
    for key, value in params.items():
        print(key + ": " + str(value))

    # Run the training job

    model.go_train(params)
