import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 
import csv

# filename = open('FRF_ModPhase.txt')
# n = 0
# data = []
# for line in filename.readlines():
#     n+=1
#     if n == 5:
#         data.append(line)
# print(data)

data = pd.read_csv("FRF_ModPhase.txt", delimiter = "\t", names=["freq", "mod", "phase"])
test = np.loadtxt("FRF_ModPhase.txt")[5:, :]

data_array = np.array(data)[1:, :]
for i in range(len(data_array[0])):
    for j in range(len(data_array[:, 0])):
        data_array[j, i] = float(data_array[j, i])
print(data_array)

with open('FRF_ModPhase.txt') as f:
    lines = (float(line) for line in f if not line.startswith('#'))
    FH = np.loadtxt(lines, delimiter=',', skiprows=1)
print(FH)