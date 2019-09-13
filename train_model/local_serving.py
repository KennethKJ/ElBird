

from tensorflow.python.estimator.export import export as ex
import tensorflow as tf
from train_model.model import create_estimator
from train_model.input_fn import get_image
from tensorflow.contrib import predictor
import numpy as np
import os
from matplotlib import pyplot as plt
from PIL import Image


# Throw properties into params dict to pass to other functions
params = {}
params['train csv'] = "D:/Google Drive/ML/ElBird/Data_proc/train_set_local.csv"
params['eval csv'] = "D:/Google Drive/ML/ElBird/Data_proc/eval_set_local.csv"
params['output path'] = "C:/EstimatorOutput/4/"
params['data path'] = "D:/Google Drive/ML/Databases/Birds_dB/Images"
params['image size'] = [244, 224]
params["batch size"] = 16
params['use random flip'] = True
params['learning rate'] = 0.000000000002  # 0.00001
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


save_model = False

if save_model:
    feature_spec = {'input_1': tf.placeholder(shape=[None, 224, 224, 3], dtype=tf.int32)}
    serving_input_fn = ex.build_raw_serving_input_receiver_fn(feature_spec)

    Est = create_estimator(params)

    export_dir = "C:/EstimatorOutput/3/saved model/"

    Est.export_savedmodel(export_dir, serving_input_fn)





with tf.Session() as sess:

    # Set up list to convert numerical prediction to actual name
    GD_path = "C:/Users/alert/Google Drive"
    DB_path = "/ML/Databases/Birds_dB/Images/"
    classes = [item for item in os.listdir(GD_path + DB_path)]

    # Define placeholde for filename
    s = tf.placeholder(dtype=tf.string, name='filnim')
    # Get the image given the filename
    a = get_image(s)
    # Expand dim because batch num = 1 and first dim thus collapsed but model wants it
    a = tf.expand_dims(a, 0)

    # Where to get saved model from
    model_dir = "C:/EstimatorOutput/3/saved model/1568150988/"

    # Define prediction function
    predict_fn = predictor.from_saved_model(model_dir)

    # RUN AND HAVE FUN!
    filename = "C:/Users/alert/Google Drive/ML/Databases/Birds_dB/Images/american_crow/Ex1.jpg"

    doBooth = True

    for i in range(100):

        if doBooth:

            dB_loc = "C:/Users/alert/Google Drive/ML/Databases/Photo Booth User Group Photos/(2) Bird Photo Booth Users Group_files/"

            pics = [item for item in os.listdir(dB_loc)]

            f = dB_loc + pics[i]
        else:
            f = "C:/Users/alert/Google Drive/ML/Databases/Birds_dB/Images/" + \
                classes[np.random.randint(0, 122)] + "/Ex" + str(np.random.randint(1, 10)) + ".jpg"

        a_np = sess.run(a, feed_dict={s: f})

        Y = predict_fn({'input_1': a_np})['sm_out']

        pred = np.argmax(Y)

        im = Image.open(f)

        fig, ax = plt.subplots()

        ax.imshow(im)
        plt.title(classes[pred])
        plt.show()
        print(classes[pred])

