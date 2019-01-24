from pwn import *
r = process('./lab-2')
# buffer: format 0x200e20, every read 0x60 char
# r.interactive()
