"""Hand of Straights with 10^4 cards: overlapping consecutive runs that split exactly into
groups, or the same hand with one card changed."""

SEEDS = 3
N = 10**4


def generate(rng):
    size = rng.choice([1, 2, 10, 100, 5000])
    groups = N // size
    starts = []
    base = rng.randint(0, 10**9 - 2 * N)
    for _ in range(groups):
        starts.append(base + rng.randint(0, rng.choice([5, 3000])))
    hand = [s + j for s in starts for j in range(size)]
    if size > 1 and rng.random() < 0.34:
        hand[rng.randrange(len(hand))] += 1
    rng.shuffle(hand)
    return {"hand": hand, "groupSize": size}
