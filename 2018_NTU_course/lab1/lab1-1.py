from pwn import *
r = remote('csie.ctf.tw',10123)
s  = r.recvline()
s  = r.recvline()
s  = r.recvline()

for _ in range(100):
	s  = r.recvline()
	print(s)
	s  = r.recvline().strip().decode()
	s = sorted(list(map(int,s.split())))
	r.send(' '.join(map(str,s)) + '\n')

r.interactive()