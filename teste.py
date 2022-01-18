from sniff import Sniff
import json

f = open('partial_program.txt', 'w')
f.close()

def func(pct):
  f = open('partial_program.txt', 'a')
  f.write(json.dumps(pct) + '\n')
  f.close()

s = Sniff(func)
s.start()
