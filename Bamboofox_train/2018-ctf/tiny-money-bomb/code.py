b58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
from pwn import * 
from hashlib import sha256

def base58encode(n):
	result = ''
	while n > 0:
		result = b58[n%58] + result
		n /= 58
	return result

def base256decode(s):
	result = 0
	for c in s:
		result = result * 256 + ord(c)
	return result

def base256encode(n):
	result = ''
	while n > 0:
		result = chr(n%256) + result
		n //= 256
	return result

def base58decode(s):
	result = 0
	for c in s:
		result = result * 58 + b58.find(c)
	return result

dec = lambda s : base256encode(base58decode(s))
enc = lambda s : base58encode(base256decode(s))

server = remote('bamboofox.cs.nctu.edu.tw',58787)
s = server.recvlines(3)[2]
while True:
	print('server response' , s)
	s = s.ljust(51, "A")
	s = dec(s)[:33]
	check = sha256(sha256(s).digest()).digest()
	cr = enc(s + check[:4])

	# key = base58.b58encode_check(key)


	# cr = correct(base256encode(base58decode(s)))
	server.sendline(cr)
	result = server.recv()
	print(result)
	i,s,_ = result.split('\n')
	if 'empty' in i:
		break

while True:
	left_s , right_s  = s.split(' ')
	for c in b58:
		now_s = left_s + c + right_s
		s = dec(now_s)
		mac = s[-4:]
		addr = s[:-4]
		calc_mac = sha256(sha256(addr).digest()).digest()[:4]
		if calc_mac == mac:
			server.sendline(now_s)
		# print(calc_mac,mac)
	# print('send!')
	result = server.recv()
	print(result)
	if len(result.split('\n'))!=3:
		break
	i,s,_ = result.split('\n')
	
server.close()
