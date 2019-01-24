from pwn import *
r = remote('127.0.0.1',12777)
left , right = 10000000 , 100000000
while True:
	result = r.recv().decode()
	print(result)
	if result.startswith("no"):
		break
	m = (left+right) //2
	r.send(str(m) + "\no")
	result = r.recvline().decode()
	print(m , ":" ,result)
	if result.startswith("hi"):
		right = m
	else:
		left = m
'''
solution 1
x/wx $rbp-0x94
p $eax -> get eax
p/d 0xc -> get *(0xc)
c -> continuing


solution 2
patch to nop



forest:

y -> change type
n -> change variable name

ncat -vc shellsort -kl 127.0.0.1 8888

'''