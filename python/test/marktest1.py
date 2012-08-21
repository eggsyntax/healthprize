# This is the example from http://unmarkedegg.pbworks.com/w/page/38869923/How-to-make-predictions-with-the-DSL

import sys
print sys.path
sys.path.append('/Users/egg/Documents/Programming/healthprize/python')

from domain.data import *
	#(don't worry about why yet, but this line should be at the top of every program you write)

members = Members()
	#(members (an arbitrary name, coulda been 'patients' or 'm' or whatever) now contains all the members in the training data set)

members.where("memberid < 300000")

	#(constrains members to the subset of members with low member ids).
	#(an alternate syntax for the two lines above would have been this:)
	#    members = (Members()
	#	    .where("memberid < 100000")
	#		)

	#(You can chain those where clauses at will)

def predictYoungMenSuffer(member):

	#(Now we're creating our algorithm to actually make a prediction. This algorithm will be run on each member in a group.
	#(This is the section that later will become much more complex, but for now let's make a very simple prediction that young
	#(males will go into the hospital and everyone else will be fine (maybe it's the time of Herod or something) ).

	if member["ageatfirstclaim"] < 20 and member["sex"] == "M":
		return 10
	else:
		return 0

	#(Boom, that's it, a complete prediction algorithm! Let's run it against the members we grabbed earlier and see how it does.

print "Score is",members.makeprediction(predictYoungMenSuffer)

	#Doesn't do too well, mind you.


	#Next steps: you can start to include claims data in your prediction algorithm as well:

def predictLabsKillPeople(member):
	claims = (Claims()
		.formember(member)
				)
	specialties = [claim["specialty"] for claim in claims]

		#This is Python's *amazing* list comprehension syntax, see http://www.secnetix.de/olli/Python/list_comprehensions.hawk

	if any(specialty == "Laboratory" for specialty in specialties):
		return 5
	else:
		return 0

print "Score is",members.makeprediction(predictLabsKillPeople)
	
	#Not too bad, huh?
