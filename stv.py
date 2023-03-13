
from preflibtools.instances import OrdinalInstance
from profile_overview import data_overview
from copy import deepcopy


def get_data():
    '''
    Returns profile and alternatives from .toi file.
    We make list of the order tuples together with their multiplicity, for easier removal later on.
    '''
    instance = OrdinalInstance()
    instance.parse_url('https://www.preflib.org/static/data/aspen/00016-00000001.toi')
    profile = [[instance.multiplicity[order], list(order)] for order in instance.orders]        # Make list of multiplicity and order
    alternatives = [(x,) for x in instance.alternatives_name.keys()]        # Make list of alternatives as tuples (for consistency with other functions)
    return profile, alternatives


def clean_pref(pref, to_remove):
    '''
    Removes all alternatives that are marked for removal from the preference order of the current voter.
    '''
    pref[1] = [x for x in pref[1] if x not in to_remove]   # Remove all alternatives that are marked for removal
    ties = [x for x in pref[1] if len(x) > 1]       # Find all ties
    remove_votes = list(sum(to_remove, ()))         # Flatten list of tuples
    for tie in ties:
        idx = pref[1].index(tie)
        tie = tuple(x for x in tie if x and x not in remove_votes)  # Remove all alternatives that are None or marked for removal
        if len(tie) == 1:
            tie = (tie[0], None)            # If there is only one alternative left, add a None to make it a tuple (to keep plurality scores for ties)
        pref[1][idx] = tie
    pref[1] = [x for x in pref[1] if x]     # Remove all empty tuples
    return pref


def remove_alternatives(profile, to_remove):
    '''
    Removes all alternatives that are marked for removal from the profile.
    '''
    for pref in profile:
        pref = clean_pref(pref, to_remove)
    return [x for x in profile if x[1]]


def plurality(profile, alternatives):
    '''
    Calculate plurality scores for all alternatives.
    '''
    plur_score = {alternative: 0 for alternative in alternatives}
    for pref in profile:
        max_pref = pref[1][0]
        if len(max_pref) == 1:
            plur_score[max_pref] += pref[0]
        elif len(max_pref) > 1:
            for x in max_pref:
                if x:    # If x is not None
                    plur_score[(x,)] += float(pref[0]*(1/2))
    print(f"{plur_score=}")
    return plur_score


def STV(profile, alternatives):
    '''
    Calculates the winner of the election using the Single Transferable Vote method.
    Implemented with recursion.
    '''
    plur_score = plurality(profile, alternatives)
    lowest_plur_score = min(plur_score.values())
    to_remove = [alternative for alternative in plur_score if plur_score[alternative] == lowest_plur_score]
    print(f"{to_remove=}, with {lowest_plur_score=}")

    alternatives = [x for x in plur_score if x not in to_remove]
    print(f"Subset of {alternatives=}")

    if not alternatives:
        return plur_score

    profile = remove_alternatives(profile, to_remove)
    return STV(profile, alternatives)


def main():
    profile, alternatives = get_data()
    # Dataframe with rows as alternatives and columns as preference ranks
    initial_counts = data_overview(profile, alternatives)
    plur_score = STV(deepcopy(profile), alternatives)
    print(f"Winning alternative is {plur_score}.")
    winner, = max(plur_score, key=plur_score.get)
    # Dataframe with rows as alternatives and columns as preference ranks, counting only votes preferred over the winner or not containing the winner
    pref_over_winner = data_overview(profile, alternatives, winner)
    comparison = initial_counts.compare(pref_over_winner, keep_shape=True, keep_equal=True)
    print(comparison)


if __name__ == "__main__":
    main()