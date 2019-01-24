import os
from rng import RNG
from pwn import *
from arts import maze, mazeDir, bossBG, gameOver, boom, win
import time
# # Variable initialization
p = 198543992929796982831856294122484542605661595500963697094465382211596515703899
rng = RNG(p, pow(0xdeadbeef, 31337, p) // 2)
print(bin(rng.M)[2:])
print(bin(rng.max)[2:])
print(bin(rng.entropy_pool)[2:])
print(len(bin(rng.entropy_pool)[2:]))

M_list = [ int(i) for i in bin(rng.M)[2:]]

# now_status = 	[ int(i) for i in bin(rng.entropy_pool)[2:]]+ \
# 				[ 0 for i in range(256)]
# for i in range(256):
# 	if now_status[i] == 1:
# 		for j,m in zip(range(i,i+256),M_list):
# 			now_status[j+1] = (now_status[j+1] + m) % 2
# print(now_status[256:])
x = 0b1000000000011011011100101001000000011111101101101010001001111110100101011011001110100000110101100011110111100101000111001010000100110111010111101100101100010101100101101100111000010100111110100111111000111010000100110110111010110101010001101010000111111101
M3 = rng.M ^ (rng.M*2) ^ (rng.M*4)
print(bin(M3))
print(bin(x))

# exit()
r = remote('edu-ctf.zoolab.org',8400)
with open('path31337','r') as fin:
	for row in fin:
		print(row)
		print(r.recvuntil('[>]').decode())
		r.sendlineafter('ction:',row.strip())
		# time.sleep(0.01)
for i in range(52):
	print(r.recvuntil('[>]').decode())
	r.sendlineafter('ction:','a')
	time.sleep(0.01)


r.interactive()
while True:
	row = input()
	print(row)
	if row == 'auto':
		break
	print(r.recvuntil('[>]').decode())
	r.sendlineafter('ction:',row.strip())
	# time.sleep(0.01)

for i in range(42):
	r.sendlineafter('ction:','a')
	time.sleep(0.01)

