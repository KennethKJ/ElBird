import tensorflow as tf

print("GPU build with cuda = " + str(tf.test.is_built_with_cuda()))
print("GPU available = " + str(tf.test.is_gpu_available(cuda_only=False,
                         min_cuda_compute_capability=None)))
