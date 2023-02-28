import pandas as pd

def get_data():
    votes = []
    data = pd.read_csv('00016-00000001.dat', sep='\t', header=None, index_col=False)    
    for i in range(1770):
        vote = data.iloc[i,0]
        vote = vote.split(' ')
        coef = int(vote[0][:-1])
        prefs = vote[1].split(',')
        print(prefs)
        print('\n')
        vote_dict = {'coef': coef, 'prefs': prefs}
        votes.append(vote_dict)

    return votes

get_data()