from domain.data import *

# Comment out the where clause to run on the full dataset
members = Members().where("id < 100") 

totaldaysin = sum([member["daysin"] for member in members])
nummembers = len(members)
average = float(totaldaysin) / nummembers # "float" just tells it not to do integer division
print "Average days in hospital:",average

# I wrote the above to show you the mechanics. But actually there's a handier way; I've set it
# up so that every subset of members actually knows how long it's been in. So you can just do:
print "Average days in hospital:",members.avedaysin()

# Hmm. Actually, I'd like to set up a much simpler way to go about this. Do realize that nothing
# is set in stone yet, it's all so new. But here's a stab at it:
membersWhoHaveSeenAPediatrician = [] # an empty list
for member in members:
	claims = Claims().formember(member)
	specialtylist = [claim["specialty"] for claim in claims]
	if any(specialty == "Pediatrics" for specialty in specialtylist):
		membersWhoHaveSeenAPediatrician.append(member)
		
totaldaysin = sum(member["daysin"] for member in membersWhoHaveSeenAPediatrician)
average = float(totaldaysin) / len(membersWhoHaveSeenAPediatrician)
print "Average days in for members who have seen a pediatrician:",average

print

# OK, done. But you know, this is the kind of thing that programmers love to generalize, so
# let's do it again but turn it into a function. Takes as input a group of members and a specialty.
# Notice there's almost nothing at all new here.
def averageDaysInForSpecialty(members,specialty):
	membersWhoHaveSeenThisSpecialty = [] # an empty list
	for member in members:
		claims = Claims().formember(member)
		specialtylist = [claim["specialty"] for claim in claims]
		if any(s == specialty for s in specialtylist):
			membersWhoHaveSeenThisSpecialty.append(member)
			
	totaldaysin = sum(member["daysin"] for member in membersWhoHaveSeenThisSpecialty)
	average = float(totaldaysin) / len(membersWhoHaveSeenThisSpecialty)
	return "Average days in for members who have seen a specialist in "+specialty+": "+str(average)

# Now we can run it for different specialties and/or different groups of members!
print averageDaysInForSpecialty(members, "Pediatrics")
print averageDaysInForSpecialty(members, "Internal")
print averageDaysInForSpecialty(members, "Surgery")

