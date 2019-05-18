from random import seed
from random import shuffle
import os


def get_image_and_label_list_new(params):

    image_path = params['data path']

    class_names = []
    with open(os.path.join(image_path, 'minimal bird list.txt')) as f:
        for line in f:
            class_names.append(line.strip())

    image_list = []
    labels = []

    for idx, directory in enumerate(class_names):

        directory = directory.replace('/', '-')

        files = os.listdir(image_path + directory)
        for f in files:
            image_list.append(image_path + directory + '/' + f)
            labels.append(idx)

    print("Hello from make file and label list")

    return image_list, labels


def get_data(params):
    # Get list of images and labels
    image_list, labels = get_image_and_label_list_new(params)

    # Set up training, evaluation, and test set
    num_imgs = len(image_list)

    ratio_test = 0.1
    ratio_train = 0.7
    ratio_eval = 1 - ratio_test - ratio_train

    num_test = round(ratio_test * num_imgs)
    num_train = round(ratio_train * num_imgs)
    num_eval = round(ratio_eval * num_imgs)

    # Print info
    print('Total number of train images: ' + str(num_train))
    print('Number train iterations per epoch = : ' + str(num_train/params['batch size']))

    seed(1)
    # prepare a sequence
    rand_idx = [i for i in range(num_imgs)]
    shuffle(rand_idx)

    train_idx = rand_idx[0:num_train]
    eval_idx = rand_idx[num_train: num_train + num_eval]
    test_idx = rand_idx[num_train + num_eval: num_imgs]

    data = {}
    data['train_images'] = [image_list[i] for i in train_idx]
    data['train_labels'] = [labels[i] for i in train_idx]

    data['eval_images'] = [image_list[i] for i in eval_idx]
    data['eval_labels'] = [labels[i] for i in eval_idx]

    data['test_images'] = [image_list[i] for i in test_idx]
    data['test_labels'] = [labels[i] for i in test_idx]

    return data
