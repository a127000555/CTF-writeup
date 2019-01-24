data = open('some_magic','rb').read()
for i in range(0,len(data),30):
	print(data[i:i+30])