import os
import logging
logging.basicConfig(format="[%(asctime)s] %(message)s", datefmt="%m-%d %H:%M:%S")

import numpy as np
from tqdm import trange
import tensorflow as tf

from utils import *
from network import Network
from statistic import Statistic
import csv

flags = tf.app.flags

# Important flags
# Eric - if use_swapout=True, will overwrite use_residual=True. Cannot use both. 
flags.DEFINE_boolean("use_swapout", True, "using swapout") 
flags.DEFINE_string("model", "pixel_cnn", "name of model [pixel_rnn, pixel_cnn]")
flags.DEFINE_integer("max_epoch", 30, "# of step in an epoch")

# Eric - swapout flags
flags.DEFINE_float("p1", 0.8, "probability 1?")
flags.DEFINE_float("p2", 0.2, "probability 2?")

# network
flags.DEFINE_integer("batch_size", 100, "size of a batch")
flags.DEFINE_integer("hidden_dims", 16, "dimesion of hidden states of LSTM or Conv layers")
flags.DEFINE_integer("recurrent_length", 7, "the length of LSTM or Conv layers")
flags.DEFINE_integer("out_hidden_dims", 32, "dimesion of hidden states of output Conv layers")
flags.DEFINE_integer("out_recurrent_length", 2, "the length of output Conv layers")
flags.DEFINE_boolean("use_residual", False, "whether to use residual connections or not")
# flags.DEFINE_boolean("use_dynamic_rnn", False, "whether to use dynamic_rnn or not")

# training
flags.DEFINE_integer("test_step", 100, "# of step to test a model")
flags.DEFINE_integer("save_step", 1000, "# of step to save a model")
flags.DEFINE_float("learning_rate", 1e-3, "learning rate")
flags.DEFINE_float("grad_clip", 1, "value of gradient to be used for clipping")
flags.DEFINE_boolean("use_gpu", True, "whether to use gpu for training")

# data
flags.DEFINE_string("data", "mnist", "name of dataset [mnist, cifar]")
flags.DEFINE_string("data_dir", "data", "name of data directory")
flags.DEFINE_string("sample_dir", "samples", "name of sample directory")

# Debug
flags.DEFINE_boolean("is_train", True, "training or testing")
flags.DEFINE_boolean("display", False, "whether to display the training results or not")
flags.DEFINE_string("log_level", "INFO", "log level [DEBUG, INFO, WARNING, ERROR, CRITICAL]")
flags.DEFINE_integer("random_seed", 123, "random seed for python")

conf = flags.FLAGS

# logging
logger = logging.getLogger()
logger.setLevel(conf.log_level)

# random seed
tf.set_random_seed(conf.random_seed)
np.random.seed(conf.random_seed)

def main(_):
  model_dir = "model"

  DATA_DIR = os.path.join(conf.data_dir, conf.data)
  # SAMPLE_DIR = os.path.join(conf.sample_dir, conf.data, model_dir)
  SAMPLE_DIR = "sample"

  check_and_create_dir(DATA_DIR)
  check_and_create_dir(SAMPLE_DIR)

  # 0. prepare datasets
  if conf.data == "mnist":
    from tensorflow.examples.tutorials.mnist import input_data
    mnist = input_data.read_data_sets(DATA_DIR, one_hot=True)

    next_train_batch = lambda x: mnist.train.next_batch(x)[0]
    next_test_batch = lambda x: mnist.test.next_batch(x)[0]

    height, width, channel = 28, 28, 1

    train_step_per_epoch = int(mnist.train.num_examples / conf.batch_size)
    test_step_per_epoch = int(mnist.test.num_examples / conf.batch_size)
  elif conf.data == "cifar":
    from cifar10 import IMAGE_SIZE, inputs

    maybe_download_and_extract(DATA_DIR)
    images, labels = inputs(eval_data=False,
        data_dir=os.path.join(DATA_DIR, 'cifar-10-batches-bin'), batch_size=conf.batch_size)

    height, width, channel = IMAGE_SIZE, IMAGE_SIZE, 3


  with tf.Session() as sess:
    network = Network(sess, conf, height, width, channel)

    stat = Statistic(sess, conf.data, model_dir, tf.trainable_variables(), conf.test_step)
    stat.load_model()

    if conf.is_train:
      logger.info("Training starts!")

      initial_step = stat.get_t() if stat else 0
      iterator = trange(conf.max_epoch, ncols=70, initial=initial_step)
      
      # Eric - define the filename where we store errors
      err_filename = 'error_file_{}.csv'.format(get_timestamp())

      # Eric - writes params to first two lines of file
      with open(err_filename, 'a') as errorFile:
        errorWriter = csv.writer(errorFile, delimiter =',')
        errorWriter.writerow(['model', 'max_epoch', 'use_swapout', 
          'use_residual', 'swapout_p1', 'swapout_p2'])
        errorWriter.writerow([conf.model, conf.max_epoch, conf.use_swapout, 
          conf.use_residual, conf.p1, conf.p2])
      errorFile.close()

      for epoch in iterator:
        # 1. train
        total_train_costs = []

        for idx in range(train_step_per_epoch):
          # Eric - print progress within an epoch
          # print("train step percent in this epoch:", (idx / train_step_per_epoch))
          images = binarize(next_train_batch(conf.batch_size)) \
            .reshape([conf.batch_size, height, width, channel])

          cost = network.test(images, with_update=True)
          total_train_costs.append(cost)

        # 2. test
        total_test_costs = []
        for idx in range(test_step_per_epoch):
          images = binarize(next_test_batch(conf.batch_size)) \
            .reshape([conf.batch_size, height, width, channel])

          cost = network.test(images, with_update=False)
          total_test_costs.append(cost)

        avg_train_cost, avg_test_cost = np.mean(total_train_costs), np.mean(total_test_costs)

        # Eric - print stats for each iteration
        print("Epoch: {}, train l: {}, test l: {}".format(epoch, avg_train_cost, avg_test_cost))

        # Eric - saves model. saves errors in err_filename w/ form (train l, test l)
        stat.on_step(avg_train_cost, avg_test_cost, err_filename)

      # Eric - originally this block below was in the for loop. moved out. 
      # 3. generate samples
      samples = network.generate()
      save_images(samples, height, width, 10, 10,
          directory=SAMPLE_DIR, prefix="epoch_{}".format(epoch))

      print("Sample generation of this epoch done")
    else:
      logger.info("Image generation starts!")

      samples = network.generate()
      save_images(samples, height, width, 10, 10, directory=SAMPLE_DIR)


if __name__ == "__main__":
  tf.app.run()
