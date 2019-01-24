import hashlib
import sys
import binascii
import struct

# if len(sys.argv) != 2:
#     print('Usage: python3 task.py <password>')
#     exit(255)


def md5(s):
    return hashlib.md5(s.encode('ascii')).hexdigest()

sys.argv.append('s')
hashs = ''.join(map(md5, sys.argv[1]))
m = int(hashs, 16)
A = b'''
bc69f315c01224ca6778d124281a31f5ffaf7e97ef666f349fb6c6d390e1bd2b
4ece1d956c577f57920ff9a082b6855ea9a99914f21491b4012cad5aecb93c44
c0b1cabd5a7573b53fb6b4a3b7025a19a40c8ced23b93d4d80f189f2c9e94360
cd41bc81dba40b782011adcd4359d4ef1af2d6d71a8c1352090d0b95b84d11e6
c619c27a45db86b76aeb4fa3b4fff12783e20a40fe25bab19ea9221a0c08d960
9b0df26bd6ab5c4b0a26a269407bbdbc630c4e2609c1980cb0ab545097325f7e
e2a37bbdfc3f08b166e50cbe89daabc197385a0d7b59e5b5e1ebb4ebff499959
995611f14faec3531defbbce4c39cd0750fc46699850b82adcc11f31de7172e7
1d45ab686016f181b82c4275ea024d2c68bb073cd0121857cad4cf4846c474ea
a4b970ec1c0280cf6ffc7d6baab06338edef2b00e4201a22798d07ade14fdb18
1959db018acab1cc5ff742d66bb6144e2e568491715c19a985e9592dcdcf93ca
4793a61becb8ead82110b7db361bd2ed11c19c9d6dc30c2d5925cdd7c3a688c5
4ceb08129fcabdf4ac51fcfaeb24647d09c1dff6e427f51b90c9d40902e0f0c2
b28e0dc8f1d382f1bc282629fb082321651019a62d9341e9c4be1c415cbd8397
fdca24617d48127d2f21b9d29800c25876beff87dc6cf6677856e4e8787d8bdb
6219c9a746c64ef18236f12a9137511e84c1df56a98d7e030037579b3f34522d
'''.replace(b'\n', b'')


a = int('''
d3d36115599d53eeb0413c3a818e120bc1ce4cc9bca9e7b23a695a150c056c4a
6ca2e3ce99efe8a0f4385e86e8897d2e47bd25a45e723b768af040e2b6d73beb
193fb86aae849513463e3a794768ab865b4b82bd5df627e83afdfc0ee00bc983
2e6c38e53d2812a344ff34008198e142e642c95a449a762d7fd30df018fa5fe6
53c882a192d011594a29a0926fe841473622a61e41ac0f675f5fda76a27561ff
c7c90c6d85464f23fab9e88bfca8ed5a0f2e0e11c0a0f4521e1919194e868d18
c0d33f5fdc0cb95793ca96f7b8a7127cb9ae6acde7e158bcf718cf30ea69933e
f6cdefa6f9383f8c9735f9510f70f228d299479a257c1a2d3c10d1f47cc1a055
'''.replace('\n', ''), 16)
K = hex(a).encode('ascii')
S = list(range(256))
j = 0
for i in range(256):
    j = (j + S[i] + K[i % len(K)]) % 256
    S[i], S[j] = S[j], S[i]

j = 0
XOR_list = []
for k in range(512):
    i = (k + 1) % 256
    j = (j + S[i]) % 256
    S[i], S[j] = S[j], S[i]
    XOR_list.append(S[(S[i] + S[j]) % 256])





b = int('''
e5b537e60922d57a763918a5b1e8af1bc07c85fefea11e8179f2a9ee6cf7c611
7d0eba7963617035cf1ddb1f0cc858d70890a76990f96adb29ea8b0403f869cd
be51b76f06c25a9319ecd04366f846338fc1f81ae05f143940039bfbbc4de953
b933c89e74fe62485157d7a3b31993915808a4b95bb768f369818c10edfa561e
3530c999c33ef62a4466ec67622cc12525cf0ea3d402931d16ef115acc172641
a63037190ba04931d3caa2ef861ee7f277647844f8a7f94569f06cea32badb02
82355467cec0bdbdff5e7cd837ffce048925280ab92a9560c1cd6bd309239d7e
72b298af5ad81d27ee9adf7143185815bdadfa21296833149748ed2f55343533
'''.replace('\n', ''), 16) * a
init_b = int('''
e5b537e60922d57a763918a5b1e8af1bc07c85fefea11e8179f2a9ee6cf7c611
7d0eba7963617035cf1ddb1f0cc858d70890a76990f96adb29ea8b0403f869cd
be51b76f06c25a9319ecd04366f846338fc1f81ae05f143940039bfbbc4de953
b933c89e74fe62485157d7a3b31993915808a4b95bb768f369818c10edfa561e
3530c999c33ef62a4466ec67622cc12525cf0ea3d402931d16ef115acc172641
a63037190ba04931d3caa2ef861ee7f277647844f8a7f94569f06cea32badb02
82355467cec0bdbdff5e7cd837ffce048925280ab92a9560c1cd6bd309239d7e
72b298af5ad81d27ee9adf7143185815bdadfa21296833149748ed2f55343533
'''.replace('\n', ''), 16) 

assert( m < b )
phi_b = (a-1) * (init_b-1)
m = pow(m, 65537, b)
m = hex(m)[2:].rjust(1024, '0')
# print(binascii.a2b_hex(m))
m = list(binascii.a2b_hex(m))
# print(m)
# exit()

