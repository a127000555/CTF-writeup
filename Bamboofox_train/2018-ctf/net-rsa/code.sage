from Crypto.Util.number import *

load("coppersmith.sage")
N = 191549949433723386840002778806410465057
e = 65537
C = 157396899712935842966144562474528825171
prefix = b"BAMBOOFOX{1234567890000"
prefix_n = bytes_to_long(prefix)
for suffix_len in range(16,0,-1):
    print('now length: %d' % suffix_len)
    m = prefix_n * pow(256,suffix_len,N)
    ZmodN = Zmod(N)
    P.<x> = PolynomialRing(ZmodN)
    f = (m + x)^e - C
    dd = f.degree()
    beta = 0.5                             # we should have q >= N^beta
    epsilon = beta / 7                     # <= beta/7
    mm = ceil(beta**2 / (dd * epsilon))    # optimized
    tt = floor(dd * mm * ((1/beta) - 1))   # optimized
    XX = ceil(N**((beta**2/dd) - epsilon)) # we should have |diff| < X
    print('run!')
    roots = coppersmith_howgrave_univariate(f, N, beta, mm, tt, XX)
    print('finish!')
    for r in roots:
        print(long_to_bytes(r))