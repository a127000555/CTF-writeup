from pwn import *
r = remote('bamboofox.cs.nctu.edu.tw',22005)
l , ri =1 , 500000000
while True:
	r.recvuntil('Input number = ')
	mid = (ri+l)//2
	print('%30d , %30d , %30d' %(l,mid,ri))
	r.sendline(str(mid))
	key = r.recv().split()[-1]
	print(key)
	if key == b'Congratulations':
		break
	if  key== b'small':
		l = mid
	else:
		ri = mid
r.interactive()