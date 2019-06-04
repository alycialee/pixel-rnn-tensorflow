import pandas as pd
import glob
import matplotlib.pyplot as plt
import numpy as np
import csv

path = 'errors'
all_files = glob.glob(path + "/*.csv")

errors = []

for filename in all_files:
    data = csv.reader(open(filename, 'r'), delimiter=",")
    train_l, test_l = [], []

    for row in data:
        if len(row) == 2:
            train_l.append(float(row[0]))
            test_l.append(float(row[1]))

    if(len(train_l) != len(test_l)):
        print("error: train loss and test loss diff number of epochs")
    print(filename)

    x = np.array([i for i in range(len(train_l))])
    _ = plt.plot(x, train_l)
    _ = plt.plot(x, test_l)

_ = plt.xlabel("Epochs")
_ = plt.ylabel("Error (Cross Entropy)")
_ = plt.title("PixelRNN: Swapout vs Resnet vs None")
_ = plt.legend(['Train Loss - None', 'Test Loss - None', 'Train Loss - Resnet', 
    'Test Loss - Resnet', 'Train Loss - Swapout', 'Test Loss - Swapout'], loc='upper right')
# _ = plt.savefig("pixelrnn_30epochs_errs1")
_ = plt.show()


