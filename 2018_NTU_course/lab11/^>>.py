# def xorshift(s):
#     s ^= (s & MASK) << 13
#     s ^= (s & MASK) >> 7
#     s ^= (s & MASK) << 17
#     return s & MASK


from Crypto.Util.number import getRandomRange
import os
import numpy as np
MASK = (1 << 64) - 1

def reduce(l):
	has = [ 0 for _ in range(64)]
	for i in l:
		has[i] = 1 - has[i]
	l2 = [i for i in range(64) if has[i]]

	return l2
def xorshift_l(l):
	right_shit_13 = [[]] * 13 + l
	l = [ a+b for a,b in zip(l,right_shit_13)]
	left_shit_7 = l[7:] + [[]] * 7
	l = [ a+b for a,b in zip(l,left_shit_7)]
	right_shit_17 = [[]] * 17 + l
	l = [ reduce(a+b) for a,b in zip(l,right_shit_17)]
	return l
def xorshift(s):
    s ^= (s & MASK) << 13
    s ^= (s & MASK) >> 7
    s ^= (s & MASK) << 17
    return s & MASK

l = [ [i] for i in range(64)]
s0 = getRandomRange(0, (1 << 64))
s = s0
given = '.1..0....110..0.1010..1001..00......0.1.10101.....01.1.....000..0.10......00..01..1..10.00.0..1.1........0.1001.0.001...0..01.110110.1.1.0..110..1..010.1.1..1..01..1..0.1....0...0.1......011.110...11.'
mat,y = [],[]
for _y , i in zip(given,range(200)):
	l = xorshift_l(l)
	if _y != '.':
		mat.append(np.array([ 1 if i in l[0] else 0 for i in range(64)]+[int(_y)]))
		y.append(int(_y))
used = [0 for _ in range(256)]
for i in range(64):
	base_line = -1
	for j,row in enumerate(mat):
		if row[i] == 1 and used[j] == 0:
			base_line = j
			used[j] = 1
			break
	for j,row in enumerate(mat):
		if row[i] == 1 and j != base_line:
			mat[j] = (mat[base_line] + mat[j]) % 2

answer = [0 for i in range(64)]
for row in mat:
	idx = np.argmax(row)
	if row[idx] == 1:
		answer[idx] = row[64]
s = int(''.join(list(map(str,answer[::-1]))),2)
print(s)
# s = getRandomRange(0, (1 << 64))

r = ''
for _ in range(200):
    s = xorshift(s)
    r += str(s & 1)
print(r)
print(given)
print(s)

# print(mat)
# 
