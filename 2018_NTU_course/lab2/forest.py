command = 'DLLDLDLLLLLDLLLLRLDLLDLDLLLRRDLLLLRDLLLLLDLLRLRRRDLLLDLLLDLLLLLDLLRDLLLRRLDLLLDLLLLLDLLLRLDLLDLLRLRRDLLLDLLRLRRRDLLRDLLLLLDLLLRLDLLDLLRLRRDLLLLLDLLRDLLLRRLDLLLDLLLLLDLLRDLLRLRRDLLLDLLLDLLRLRRRDLLLLLDLLLLRLDLLLRRLRRDDLLLRRDLLLRRLRDLLLRLDLRRDDLLLRLDLLLRRRDLLRLRRRDLRRLD'
charset = "yuoteavpxqgrlsdhwfjkzi_cmbn"

tree_dict = { 'val' : charset[0] }
charset = charset[1:]


for c in charset:
	now_tree = tree_dict
	while True:
		if c > now_tree['val']:
			if "right" not in now_tree:
				now_tree["right"] = { 'val' : c }
				break
			else:
				now_tree = now_tree["right"]
		else:
			if "left" not in now_tree:
				now_tree["left"] = { 'val' : c }
				break
			else:
				now_tree = now_tree["left"]
path_set = command.split('D')[:-1]
ans = ""
for path in path_set:
	now_tree = tree_dict
	for c in path:
		if c=='L':
			now_tree = now_tree['left']
		else:
			now_tree = now_tree['right']
	ans += now_tree['val']
	print(now_tree['val'], path)

print('flag{' + ans + '}')
# print(path_set)
# print(tree_dict)