
import pandas as pd
import numpy as np


def get_data():
    votes = []
    data = pd.read_csv('00016-00000001.dat', sep='\t', header=None, index_col=False)
    for i in range(len(data)):
        pref = data.iloc[i,0]
        pref = pref.split(': ')
        pref[0] = int(pref[0])
        pref[1] = pref[1].replace('{', '{,').replace('}', ',}')
        pref[1] = [int(x) if not any(b in x for b in ['{','}']) else x for x in pref[1].split(',')]
        votes.append(pref)
    return votes


def plurality(profile, alternatives):
    plur_score = {alternative: 0 for alternative in alternatives}
    for i in range(len(profile)):
        factor = profile[i][0]
        max_pref = profile[i][1][0]
        if not isinstance(max_pref, int):
            set_end = profile[i][1].index('}')
            if set_end > 3:
                print(f"Warning: tie set of size {set_end-1} found")
                print(f"This case is not properly handled. Weight for all tied preferences is 1/2.")
            for j in range(1, set_end):
                plur_score[profile[i][1][j]] += float(factor * (1/2))
        else:
            plur_score[max_pref] += factor
    print(f"{plur_score=}")
    return plur_score


def remove_alternatives(profile, to_remove):
    for i in range(len(profile)):
        profile[i][1] = [x for x in profile[i][1] if x not in to_remove]
        if profile[i][1]:
            profile[i][1] = [x for j, x in enumerate(profile[i][1]) if not (x == '{' and profile[i][1][j+1] == '}')]
    return [x for x in profile if x[1]]


def sigma(profile, alternatives):
    plur_score = plurality(profile, alternatives)
    lowest_plur_score = min(plur_score.values())
    to_remove = [alternative for alternative in plur_score if plur_score[alternative] == lowest_plur_score]
    print(f"{to_remove=}, with {lowest_plur_score=}")

    alternatives = [x for x in plur_score if x not in to_remove]
    print(f"Subset of {alternatives=}")

    if not alternatives:
        return plur_score

    profile = remove_alternatives(profile, to_remove)
    return sigma(profile, alternatives) 


def STV(profile, alternatives):
    return sigma(profile, alternatives)


def manipulate_election(profile, dropped_vote, first_vote):
    votes = [item[1] for item in profile]
    votes = drop_vote(votes, dropped_vote, first_vote)
    for item, vote in zip(profile, votes):
        item[1] = vote
    return profile

def drop_vote(profile, dropped_vote, first_vote):
    manipulated_votes = []
    for preference in profile:
        if (dropped_vote in preference) and (first_vote in preference):
            if preference.index(dropped_vote) > preference.index(first_vote):
                preference.pop(preference.index(dropped_vote))
                preference.insert(0, preference.pop(preference.index(first_vote)))
                manipulated_votes.append(preference)
            else:
                manipulated_votes.append(preference)
        elif first_vote in preference:
            preference.insert(0, preference.pop(preference.index(first_vote)))
            manipulated_votes.append(preference)
        else: 
            manipulated_votes.append(preference)
    return manipulated_votes


def main():
    profile = get_data()
    alternatives = [x for x in range(1, 12)]
    rigged_profile = manipulate_election(profile,8,2)
    plur_score = STV(rigged_profile, alternatives)
    print(f"Winning alternative is {plur_score}.")


if __name__ == "__main__":
    main()