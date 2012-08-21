from domain.data import *

claims = (Claims()
    .where("memberid = 60481") 
    .where("charlsonindex = '3-4'")
    )

for claim in claims:
    print claim["specialty"]," : ",claim["placesvc"]

members = (Members()
    .where("memberid < 100000")
    )

print members

def predict1(d):
    return 1.5

def predict2(d):
    return 15

def predict3(d):
    return d["daysin"]


print members.makeprediction(predict1)
print members.makeprediction(predict2)
print members.makeprediction(predict3)
