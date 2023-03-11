
from preflibtools.instances import OrdinalInstance
from profile_overview import data_overview
from copy import deepcopy


def get_data():
    instance = OrdinalInstance()
    instance.parse_file('00016-00000001.toi')
    profile = [[instance.multiplicity[order], list(order)] for order in instance.orders]    # Make list of multiplicity and order
    alternatives = [(x,) for x in instance.alternatives_name.keys()]   # Make list of alternatives as tuples (for consistency with other functions)
    return profile, alternatives


def clean_pref(pref, to_remove):
    pref[1] = [x for x in pref[1] if x not in to_remove]   # Remove all alternatives that are marked for removal
    ties = [x for x in pref[1] if len(x) > 1]       # Find all ties
    remove_votes = list(sum(to_remove, ()))     # Flatten list of tuples
    for tie in ties:
        idx = pref[1].index(tie)
        tie = tuple(x for x in tie if x and x not in remove_votes)  # Remove all alternatives that are None or marked for removal
        if len(tie) == 1:
            tie = (tie[0], None)            # If there is only one alternative left, add a None to make it a tuple (to keep plurality scores for ties)
        pref[1][idx] = tie
    pref[1] = [x for x in pref[1] if x]
    return pref


def remove_alternatives(profile, to_remove):
    for pref in profile:
        pref = clean_pref(pref, to_remove)
    return [x for x in profile if x[1]]


def plurality(profile, alternatives):
    plur_score = {alternative: 0 for alternative in alternatives}
    for pref in profile:
        max_pref = pref[1][0]
        if len(max_pref) == 1:
            plur_score[max_pref] += pref[0]
        elif len(max_pref) > 1:
            for x in max_pref:
                if x:
                    plur_score[(x,)] += float(pref[0]*(1/2))
    print(f"{plur_score=}")
    return plur_score


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


def main():
    profile, alternatives = get_data()
    data_overview(profile, alternatives)
    plur_score = STV(deepcopy(profile), alternatives)
    print(f"Winning alternative is {plur_score}.")
    winner, = max(plur_score, key=plur_score.get)
    data_overview(profile, alternatives, winner)


if __name__ == "__main__":
    main()