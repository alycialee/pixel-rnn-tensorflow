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
    column1, column2 = [], []

    for row in data:
        column1.extend(row[0])
        column2.extend(row[1])

    print(column1)
    print(column2)

# frame = pd.concat(errors, axis=0, ignore_index=True)
# x = list(range(len(frame.iloc[:,0])))
# for data in frame.iloc[:,0]:
#     print(data)
#     plt.plot(x, data, color='olive')
# for data in frame.iloc[1::2, :]:
#     plt.plot(x, data, color='skyblue')
