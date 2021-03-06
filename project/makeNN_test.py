'''
This is codes for LEARNING
(Make a Neural Network with training data)
(Insert WEIGH into DB)
'''
import sys
sys.path.append('nnet')

import numpy as np
#from NeuralNetworkLearn import nnet.NeuralNetworkLearn
from NeuralNetworkLearn import NeuralNetworkLearn
import pymongo
'''
!!!!!!!!!!!!!!!!!!!!!!!
SUPPOSE ngram data in DB is as follows:

[0,0,0,0,144,144,144,144, ..., 255,0,10,55,1] (last one(1) is identifying data 1:malware, 0:normal)
!!!!!!!!!!!!!!!!!!!!!!
'''



'''
get ngram from DB
'''
connection = pymongo.MongoClient("192.168.0.116", 27017)  # Mongodb_TargetIp, portNumber
db = connection.test  # testDB
collection = db.ngramData  # testDB testCollection
data = collection.find()

ngram_list=[]
for ngram in data:
        ngram_list.append(ngram['ngram'])


'''
arrange data format
'''
trainData = np.array(ngram_list, dtype='f')
trainClass = trainData.transpose()[-1:].transpose()
trainData = trainData.transpose()[:-1].transpose()
# match the size of array
trainClass = np.insert(trainClass,0,0.0,axis=1)

print 'Training Data Amount'
print len(trainData)


'''
set arguments for NN
'''
Layers=[2000,1300,2]
errFunChgLmt = 1e-6;
weightChgLmt = 1e-4;
maxRound = 1000;
learnRate = 1;

'''
Learning
'''
print 'Learning...'
bestNetwork = NeuralNetworkLearn(Layers,learnRate,errFunChgLmt,weightChgLmt,maxRound,trainData,trainClass)
print 'Done.'

print 'best training error function'
print bestNetwork.bestTrainErrFun
print 'best training error function rate'
print bestNetwork.bestTrainErrFunRate



'''
For DB data, make a weight list of best network
'''

weight_len = len(Layers)-1
weight_list = []

for i in range(weight_len):
	# split some weight into small size it is too large (DB INSERT ERROR)
	# merge later(in Detection code)
	if len(bestNetwork.w[i]) > 1000:
		div_len=len(bestNetwork.w[i])/3
		weight_list.append(bestNetwork.w[i][0:div_len].tolist())
		weight_list.append(bestNetwork.w[i][div_len:div_len*2].tolist())
		weight_list.append(bestNetwork.w[i][div_len*2:].tolist())
	else:
		weight_list.append(bestNetwork.w[i].tolist())


'''
insert weight into DB
'''
collection = db.weight  # testDB weight collection
collection.remove({}) # initialization
for i in range(len(weight_list)):
	collection.insert({'bestNN_weight':weight_list[i]})
print 'WEIGHT INSERTED'
