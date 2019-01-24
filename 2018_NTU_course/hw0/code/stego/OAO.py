from skimage import io
img=io.imread('OAO.png')
import matplotlib.pyplot as plt
img = img[:,:,2]

img2 = img & 1

img2 = img2.reshape([-1,8]).tolist()

f = []
for i in img2:
	f.append(chr(int(''.join(list(map(str,i))),2)))

idx = ''.join(f).find('CS 2018 Fall')
f = []
for i in img2:
	print(i)
	x = int(''.join(list(map(str,i))),2)
	print(x)
	f.append(x.to_bytes(1,byteorder='big'))
exit()
f = f[:idx]
fout = open("XD",'wb')
for b in f:
	print(b)
	fout.write(b)
print(f)