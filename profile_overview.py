
import pandas as pd

def find_elem(lst, elem):
    for x in lst:
        if elem in x:
            return lst.index(x)
    return None


def data_overview(profile, alternatives, winner=None):
    overview = pd.DataFrame(columns=[x for x in range(1,11)], index=[x for (x,) in alternatives])
    overview = overview.fillna(0)
    for voter in profile:
        if winner:
            idx_winner = find_elem(voter[1], winner)
        else:
            idx_winner = None
        for pref in voter[1]:
            if idx_winner and voter[1].index(pref) > idx_winner:
                continue
            idx = voter[1].index(pref)+1
            if len(pref) > 1:
                for x in pref:
                    overview.loc[x, idx] += float(voter[0]*(1/2))
            else:
                overview.loc[pref[0], idx] += voter[0]
    overview['total'] = overview.sum(axis=1)
    print(overview)
    return
