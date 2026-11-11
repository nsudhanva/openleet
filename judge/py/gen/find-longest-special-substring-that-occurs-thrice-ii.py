"""Find Longest Special Substring That Occurs Thrice II at length ~3.7 * 10^5: three runs of one
letter ~6 * 10^4 long among 6 * 10^4 short runs of that same letter and 10^4 of others, so trying
each length in turn over the runs (even only that letter's runs) is ~4 * 10^9 steps."""

SEEDS = 2
LONG = 6 * 10**4
SHORT = 6 * 10**4
OTHER = 10**4


def generate(rng):
    letters = list("abcdefghijklmnopqrstuvwxyz")
    rng.shuffle(letters)
    star, other = letters[0], letters[1:]
    pieces = [star * rng.randint(LONG - LONG // 15, LONG) for _ in range(3)]
    pieces += [star * rng.randint(1, 3) for _ in range(SHORT)]
    pieces += [rng.choice(other) * rng.randint(1, 3) for _ in range(OTHER)]
    rng.shuffle(pieces)
    # Adjacent pieces of one letter would merge into a longer run; split them with another letter.
    s = []
    for p in pieces:
        if s and s[-1][-1] == p[0]:
            s.append(next(c for c in other if c != p[0]))
        s.append(p)
    return {"s": "".join(s)}
