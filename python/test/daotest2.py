from domain.data import *

''' To make a prediction about a set of members (can be the whole set, but doesn't have
    to be), define a function which takes a member and returns a number.
'''

members = (Members()
    .where("memberid < 100000")
    )

def predict1(d):
    return 1.5

def predict2(d):
    return 15

def predict3(d):
    ''' Magic perfect function, aka it cheats '''
    return d["daysin"]

def predict4(d):
    ''' All old people will be hospitalized for two weeks; everyone else is fine '''
    if d["ageatfirstclaim"] >= 60:
        return 14
    else:
        return 0

def predict5(d):
    return 0

def makeConstantFunction(k):
    ''' This creates a function which returns a constant. It could have been
        used to create predict1 or predict2 above. Marko -- ignore this, it
        gets into some fancy functional programming. I'm using it below to 
        figure out what constant would get the best score for the dataset.
    '''
    fn = lambda d: k # Anonymous function that ignores d and returns k
    return fn

print "Predicts 1.5 for all members:", members.makeprediction(predict1)
print "Predicts 15 for all members:",  members.makeprediction(predict2)
print "Perfect (predicts 'daysin' for all members):",members.makeprediction(predict3)
print "Not bad for this dataset (predicts 15 if age 60+, else 0):",members.makeprediction(predict4)
print "Predicts 0 for all members (notice how well this does):",  members.makeprediction(predict5)

members = (Members()
    .where("id <= 10000")
    )

print "Average days in:",members.avedaysin(),"for",len(members),"members"

for i in range(20):
    k = i/20.0
    print k, members.makeprediction(makeConstantFunction(k))

def functionWhichPredicts0Correctly(d):
    ''' This is a 'magic' function, ie it looks at the actual value of days in (which of course
        any real algorithm shouldn't do) and predicts 0 correctly in all cases, and predicts
        1 for all patients who have spent any time in hospital.
    '''
    if d["daysin"] == 0: return 0
    return 1

print "Another magic function:",members.makeprediction(functionWhichPredicts0Correctly)


