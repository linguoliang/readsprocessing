import tensorflow as tf
x = tf.float32, [None, 784]
w = tf.zeros([784, 10])
b = tf.zeros([10])
y = tf.nn.softmax(tf.matmul(x, w) + b)