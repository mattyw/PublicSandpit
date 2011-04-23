
def election(voters, votes):
    one = round_one(voters, votes)
    if one != None:
        return one
    else:
     winner = None
     highest = 0
     while winner == None:
         party, party_votes = knockout_round(votes, 1)
         winner = party if party_votes > voters/2 else None
     return winner
     
    


def maximum(votes, preference):
    winner = None
    highest = 0
    for party, party_results in votes.iteritems():
        #print party, party_results
        if party_results[preference] > highest:
            highest = party_results[preference]
            winner = party
            #print winner, highest
    return (winner, highest)

def minimum(votes, preference):
    loser = None
    lowest = 1000000
    for party, party_results in votes.iteritems():
        #print party, party_results
        if party_results[preference] < lowest:
            lowest = party_results[preference]
            loser = party
    return (loser, lowest)

def round_one(voters, votes):
    winner, highest = maximum(votes, 0)
    return winner if highest > voters/2 else None

def total_up(votes, preference):
    total = {}
    for party, voters in votes.iteritems():
        total.update({party: [voters[preference-1] + voters[preference]]})
    return total
        

def knockout_round(votes, preference):
    #eliminate lowest
    loser, lowest = minimum(votes, preference-1)
    del votes[loser]
    total = total_up(votes, preference)
    print total
    winner, highest = maximum(total, 0)
    return winner, highest
        
