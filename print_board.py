#!/usr/bin/env python
from sys import argv
try:p=int(argv[1])
except:p=0
if p<0:p=63+p
p=p%64
for y in xrange(8):print" ".join(format(y*8+x-p,"3d")for x in xrange(8)),"\n"
