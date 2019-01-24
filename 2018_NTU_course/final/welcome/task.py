#!/usr/bin/python3
import random
import time
import codecs
import sys

# Secrets
flag = b'flag{xxxxxxxxxxxxxx}'
myCommonPassword = b'xxxxxxxx'


flag1 = flag[:len(flag) // 2]
flag2 = flag[len(flag1):]


seed = int(time.time())
print(seed, file=sys.stderr)
random.seed(seed)
flag1 = bytes(c ^ random.randrange(256) for c in flag1)


seed = int.from_bytes(myCommonPassword, 'little')
print(seed, file=sys.stderr)
random.seed(seed)
flag2 = bytes(c ^ random.randrange(256) for c in flag2)


flag = flag1 + flag2

print(sys.version)
print(codecs.encode(flag1 + flag2, 'base64').decode('ascii'))
