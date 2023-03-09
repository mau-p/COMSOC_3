
from stv import plurality, get_data


def get_choice(pref):
    try:
        return pref.pop(0)
    except IndexError:
        return None


def get_totals(totals, plur_score):
    for key, value in plur_score.items():
        totals[key] += value
    return totals


def profile_ranking(profile, alternatives):
    totals = {x: 0 for x in alternatives}
    for i in range(10):
        plur_score = plurality(profile, alternatives)
        totals = get_totals(totals, plur_score)
        print(f"At rank {i+1}, {plur_score=}")
        for x in profile:
            popped = x[1].pop(0)
            if not isinstance(popped, int):
                while popped != '}':
                    popped = x[1].pop(0)
        profile = [x for x in profile if x[1]]
    print(f"{totals=}")
    return


def main():
    profile = get_data()
    alternatives = [x for x in range(1, 12)]
    profile_ranking(profile, alternatives)


if __name__ == "__main__":
    main()