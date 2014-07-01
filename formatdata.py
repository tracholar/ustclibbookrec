# coding:gbk
import re

f = open('lend.txt','r')
fo = open('lendformat.txt','w')
f.readline()
f.readline()
line = f.readline()
data = []
i = 0
while line:
	tmp = re.split(r'\s+',line)
	#print tmp
	if len(tmp) >= 3:
		data.append([tmp[0] ,tmp[2]])
		fo.writelines(','.join([tmp[0] ,tmp[2]]) + '\n')
	print i
	i += 1
	
	line = f.readline()
	


f.close()
fo.close()