for k in range(512):
    m[k] ^= XOR_list[k]

x, delta, mask = 0, 0x9e3779b9, 0xffffffff
sum_array = [0]
for i in range(33):
    x = (x + delta) & mask
    sum_array.append(x)

k = struct.unpack("<4L", K[:16])
for i in range(0, len(m), 8):
    v0, v1 = struct.unpack("<2L", bytes(m[i:i+8]))
    
    sum, delta, mask = 0, 0x9e3779b9, 0xffffffff
        
    for round in range(32):
        v0 = (v0 + (((v1 << 4 ^ v1 >> 5) + v1) ^ (sum_array[round] + k[sum_array[round] & 3]))) & mask
        v1 = (v1 + (((v0 << 4 ^ v0 >> 5) + v0) ^ (sum_array[round+1] + k[sum_array[round+1] >> 11 & 3]))) & mask

    # print(v0,v1)
    e = struct.pack("<2L", v0, v1)
    for j in range(8):
        m[i+j] = e[j]
A2 = [int(c)for c in binascii.a2b_hex(A)]
rev_m = b''
for i in range(0,len(A2),8):
    e = [0 for i in range(8)]
    for j in range(8):
        e[j] = A2[i+j]
    # print(e)
    # print(bytes(e))
    v0 , v1 = struct.unpack("<2L" , bytes(e))
    sum, delta, mask = 0, 0x9e3779b9, 0xffffffff
    # print("req:" , v0,v1)
    # exit()
    # v0, v1 = struct.unpack("<2L", bytes(m[i:i+8]))
    
    for round in range(32,0,-1):
        v1 = ( 1 + mask + v1 - (((v0 << 4 ^ v0 >> 5) + v0) ^ (sum_array[round] + k[sum_array[round] >> 11 & 3]))) & mask 
        if(v1<0):
            v1 +=  0x100000000
        v1 = v1 & mask
        v0 = ( 1 + mask + v0 - (((v1 << 4 ^ v1 >> 5) + v1) ^ (sum_array[round-1] + k[sum_array[round-1] & 3]))) & mask
        if(v0<0):
            v0 +=  0x100000000
    
    this_m = struct.pack("<2L" , v0,v1)
    rev_m += this_m
rev_m = list(rev_m)
for k in range(512):
    rev_m[k] ^= XOR_list[k]
# exit()
# print(rev_m)
rev_m = ''.join([ hex(c)[2:].rjust(2,'0') for c in  rev_m])
# m = pow(m, 65537, b)
# m = hex(m)[2:].rjust(1024, '0')
# m = list(binascii.a2b_hex(m))

def gcd(a,b):
    while a!=0:
        a,b = b%a,a
    return b


def findModReverse(a,m):
    if gcd(a,m)!=1:
        return None
    u1,u2,u3 = 1,0,a
    v1,v2,v3 = 0,1,m
    while v3!=0:
        q = u3//v3
        v1,v2,v3,u1,u2,u3 = (u1-q*v1),(u2-q*v2),(u3-q*v3),v1,v2,v3
    return u1%m
rev_m = int(rev_m,16)
# print('rev_m:' , rev_m)


x = findModReverse(65537, phi_b)


fin = hex(pow(rev_m,x,b))[2:]




# print(fin)
fin = [ fin[i:i+32]for i in range(0,len(fin),32)]
import string
d = { md5(c) : c for c in string.printable}
for x in fin:
    print(d[x] , end='')


# m^65537 % b = r
# import math
# print(math.log(int(rev_m,16),65537))   
'''
'f6fd92dce52d82b61538575020db2bca996b2435306384d04b5b87e16f40b1fdec097efacca93133ce00aae96ae41533012f12f3e3be3e3030ef1fbdf3f792069aad4be106d1418570fb2dc4add29773ae14d8602761dc213ce437cd1e1cdd0c5fcb3b7e8f906a573bd8c0ad5212533b6b5766ddbfcefae3f819a604d1c98882240a6a34aec0e6822f6daae6652826082e44b3a3358b06f19226e9d8ed0655d0c49f676f02f3428a99ee4ab00da6dff75c2fbcc08357a4e0e3ae4272d967e4b50d2626f80dbff1f404160b930187092a72e93f47169b13590416e23715e7ece260660b12a61a99f9046b9befff37bfa4a6e758ea74ef1cae3a98c776424e6851ac1916f82eeeb9bfdbd5d33499d832b3625f0967d89ec5d5394a8412a87fe6d7d3ea55e030738ab73dcea874c7a6be636aaf7bd534718c2215e2e03ba5a696296cde40586359bde6e1e12f1b1a7e9a7e8b8ff5d2967331e9a6e45191c231132f62a66519e8857ad918ac9aa672d790c3e1c3d1f9d1180f1d8f68c2ecfe2aa7517468d87393b502c662469892a1c11bec717a0db46c74ff49769cad54f8acbbd62d73807a3a012359c70d0690a590c90298320c56dcbb584b8a60ebf48c894616646fd1095c10a903d0a01a0df5a2b3faa85a1e6939c445b20c53056877e6954ff61c08bc9faf46362a28e35e64d3fe7960964b390677f33daefa96d663ae3306
'''
# print(m[:10])
# print(bytes(m[:10]),"\n")

m = bytes(m)
m = binascii.b2a_hex(m)


# print(m)