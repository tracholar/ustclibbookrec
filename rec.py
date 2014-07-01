# coding:utf-8
import random
import re
import math
import json
from operator import *
import SimpleHTTPServer
import SocketServer
import urllib

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
tr, te = SplitData(data,3,-1,0)
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
				if not C.has_key(u):
					C[u] = dict()
				if not C[u].has_key(v):
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

K = 10
def Recommend(user, train, W):
	rank = dict()
	if user not in train.keys():
		return rank
	interacted_items = train[user]
	for v,wuv in sorted(W[user].items(), key=itemgetter(1),reverse=True)[0:K]:
		for i in train[v]:
			if i in interacted_items:
				continue
			rank[i] = wuv
			
	return rank
	

## 前端显示部分 

# request handler
class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		m = re.match(r'/rec/([^/]+)',self.path)
		if m:
			print self.path
			uid = m.group(1)
			res = Recommend(uid,train,W)
			
			data = dict()
			data['book'] = res
			bookInfo = dict()
			for bid in res.keys():
				bookHtml = urllib.urlopen('http://opac.lib.ustc.edu.cn/opac/item.php?marc_no=' + bid).read()
				s=re.search(r'<div id="item_detail" style="float:left; width:80%;">(.+)<div style="text-align:left;color:blue;" id="showMoreAnchor"',bookHtml,re.S)
				if s:
					bookInfo[bid] = s.group(1).replace('<a href="','<a target="_blank" href="http://opac.lib.ustc.edu.cn/opac/')
			data['info'] = bookInfo
			
			html = json.dumps(data)
			print res
			self.protocol_version = 'HTTP/1.1'
			self.send_response(200,'OK')
			self.send_header('Content-Type','text/json')
			self.end_headers()
			self.wfile.write(html)
		else:
			return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
	
		
		
		
		
PORT = 80
Handler = MyRequestHandler
server = SocketServer.TCPServer(('0.0.0.0',PORT),Handler)
server.serve_forever()

print 'server at port ', PORT



		
