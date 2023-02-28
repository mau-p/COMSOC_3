import pandas as pd

def parse_votes(preference):
    prefs_out = []
    for i in range(len(preference)):
        item = preference[i]
        if item[0] == '{':
            next_item = preference[i+1]
            tie = [int(item[1]), int(next_item[0])]
            prefs_out.append(tie)
        elif len(item) == 1:
            prefs_out.append(int(item))

    return prefs_out


def get_data():
    votes = []
    data = pd.read_csv('00016-00000001.dat', sep='\t', header=None, index_col=False)    
    for i in range(1770):
        vote = data.iloc[i,0]
        vote = vote.split(' ')
        coef = int(vote[0][:-1])
        prefs = vote[1].split(',')
        prefs = parse_votes(prefs)
        vote_dict = {'coef': coef, 'prefs': prefs}
        votes.append(vote_dict)

    return votes

