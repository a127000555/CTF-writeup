c = 150815
d = 1941
N = 435979

from Crypto.Util.number import *
print(long_to_bytes(pow(c,d,N)))
print(pow(c,d,N))