'''
Created on Apr 9, 2011

@author: egg
'''

divisors = range(2,21)
n = 9699690
while(1):
    remainders = [n%i for i in divisors]
    if any(remainders):
        if not n%100000: print n
        n += 9699690
    else:
        print n
        break

