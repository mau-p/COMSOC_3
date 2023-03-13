
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
        idx_winner = None
        if winner:
            idx_winner = find_elem(voter[1], winner)
        for pref in voter[1]:
            if idx_winner == 0:
                break
            elif idx_winner != None:
                if voter[1].index(pref) < idx_winner:
                    idx = voter[1].index(pref)+1
                    if len(pref) > 1:
                        for x in pref:
                            if x:
                                overview.loc[x, idx] += float(voter[0]*(1/2))
                    else:
                        overview.loc[pref[0], idx] += voter[0]
            else:
                idx = voter[1].index(pref)+1
                if len(pref) > 1:
                    for x in pref:
                        if x:
                            overview.loc[x, idx] += float(voter[0]*(1/2))
                else:
                    overview.loc[pref[0], idx] += voter[0]
    overview['total'] = overview.sum(axis=1)
    return overview
