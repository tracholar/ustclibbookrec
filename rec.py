# coding:gbk
import random
import math

data = []
for line in open('lendformat.txt','r'):
	user,iterm = line.split(',')
	iterm = iterm.replace('\n','')
	data.append([user,iterm])
	
def SplitData(data,M,k,seed):
	test = []
	train = []
	random.seed(seed)
	
	for user,iterm in data:
		if random.randint(0,M) == k:
			test.append([user,iterm])
		else:
			train.append([user,iterm])
	return train,test
	
train = dict()
test = dict()
tr, te = SplitData(data,3,1,0)
for user,iterm in tr:
	if train.has_key(user):
		if iterm in train[user]:
			pass
		else:
			train[user].append(iterm)
	else:
		train[user]=[iterm]
	
for user,iterm in te:
	if test.has_key(user):
		if iterm in test[user]:
			pass
		else:
			test[user].append(iterm)
	else:
		test[user]=[iterm]
	
# print train,test

def UserSimilarity(train):
	W = dict()
	f = open('W.txt','w')
	for u in train.keys():
		# W[u] = dict()
		for v in train.keys():
			if u==v:
				continue
			t = len([i for i in train[u] if i in train[v]])
			t /= math.sqrt(len(train[u]) * len(train[v]) * 1.0)
			f.write('%.4f ' % t)
			# W[u][v] = len([i for i in train[u] if i in train[v]])
			# W[u][v] /= math.sqrt(len(train[u]) * len(train[v]) * 1.0)
		f.write('\n')
		print u	
	f.close()
	return W
	
W = UserSimilarity(train)

print W
	