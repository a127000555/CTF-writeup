from phe import *
from Crypto.Util.number import *
from Crypto.PublicKey import RSA
# N = 3355606018780219439641525028884199752769801998561640011737388608153379282249382897148298658962575535024085284928972539734583078821643846525056379100313329257692793347640441779084228476012774165371914928109864718335414973965255366726816214172666968247116508581832522056479503720544089865656910596305589

rsa = RSA.generate(1024, e=65537)
N = rsa.n
ppub = paillier.PaillierPublicKey(n=N)
ppri = paillier.PaillierPrivateKey(ppub, rsa.p, rsa.q)
# l = rsa.q * rsa.p // GCD(rsa.q,rsa.q)
l = (rsa.p-1) * (rsa.q-1)
g = ppub.g
N2 = rsa.n ** 2

# print(l,rsa.p)
# print(ppub.g)
# rsa.encrypt(0,None)[0]
# print(he)
# m = log_g ( c^lambda % N^2 ) * inv(lambda)
def self_enc(m):
	r = 7
	return (pow(g,m,N2) * pow(r,N,N2)) % N2
def self_dec(c,l,n):
	u = pow(c, l, N2)
	l_of_u = ppri.l_function(u,N)
	return (l_of_u * inverse(l,N)) % N
	# return (ppri.l_function(pow(c,l,N2),N+1) * inverse(l,N)) %N
# print((ppri.l_function(0,rsa.n) * inverse(l,N) )% N)
# c = ppub.raw_encrypt(123)
# c = self_enc(123)
# print('+' * 50)
# print(self_dec(c,l,N))
# print('+' * 50)
# print(ppri.raw_decrypt(c))
# print('+' * 50)
# print(rsa.encrypt(5, None))
# print(rsa.encrypt(5, None))
# print(rsa.encrypt(5, None))
# help(rsa.encrypt)
# exit()
c = ppub.raw_encrypt(123)
print(c)
c = ppub.raw_encrypt(123)
print(c)
# exit()
# c = 0

# print('a')
# print(ppri.raw_decrypt(c))
# print('c')
#   d(0) * (N-l) = d^-1
cal_l = N-inverse(self_dec(0,l,rsa.n),N) 
print( cal_l -l ) 
print('d')

print(self_dec(1,l,rsa.n))
# print(ppri.crt(-ppri.hp ,-ppri.hq ))
# print(ppri.hp)
# print(ppri.h_function(ppri.p,ppri.p**2))

# help(ppri.crt)
# L(0,ppub.g) = -1 / p
'''
 |  h_function(self, x, xsquare)
 |      Computes the h-function as defined in Paillier's paper page 12,
 |      'Decryption using Chinese-remaindering'.
 |  
 |  l_function(self, a, N)
 |      Computes the L function as defined in Paillier's paper. That is: L(a,N) = (a-1)/N
 |  cal where x is g^x = a % N**2
 |	cal where x is x = log_g(a) % N **2 

 crt(mp, mq) method of phe.paillier.PaillierPrivateKey instance
    The Chinese Remainder Theorem as needed for decryption. Returns the solution modulo n=pq.
    
    Args:
       mp(int): the solution modulo p.
       mq(int): the solution modulo q.

'''
# print(ppri.r)
# print(N**0.99)l