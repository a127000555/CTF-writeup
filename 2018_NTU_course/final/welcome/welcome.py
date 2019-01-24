#!/usr/bin/python3
import random
import time
import codecs
import sys
from base64 import *
# Secrets
# flag = b'flag{xxxxxxxxxxxxxx}'
# myCommonPassword = b'xxxxxxxx'
# print(sys.version)
# print(int(time.time()))
# exit()

# flag1 = flag[:len(flag) // 2]
# flag2 = flag[len(flag1):]
seed = 1547167075
secret = b64decode(b'x1FtPcm9gAtLVXFmCkINH7INJd6/aFI/M6SlYjh6T+iqnN97SfdfClZC9Ms3fDfyQhIeq1oP')
secret1 = secret[:27]
secret2 = secret[27:]

random.seed(seed)
flag1 = bytes(c ^ random.randrange(256) for c in secret1)
if flag1.startswith(b'fl'):
	print(flag1)

# rockyou.txt is the password collection name.
with open('rockyou.txt','r') as  fin:
	for row in fin:
		seed = int.from_bytes(bytes(row.strip().encode()), 'little')
		# print(seed)
		# exit()
		# print(seed, file=sys.stderr)
		random.seed(seed)
		flag2 = bytes(c ^ random.randrange(256) for c in secret2)
		try:
			print(flag2.decode())
			print(row)
			print()
		except:
			continue
# flag = flag1 + flag2

# print(codecs.encode(flag1 + flag2, 'base64').decode('ascii'))
# flag{\\|/-3b4dabaf1e772-H4pPy_N3w_y3aR-ccce3295f562\|/}
