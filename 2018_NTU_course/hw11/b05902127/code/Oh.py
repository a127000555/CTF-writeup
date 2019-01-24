from pwn import *
from termcolor import *
import math
from Crypto.Util.number import *
def power(a,b):
	assert len(a) == 2048 //4
	server.sendline(b'Power! Unlimited power!')
	server.sendlineafter(b'[>] Who are you? ',a)
	server.sendlineafter(b'[>] How strong do you want to be? ',str(b))
	msg = server.recvlines(2)[1]
	return msg
def mul(a,b):
	assert len(a) == 2048 //4
	assert len(b) == 2048 //4
	server.sendline(b"Help me!")
	server.sendlineafter(b"[>] What's wrong? ",a)
	server.sendlineafter(b'[>] Hmm... ',b)
	msg = server.recvlines(2)[1]
	return msg
def imul(a,b):
	assert len(a) == 2048 //4
	server.sendline(b"You're my only hope!")
	server.sendlineafter(b"[>] What's wrong? ",a)
	server.sendlineafter(b'[>] Hmm... ',str(b))
	msg = server.recvlines(2)[1]
	return msg
def whoru(a,b):
	assert len(a) == 2048 //4
	assert len(b) == 2048 //4
	server.sendline(b"What happened?")
	server.sendlineafter(b"[>] Who are you? ",a)
	server.sendlineafter(b'[>] Who am I? ',b)
	msg = server.recvlines(2)[0]
	return True if msg == b'[+] You were my brother, Anakin.' else False

def gen_E_EP(x):
	# given x, get AES_encrypt( Paillier_encrypt( x ))
	return imul(h[1],x)
def gen_E_EP_power(a,b):
	# given x, get AES_encrypt( Paillier_encrypt( x ))
	assert b < N
	E_EP_a = gen_E_EP(a)
	E_EP_a_pow_b = power(E_EP_a,pow(b,rsa_e,rsa_n))
	return E_EP_a_pow_b

def gen_E_EP_m_power_N(m):
	a = gen_E_EP_power(m,N-1)
	return imul(a,m)

def offset_E_EP(cipher,offset):
	E_EP_m2 = gen_E_EP(offset)
	return mul(cipher,E_EP_m2)
