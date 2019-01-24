import requests
search = ['index','joinus','team','blog','register','login']
base_url = 'http://final.kaibro.tw:10004/'

for s in search:
	suffix = s + '.php'
	print(base_url+suffix)
	print(requests.get(base_url + suffix))
	suffix = s + '.php~'
	print(base_url+suffix)
	print(requests.get(base_url + suffix))
	suffix = '.' + s  + '.php.swp' 
	print(base_url+suffix)
	print(requests.get(base_url + suffix))
	suffix = '.' + s  + '.php' 
	print(base_url+suffix)
	print(requests.get(base_url + suffix))

	
