
import pandas as pd
import copy


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


def tie_set(voter, plur_score):
    set_end = voter[1].index('}')
    if set_end > 3:
        print(f"Warning: tie set of size {set_end-1} found")
        print(f"This case is not properly handled. Weight for all tied preferences is 1/2.")
    for j in range(1, set_end):
        plur_score[voter[1][j]] += float(voter[0] * (1/2))
    return plur_score


def plurality(profile, alternatives):
    plur_score = {alternative: 0 for alternative in alternatives}
    for voter in profile:
        max_pref = voter[1][0]
        if not isinstance(max_pref, int):
            plur_score = tie_set(voter, plur_score)
        else:
            plur_score[max_pref] += voter[0]
    print(f"{plur_score=}")
    return plur_score


def remove_alternatives(profile, to_remove):
    for voter in profile:
        voter[1] = [x for x in voter[1] if x not in to_remove]
        if voter[1]:
            voter[1] = [x for j, x in enumerate(voter[1]) if not (x == '{' and voter[1][j+1] == '}')]
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


def get_choice(pref):
    try:
        return pref.pop(0)
    except IndexError:
        return None


def profile_ranking(profile, alternatives):
    strict_pref = pd.DataFrame(index=alternatives, columns=alternatives)
    strict_pref = strict_pref.fillna(0)
    potential_manipulators = []
    pref_eight, pref_two = 0, 0
    for pref in profile:
        equal = False
        for vote in pref[1]:
            if vote == '{':
                equal = True
                continue
            elif vote == '}':
                equal = False
                continue
            else:
                if equal:
                    pass
    print(strict_pref)

    for i in range(len(profile)):
        if 8 in profile[i][1] and 2 in profile[i][1]:
            if profile[i][1].index(8) > profile[i][1].index(2):
                pref_two += 1
                potential_manipulators.append(i)
            else:
                pref_eight += 1
    print(f"Prefer 8>2: {pref_eight}. Prefer 2>8: {pref_two}.")
    print(f"{len(potential_manipulators)=}")
    for i in range(10):
        plur_score = plurality(profile, alternatives)
        print(f"At rank {i+1}, {plur_score=}")
        for x in profile:
            popped = x[1].pop(0)
            if not isinstance(popped, int):
                while popped != '}':
                    popped = x[1].pop(0)
        profile = [x for x in profile if x[1]]
    return potential_manipulators


def manipulate_profile(profile, voter):
    print(f"Manipulating voter {voter}.")
    eight_idx = profile[voter][1].index(8)
    two_idx = profile[voter][1].index(2)
    profile[voter][1][eight_idx], profile[voter][1][two_idx] = 2, 8
    return profile


def find_smallers_set_manipulator(profile, alternatives):
    manipulators = profile_ranking(copy.deepcopy(profile), alternatives)
    count = 0
    plur_score = STV(copy.deepcopy(profile), alternatives)
    while not 2 in plur_score.keys():
        diff = max(plur_score.values()) - min(plur_score.values())
        print(f"Diff = {diff}.")
        profile = manipulate_profile(profile, manipulators.pop())
        count += 1
        plur_score = STV(copy.deepcopy(profile), alternatives)
    print(f"Number of manipulations = {count}.")
    return profile


def main():
    profile = get_data()
    alternatives = [x for x in range(1, 12)]
    #profile = find_smallers_set_manipulator(profile, alternatives)
    plur_score = STV(profile, alternatives)
    print(f"Winning alternative is {plur_score}.")


if __name__ == "__main__":
    main()