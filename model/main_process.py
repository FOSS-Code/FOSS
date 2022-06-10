import os.path
import pickle
import shutil

from FOSS import *
import pandas as pd

if os.path.exists('./monte_carlo_tmp_data'):
    shutil.rmtree('./monte_carlo_tmp_data')
os.makedirs('./monte_carlo_tmp_data')

# feature num
attr = 12

# read data
dataset = np.zeros((16, 10000, attr))
for i in range(16):
    dataset[i] = np.loadtxt('data-2/mat' + str(i) + '.txt', delimiter=' ')

# parameters
train_num = 9
newclass_num = 7
num_per_class = 200
ind = [0, 15, 7, 10, 8, 5, 6, 11, 9, 12, 3, 2, 14, 4, 1, 13]
# allIndex = np.random.permutation(train_num+newclass_num);
allIndex = np.array(ind)
data = np.zeros((num_per_class * train_num, attr))
label = np.zeros((num_per_class * train_num, 1))

# shuffle samples within the class 
for i in range(dataset.shape[0]):
    dataindex = np.random.permutation(dataset.shape[1])
    datatemp = dataset[i, dataindex, :]
    dataset[i] = datatemp

# shuffle samples between the class 
for pos in range(train_num):
    i = allIndex[pos]
    data[pos * num_per_class:(pos + 1) * num_per_class, :] = dataset[i, 0:num_per_class, :]
    label[pos * num_per_class:(pos + 1) * num_per_class] = i  # *np.ones((num_per_class,1));

test_per_class = 80
streamdata = np.zeros((test_per_class * (train_num + newclass_num), attr))
streamlabel = np.zeros((test_per_class * (train_num + newclass_num), 1))

# dataset
for pos in range(train_num + newclass_num):
    i = allIndex[pos]
    streamdata[pos * test_per_class:(pos + 1) * test_per_class, :] = \
        dataset[i, num_per_class:num_per_class + test_per_class, :]
    if pos < train_num:
        streamlabel[pos * test_per_class:(pos + 1) * test_per_class] = i  # *np.ones((test_per_class,1));
    else:
        streamlabel[pos * test_per_class:(pos + 1) * test_per_class] = 999

numTree = 30
numSub = 100
attrNum = data.shape[1]
model = FOSS(data, label, numTree, numSub, attrNum)

# buffer
params = {'alpha': 1, 'buffersize': 1000, 'subbuffer': 500, 'eps': 5, 'minpts': 5}
result, model = Testingpro(streamdata, streamlabel, model, params)
pd.DataFrame(result).to_csv('result.csv')
newevaluation = []
for i in range(result.shape[0]):
    newevaluation.append(np.sum(result[0:(i + 1), 0] == result[0:(i + 1), 1]) / (i + 1))