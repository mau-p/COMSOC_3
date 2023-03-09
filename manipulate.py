import numpy as np
import itertools
from stv import get_data

def count_votes(ballots):
	votes = {
		1: 0,
		2: 0,
		3: 0,
		4: 0,
		5: 0,
		6: 0,
		7: 0,
		8: 0,
		9: 0,   
		10: 0,
		11: 0     
	}	
	
	for ballot in ballots:
		for i in range(len(ballot)):
			if ballot[i] != 0:
				votes[ballot[i]] += 1
				break
	return votes

def coalition_manipulation(ballots):
    votes = {
        1: False,
        2: False,
        3: False,
        4: False,
        5: False,
        6: False,
        7: False,
        8: False,
        9: False,   
        10: False,
        11: False     
	}	
    
    C = [x for x in range(1, 12)]
    orders = list(itertools.permutations(C))
    
    for order in orders:
        flag = False
        for i in range(len(order)-1):
            count = count_votes(ballots)
            for j in range(i+1, len(order)):
                while count[order[j]] < count[order[i]]:
                    if not votes[order[j]]:
                        votes[order[j]] = True
                    else:
                        flag = True
                        break
                if flag:
                    break
            if flag:
            	break

# Split the counted ballots into individual ballots
def split_ballots(ballots):
    split = []
    for ballot in ballots:
        for i in range(ballot[0]):
            split.append(ballot[1])
    return split
		
if __name__ == "__main__":
    ballots = get_data()
    ballots = split_ballots(ballots)
    coalition_manipulation(ballots)