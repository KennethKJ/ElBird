
import os
import numpy as np
# Define paths
dB_path = "D:/ML/Databases/Birds_dB/Images/"
# bucket_path = "/electric-birder-71281-bird-db/Birds_dB/Images/"
bucket_path = "/content/drive/My Drive/ML/Databases/Birds_dB/Images/"
# Files

file_list = []
label_list = []

filename_classes = "D:/ML/Databases/Birds_dB/Mappings/minimal_bird_list.txt"
LIST_OF_CLASSES = [line.strip() for line in open(filename_classes, 'r')]


f = open('D:/ML/Databases/Birds_dB/Mappings/classes_colab.txt', 'w')

num_classes = 0
for i in range(len(LIST_OF_CLASSES)):
    f.write(LIST_OF_CLASSES[i] + "\n")

    num_classes += 1
    img_path = dB_path + LIST_OF_CLASSES[i] + "/"
    with os.scandir(img_path) as files:
        for file in files:
            line = bucket_path + LIST_OF_CLASSES[i] + "/" + file.name
            file_list.append(line)
            label_list.append(str(i))
f.close()

print("Total classes = " + str(num_classes))
total_images = len(file_list)
idx = np.random.permutation(total_images)

train_proportion = 0.70
eval_proprotion = 0.2
test_proportion = 1 - train_proportion - eval_proprotion

idx_train = idx[0: int(total_images*train_proportion)]
idx_eval = idx[int(total_images*train_proportion): int(total_images*(train_proportion+eval_proprotion))]
idx_test = idx[int(total_images*(train_proportion+eval_proprotion)): total_images-1]

idxs = [idx_train, idx_eval, idx_test]
tot = len(idx_eval) + len(idx_test) + len(idx_train)

names = ['train', 'eval', 'test']

for j in range(3):

    f = open(names[j] + '_set_colab.csv', 'w')
    for i in idxs[j]:
        line = file_list[i] + "," + label_list[i] + "\n"
        print(line)
        f.write(line)  # Give your csv text here.
    f.close()





print("The End")
