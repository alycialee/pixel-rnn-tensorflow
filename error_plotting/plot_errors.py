import pandas as pd
import glob
import matplotlib.pyplot as plt
import numpy as np
import csv

# plots specifically for train_l vs. test_l
# plot_train = true -> plots train error, else plots test error
# remove_first = true -> remove first epoch from plot
def plot(all_files, title, legend, plot_train, remove_first):
    errors = []

    for filename in all_files:
        data = csv.reader(open(filename, 'r'), delimiter=",")
        train_l, test_l = [], []

        # define x and y
        for row in data:
            # csv header size probably > 2. Skip those. hacky. 
            if len(row) == 2:
                train_l.append(float(row[0]))
                test_l.append(float(row[1]))
        x = np.array([i for i in range(len(train_l))])

        # check if train loss and test loss have same dim
        if(len(train_l) != len(test_l)):
            print("error: train/test -> different dimensions")
        print(filename)

        # sets y to train or test
        if(plot_train):
            y = train_l
        else:
            y = test_l

        # possibly removes first epoch
        if(remove_first):
            x = x[1:]
            y = y[1:]

        # plot!
        plt.plot(x, y)


    plt.xlabel("Epochs")
    plt.ylabel("Error (Cross Entropy)")
    plt.title(title)
    plt.legend(legend, loc='upper right')
    # plt.savefig("pixelrnn_30epochs_errs1")
    plt.show()

if __name__ == '__main__':
    path = 'errors'
    all_files = glob.glob(path + "/*.csv")

    cnn_test_title = "PixelCNN Test Error: Swapout with Varying Probabilities"
    cnn_train_title = "PixelCNN Train Error: Swapout with Varying Probabilities"
    cnn_legend = ['p1 = 0.7, p2 = 0.2', 'no swapout', 'p1 = 0.6, p2 = 0.4', 'p1 = 0.3, p2 = 0.8',
        'p1 = 0.4, p2 = 0.9', 'p1 = 1.0, p2 = 1.0', 'p1 = 0.25, p2 = 0.75']

    plot(all_files, cnn_train_title, cnn_legend, True, False)
    plot(all_files, cnn_test_title, cnn_legend, False, False)
    plot(all_files, cnn_train_title, cnn_legend, True, True)
    plot(all_files, cnn_test_title, cnn_legend, False, True)


    # rnn_test_title = "PixelRNN Test Error: Swapout vs Resnet vs None"
    # rnn_train_title = "PixelRNN Train Error: Swapout vs Resnet vs None"
    # rnn_legend = ['None', 'Resnet', 'Swapout']

    # # plots, with first epoch
    # plot(all_files, rnn_train_title, rnn_legend, True, False)
    # plot(all_files, rnn_test_title, rnn_legend, False, False)

    # # plots, without first epoch
    # plot(all_files, rnn_train_title, rnn_legend, True, True)
    # plot(all_files, rnn_test_title, rnn_legend, False, True)

