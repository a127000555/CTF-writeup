from pwn import *
from base64 import *
s1 = b64encode(open('shattered-1.pdf','rb').read())
s2 = b64encode(open('shattered-2.pdf','rb').read())
r = remote('bamboofox.cs.nctu.edu.tw',22006)
r.sendline(s1)
r.sendline(s2)
r.interactive()