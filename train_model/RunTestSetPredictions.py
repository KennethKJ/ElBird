
# %%
import tensorflow as tf
import tensorflow.keras.estimator as kes
from train_model import model
from train_model.input_fn import make_input_fn

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

# import gcsfs
import seaborn as sn
import os

params = {}
params['test csv'] = "D:/Google Drive/ML/ElBird/Data_proc/test_set_local.csv"
#     params['train csv'] = arguments.pop('train_csv')
#     params['eval csv'] = arguments.pop('eval_csv')
params['output path'] = "C:/EstimatorOutput/3/"
params['data path'] = "D:/Google Drive/ML/Databases/Birds_dB/Images"
params['image size'] = [244, 224]
params['num parallel calls'] = 4
params["batch size"] = 16
params['use random flip'] = True
params['learning rate'] = 0.001
params['dropout rate'] = 0
params['num classes'] = 123
params['train steps'] = 100
params['eval steps'] = 100
params['eval_throttle_secs'] = 600
params['isRunOnCloud'] = False
params['num parallel calls'] = 4

print("Getting predictions:")

tf.reset_default_graph()
# tf.Graph().as_default()
pred = model.go_predict(params)
print(type(pred))

print("PANDAS:")
df = pd.read_csv(params['test csv'], header=None)
df.head()

print(df.iloc[0, 0])

# print("TF")

# # tf.reset_default_graph()
# # a1 = make_input_fn('gs://electric-birder-71281-bird-db/Birds_dB/Mappings/test_set_cloud.csv',  tf.estimator.ModeKeys.PREDICT, params, augment=False)
# # b, c = a1()

# print("******* Predictions: ************")

GD_path = "D:/Google Drive/"
DB_path = "/ML/Databases/Birds_dB/Images/"

classes = [item for item in os.listdir(GD_path + DB_path)]

# classes = ['American Goldfinch (male)', 'Background', 'Black-capped Chickadee', 'House Sparrow (Female/Juvenile)',
#            'House Sparrow (male)', 'Northern Cardinal (male)', 'Squirrel']

# # with tf.Session() as sess:
print(" HERE:")
count = 0
CM = np.zeros((len(classes), len(classes)), dtype=np.int, order='C')

# for p in pred:

N = 300
Correct = 0
# for i in range(N):
for p in pred:
    #     p = next(pred)
    current_pred = p['sm_out']
    idx = np.argmax(current_pred)
    print("Predicted class: " + classes[idx] + "; True class: " + classes[int(df.iloc[count, 1])])
    CM[np.int(df.iloc[count, 1]), idx] += 1

    if idx == int(df.iloc[count, 1]):
        Correct += 1
    count += 1

print("Total correct (%): " + str(Correct / (count + 1) * 100))
plt.matshow(CM)
plt.show()
# # imgs, labls = b.eval()
# print("LABEL")
# print(labls)
# print("IMAGE")
# print(imgs)
# print("PIC:")
# # plt.imshow(imgs['input_1'])
# #     plt.title(classes[idx])
# #     plt.show()

print("DONE!")

# %%

# df_cm = pd.DataFrame(CM, index=[i for i in classes],
#                      columns=[i for i in classes])
# sn.heatmap(df_cm, annot=True)
# plt.show()

for k in range(12):

    df_cm = pd.DataFrame(CM[k*10:(k+1)*10,k*10:(k+1)*10 ], index=[i for i in classes[k*10:(k+1)*10]],
                         columns=[i for i in classes[k*10:(k+1)*10]])
    sn.heatmap(df_cm, annot=True)
    plt.show()


