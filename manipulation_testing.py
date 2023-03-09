
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
    alt_before_8 = {x: 0 for x in alternatives}
    for x in profile:
        try:
            idx = x[1].index(8)
            for i in range(idx):
                if not isinstance(x[1][i], int):
                    set_end = x[1].index('}')
                    if set_end < idx:
                        for j in range(i+1, set_end):
                            alt_before_8[x[1][j]] += x[0] * (1/2)
                    else:
                        for j in range(i+1, idx):
                            alt_before_8[x[1][j]] += x[0] * (1/2)
                else:
                    alt_before_8[x[1][i]] += x[0]
        except ValueError:
            continue
    print(f"{alt_before_8=}")
    totals = {x: 0 for x in alternatives}
    count = 0
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
    print(f"{count=}")
    return


def main():
    profile = get_data()
    alternatives = [x for x in range(1, 12)]
    profile_ranking(profile, alternatives)


if __name__ == "__main__":
    main()