
shshi = '🍣'
l = input()
first = True
a = 0
for c in l:
  if first:
    first = False
  else:
    print('&',end='')
  print(shshi + '[]=' + str(ord(c)+a) , end='')
  a+=256
print('')
