# coding:gbk
import random
import math
from operator import *
import web

data = []
for line in open('lendformat.txt','r'):
	user,item = line.split(',')
	item = item.replace('\n','')
	data.append([user,item])
	
def SplitData(data,M,k,seed):
	test = []
	train = []
	random.seed(seed)
	
	for user,item in data:
		if random.randint(0,M) == k:
			test.append([user,item])
		else:
			train.append([user,item])
	return train,test
	
train = dict()
test = dict()
tr, te = SplitData(data,3,1,0)
for user,item in tr:
	if train.has_key(user):
		if item in train[user]:
			pass
		else:
			train[user].append(item)
	else:
		train[user]=[item]
	
for user,item in te:
	if test.has_key(user):
		if item in test[user]:
			pass
		else:
			test[user].append(item)
	else:
		test[user]=[item]
	
# print train,test

def UserSimilarity(train):
	item_users = dict()
	for u, items in train.items():
		for i in items:
			if i not in item_users:
				item_users[i] = set()
			item_users[i].add(u)
	print 'create item_users table finished!'		
	
	C = dict()
	N = dict()
	for i,users in item_users.items():
		for u in users:
			if not N.has_key(u):
				N[u] = 1
			else:
				N[u] += 1
				
			for v in users:
				if u==v:
					continue
				if (not C.has_key(u)) or (not C[u].has_key(v)):
					C[u] = dict()
					C[u][v] = 1
				else:
					C[u][v] += 1
					
	print 'create C[u][v] finished!'
	
	W = dict()
	
	#f = open('UserSimilarityMatrix.txt','w')
	for u, related_users in C.items():
		for v, cuv in related_users.items():
			if not W.has_key(u):
				W[u] = dict()
			W[u][v] = cuv / math.sqrt(N[u] * N[v])
	#		f.write('%s %s %.5f\n' % (u,v,W[u][v]))
	#f.close()
	print 'create W[u][v] finished!'
	
	return W
	
W = UserSimilarity(train)

K = 3
def Recommend(user, train, W):
	rank = dict()
	interacted_items = train[user]
	for v,wuv in sorted(W[user].items(), key=itemgetter(1),reverse=True)[0:K]:
		for i in train[v]:
			if i in interacted_items:
				continue
			rank[i] = wuv
			
	return rank
	

	
PORT = 80
urls = ( '/', 'Index',)
app = web.application(urls,globals())


class Index:
	def GET(self):
		id = web.input().uid
		html = "<br/>".join(['%s="%s"' % (key,value) for (key,value) in Recommend('0813006060',train,W).items() ])
		print html
		return html 

print 'server at port ', PORT
app.run()


		
