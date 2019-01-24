import time
import json
from Crypto.Util.number import *

load("coppersmith.sage")

N,e,C = json.load(open('data','r'))
prefix = b"Let me sleep, just let me sleep. Maybe go to sleep. I want to go to sleep. When can I go to sleep."
prefix_n = bytes_to_long(prefix)
for suffix_len in range(5,1000):
    m = prefix_n * pow(256,suffix_len,N)
    ZmodN = Zmod(N)
    P.<x> = PolynomialRing(ZmodN)
    f = (m + x)^e - C
    dd = f.degree()
    beta = 1
    epsilon = beta / 20
    mm = ceil(beta**2 / (dd * epsilon))
    tt = floor(dd * mm * ((1/beta) - 1))
    XX = ceil(N**((beta**2/dd) - epsilon))
    roots = coppersmith_howgrave_univariate(f, N, beta, mm, tt, XX)
    for r in roots:
        print(long_to_bytes(r))