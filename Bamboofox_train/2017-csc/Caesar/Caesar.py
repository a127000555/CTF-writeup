s = 'ONZOBBSBK{LbHXAbjpNRFNEQBaglBH}'
m = 'BAMBOOFOX{                    }'
for i,j in zip(s,m):
	i , j = ord(i),ord(j)
	print(i,j,i-j)
for c in s:
	print(chr(ord(c)+13),chr(ord(c)-13))
'''
Y ?
o U
U ;
e K
N 4
o U
w ]
} c
[ A
_ E
S 9
[ A
R 8
^ D
O 5
n T
t Z
y _
O 5
U ;

BAMBOOFOX{YoUKNowcAESARDOntyOU}
'''