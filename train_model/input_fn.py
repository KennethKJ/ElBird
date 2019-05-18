import tensorflow as tf
from keras.applications.vgg16 import preprocess_input
# from matplotlib import pyplot as plt

tf.logging.set_verbosity(v=tf.logging.INFO)

HEIGHT = 224
WIDTH = 224
NUM_CHANNELS = 3
NCLASSES = 123


def read_and_preprocess_with_augment(image_bytes, label=None):
    return read_and_preprocess(image_bytes, label, augment=True)


def read_and_preprocess(image_bytes, label=None, augment=False):
    # Decode the image, end up with pixel values that are in the -1, 1 range
    image = tf.image.decode_jpeg(contents=image_bytes, channels=NUM_CHANNELS)
    image = tf.image.convert_image_dtype(image=image, dtype=tf.float32)  # 0-1
    image = tf.expand_dims(input=image, axis=0)  # resize_bilinear needs batches

    if augment:
        image = tf.image.resize_bilinear(images=image, size=[HEIGHT + 10, WIDTH + 10], align_corners=False)
        image = tf.squeeze(input=image, axis=0)  # remove batch dimension
        image = tf.random_crop(value=image, size=[HEIGHT, WIDTH, NUM_CHANNELS])
        image = tf.image.random_flip_left_right(image=image)
        image = tf.image.random_brightness(image=image, max_delta=63.0 / 255.0)
        image = tf.image.random_contrast(image=image, lower=0.2, upper=1.8)
    else:
        image = tf.image.resize_bilinear(images=image, size=[HEIGHT, WIDTH], align_corners=False)
        image = tf.squeeze(input=image, axis=0)  # remove batch dimension

    # Pixel values are in range [0,1], convert to [-1,1]
    # image = tf.subtract(x=image, y=0.5)
    # image = tf.multiply(x=image, y=2.0)

    image = tf.cast(tf.round(image * 255), tf.int32)
    image = preprocess_input(image)

    label = tf.one_hot(tf.strings.to_number(label, out_type=tf.int32), depth=10)

    return {"input_1": image}, label


# def convert_labels(labels):
#
#     table_init = tf.tables_initializer()
#
#     filename_classes = "D:/ML/Databases/Birds_dB/Mappings/classes.txt"
#     LIST_OF_LABELS = [line.strip() for line in open(filename_classes, 'r')]
#
#     labels_table = tf.contrib.lookup.index_table_from_tensor(
#         mapping=tf.constant(value=LIST_OF_LABELS, dtype=tf.string))
#
#     labels = labels_table.lookup(labels)
#     labels = tf.one_hot(indices=labels, depth=NCLASSES)
#
#     return labels


def make_input_fn(csv_of_filenames, mode, params, augment=False):
    def _input_fn():
        def decode_csv(csv_row):
            filename, label = tf.decode_csv(records=csv_row, record_defaults=[[""], [""]])
            image_bytes = tf.read_file(filename=filename)
            return image_bytes, label

        # Create tf.data.dataset from filename
        dataset = tf.data.TextLineDataset(filenames=csv_of_filenames).map(map_func=decode_csv, num_parallel_calls=params['num parallel calls'])

        if augment:
            dataset = dataset.map(map_func=read_and_preprocess_with_augment, num_parallel_calls=params['num parallel calls'])
        else:
            dataset = dataset.map(map_func=read_and_preprocess, num_parallel_calls=params['num parallel calls'])

        if mode == tf.estimator.ModeKeys.TRAIN:
            num_epochs = None  # indefinitely
            dataset = dataset.shuffle(buffer_size = 2* params["batch size"])
        else:
            num_epochs = 1  # end-of-input after this

        dataset = dataset.repeat(count=num_epochs).batch(batch_size=params["batch size"]).prefetch(2)
        images, labels = dataset.make_one_shot_iterator().get_next()

        return images, labels
    return _input_fn


test = False

params = {};
params['batch size'] = 10

if test:
    a1 = make_input_fn("train_set_local.csv",  tf.estimator.ModeKeys.TRAIN, params, augment=False)
    b, c = a1()


    filename = "D:/ML/Databases/Birds_dB/Mappings/classes.txt"
    LIST_OF_LABELS = [line.strip() for line in open(filename, 'r')]

    labels_table_2 = tf.contrib.lookup.index_table_from_tensor(
        mapping=tf.constant(value=LIST_OF_LABELS, dtype=tf.string))

    with tf.Session() as sess:
        tf.tables_initializer().run()

        while 1 == 1:

            imgs, labls = sess.run(a1())

            labels = labels_table_2.lookup(keys=tf.constant(labls))
            l = tf.one_hot(indices=labels, depth=NCLASSES)
            l2 = l.eval()

            for i in range(10):
                plt.imshow(imgs['input_1'][i, :, :, :])
                plt.title(labls[i])
                plt.show(block=False)
                print("Done")

        print("Done")
