import tensorflow as tf

model_dir = "C:/EstimatorOutput/3/"
sess = tf.Session()
# train your model
saver = tf.train.Saver()
saver.save(sess, model_dir + 'model.ckpt')