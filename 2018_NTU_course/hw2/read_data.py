file_name = 'debase64_data'
data = None
with open(file_name,'r') as fin:
	data = fin.read()
from collections import Counter
data2 = Counter(list(data))
# print(data2)
d = {'x' : ']' , 'F' : '[', 'B' : '>' , 'a' : '<', 'b' : '-' , 'm' : '+', 'O' : ',' , 'o' : '.' }
m = [0 for i in range(1000)]
p = 0
pc = 0
s = []
out = ""
while pc != len(data):
	c = d[data[pc]]
	if c == '>':
		p += 1
	elif c == '<':
		p -= 1
	elif c == '+':
		m[p] += 1
	elif c == '-':
		m[p] -= 1
	elif c == '.':
		pass
		# print(chr(m[p]),end='')
	elif c == ',':
		pass
	elif c == '[':
		if m[p] == 0:
			x = 1
			pc += 1
			while x != 0:
				if d[data[pc]] == ']':
					x -= 1
				elif d[data[pc]] == '[':
					x += 1
				pc += 1
			pc -= 1
		else:
			s.append(pc)
	elif c == ']':
		if m[p] != 0:
			pc = s[-1]
		else:
			s = s[:-1]
	check = ''.join(map(chr,filter(lambda x: chr(x).isprintable() , m)))
	out += check
	pc += 1

dup = 9
import numpy as np 
filter2 = ""
for i in range(len(out)-dup):
	ar = out[i:i+dup]
	target = ar[0]
	for c in ar:
		if c != target:
			break
	else:
		filter2 += target

print(filter2[0] ,end='')
for i in range(1,len(filter2)):
	if filter2[i] != filter2[i-1]:
		print(filter2[i], end='')