def i_to_512(x):
	return hex(x)[2:].rjust(2048//4,'0')
def is_1(x):
	return whoru(x,h[1] )

def find_what_N_bound(A_part, r):
	# given ?^e, output l,r which l 
	l = 1
	while r-l > 1:
		mid = (r+l)//2
		power_factor = (pow(mid,rsa_e,rsa_n) * A_part) % rsa_n
		res = whoru(power(h[chosen_m],power_factor),h[1])
		print('mid = %d ' %(mid)  , 'res = ',res)
		if res:
			l = mid
		else:
			r = mid
	return l,r
def get_value(x):
		return x[0] * rsa_n + x[1] * N + x[2]
def get_tuple(all_value):
	out0 = all_value // rsa_n
	out1 = (all_value - out0 * rsa_n) // N
	out2 = all_value - out0 * rsa_n - out1 * N
	return (out0, out1, out2)

def find_mid(a,b,c,r,layer=1):
	a = get_tuple(get_value(a) * 2)
	b = b *2
	c = get_tuple(get_value(c) * 2)
	mid =   get_tuple( (get_value(a)+get_value(c)) // 2)
	power_factor = (pow( b * r ,rsa_e,rsa_n) * lamb) % rsa_n
	A_part = power(h[chosen_m],power_factor)
	for i in range(-layer,layer+1):
		res = is_1(imul(A_part,pow(chosen_m, mid[1] * N +  mid[0] * rsa_n + i*N  ,N)))
		# print(res)
		if res:
			if i == 0:
				return find_mid(a,b,c,r,layer+1)
			print(colored(f'layer {layer} hit!','red'))
			if i < 0:
				return True # c = mid
			if i > 0 :
				return False # a = mid

def find_lambda():
	l,r = find_what_N_bound(lamb, 10**6)

	print('+' * 20)
	a, b, c = (0,1,0) , 1, (0,2,0)
	print("{} N < {} r * lambda < {}N".format(a,b,c))
	now_guess_d = 0

	for _ in range(1024):
		
		res = find_mid(a,b,c,r,1)
		
		a = get_tuple(get_value(a) * 2)
		b = b *2
		c = get_tuple(get_value(c) * 2)
		mid =   get_tuple( (get_value(a)+get_value(c)) // 2)
		print(colored(f'{a[0]}n + {a[1]}N + {a[2]*1.0}< b * r * d < {c[0]}n + {c[1]}N + {c[2]*1.0}' ,'cyan'))
		if res:
			c = mid
		else:
			a = mid

		now_guess_d = (get_value(a)//b//r  + get_value(c)//b//r) //2
		print(colored(now_guess_d,'green'))


	print('now now_guess_d , ',now_guess_d)
	

# server = remote('csie.ctf.tw',10141)
server = remote('localhost',10141)
tmp = server.recvuntil('[>]').split()
rsa_n, lamb, g, FLAG2, One = int(tmp[3]), int(tmp[7]), int(tmp[11]), tmp[14], tmp[17]
rsa_e = 65537
chosen_m = 3
remote_N = 3355606018780219439641525028884199752769801998561640011737388608153379282249382897148298658962575535024085284928972539734583078821643846525056379100313329257692793347640441779084228476012774165371914928109864718335414973965255366726816214172666968247116508581832522056479503720544089865656910596305589
remote_d = 34277953896870282546851952406523379908572558058324718693049508735503496457897142798826267789267733824586647648772882298553364647696935936064073172005532781919357777989823129512740603351131571245843881519698188897779616849300252286417581339672229123683070279049655004410429112257006578615654316946
local_N = 1635481817348904330966383028809394436505825569570534036045830391868525867003626073953825875387848973817432130296407322212723117626680085082752449868862293802596682229511976372125927116399164411888087813990349732219819108437069081523413373201667328491746465602581942880783371012145897092010173235723301
local_d = 17979835726445156559512576997091031821044233521366439128931096412441743442356435368107845862974087792896287793764509599752898107195093391556391128920425150214299833080641507031517819296547601157503392036344790735080806472348008052673250018943061823352309631819146855349323062753807519743268877766

# N, d = remote_N, remote_d
N, d = local_N, local_d

N2 = N * N
h = {}
h[1] = One
# ========================= #
# print(whoru(One_in_h,One_in_h))
h[chosen_m] = gen_E_EP(chosen_m)
h[0] = gen_E_EP(0)
# find_lambda() : flag{--_~~ H0w I|v3 m1s5ed y0u ~~_--}

g_half_d = pow(g, d // 2, N) 

# print(g_half_d)
# print(g_half_d*g_half_d %N)

now_FLAG2 = FLAG2
minus_1 = inverse(g,N)


for now_bit_order in range(0,10):
	tmp_FLAG2 = now_FLAG2
	for _ in range(now_bit_order):
		power(tmp_FLAG2, pow(d//2,rsa_e,rsa_n))
		# print(is_1(power(tmp_FLAG2, pow(d//2,rsa_e,rsa_n))))

	res = is_1(power(imul(tmp_FLAG2, inverse(g,N)),pow(d//2,rsa_e,rsa_n) ))
	res2= is_1(power(tmp_FLAG2,pow(d//2,rsa_e,rsa_n) ))
	if res:
		now_FLAG2 = imul(now_FLAG2, inverse(g,N)*pow(2,now_bit_order,N))

	print(res,res2,is_1(now_FLAG2))
		# now_FLAG2 = pow(now_bit_order)
	# else:
			

print(is_1(
	power(
		power(
			imul(FLAG2,pow(inverse(g,N),1,N)),
			pow(d//2, rsa_e,rsa_n)
		), pow(d//2, rsa_e,rsa_n))))
print(is_1(
		power(
			imul(FLAG2,pow(inverse(g,N),1,N)),
			pow(d//2, rsa_e,rsa_n)
		)))
print(is_1(
		power(
			imul(FLAG2,pow(inverse(g,N),3,N)),
			pow(d*d//2//2, rsa_e,rsa_n)
		)))
print(is_1(
		power(power(
			power(h[chosen_m],1),
			pow(d//2, rsa_e,rsa_n)
		),
			pow(d//2, rsa_e,rsa_n))

))
print(d*d//2//2/rsa_n)
# FLAG - 1 * 
# FLAG + 1 = FLAG

server.interactive()