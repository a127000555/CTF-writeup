import os
import msgpack
usr = b'\x12'
pwd = '456'
vc = os.urandom(20).hex()
print(len(vc))
token = {'usr': usr, 'pwd': pwd, 'vc': vc}
token = msgpack.dumps(token)
print(token)
for i in range(256):
	print(msgpack.loads(token[:-1] + bytes([i])))
