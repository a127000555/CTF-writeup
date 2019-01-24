#!/usr/bin/python -u

import random,string
random.seed("random")
'''
flag = "FLAG:"+open("flag", "r").read()[:-1]
encflag = ""
for c in flag:
  if c.islower():
    #rotate number around alphabet a random amount
    encflag += chr((ord(c)-ord('a')+random.randrange(0,26))%26 + ord('a'))
  elif c.isupper():
    encflag += chr((ord(c)-ord('A')+random.randrange(0,26))%26 + ord('A'))
  elif c.isdigit():
    encflag += chr((ord(c)-ord('0')+random.randrange(0,10))%10 + ord('0'))
  else:
    encflag += c
print "Unguessably Randomized Flag: "+encflag
'''

# Unguessably Randomized Flag: BNZQ:KLRXRNLXL{1_W8FF0Y_t0ic7l9_m5p_ruKo_vbjUOH}
s = 'BNZQ:KLRXRNLXL{1_W8FF0Y_t0ic7l9_m5p_ruKo_vbjUOH}'
# s = 'FLAG:BAMBOOFOX{'
decflag = ""
for c in s:
  if c.islower():
    #rotate number around alphabet a random amount
    decflag += chr((ord(c)-ord('a')-random.randrange(0,26))%26 + ord('a'))
  elif c.isupper():
    decflag += chr((ord(c)-ord('A')-random.randrange(0,26))%26 + ord('A'))
  elif c.isdigit():
    decflag += chr((ord(c)-ord('0')-random.randrange(0,10))%10 + ord('0'))
  else:
    decflag += c
print(decflag)
# python2 