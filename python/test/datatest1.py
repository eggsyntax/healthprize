'''
Created on Apr 8, 2011

@author: egg
'''
from domain.data import *

print "go"
members = (Members()
    .where("id < 1000")
    )

for m in members:
    claims = (Claims()
              .formember(m)
              )
    s = (m["memberid"],":",len(claims),"claims")


print "\nEvaluated",len(members),"members."

