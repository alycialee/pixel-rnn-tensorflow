import pandas as pd
import glob
import matplotlib.pyplot as plt
import numpy as np

path = 'errors'
all_files = glob.glob(path + "/*.csv")

errors = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=None)
    errors.append(df)

frame = pd.concat(errors, axis=0, ignore_index=True)
x = list(range(len(frame.iloc[:,0])))
for data in frame.iloc[:,0]:
    print(data)
    plt.plot(x, data, color='olive')
for data in frame.iloc[1::2, :]:
    plt.plot(x, data, color='skyblue')
