"""Count Words Obtained After Adding a Letter with 2 * 10^4 start words of 5 letters and 2 * 10^4
target words of 6, a quarter of them reachable, so comparing every target with every start word
costs 4 * 10^8 checks."""

SEEDS = 2
N = 2 * 10**4
LEN = 5


def generate(rng):
    letters = "abcdefghijklmnopqrstuvwxyz"
    start = ["".join(rng.sample(letters, LEN)) for _ in range(N)]
    target = []
    for _ in range(N):
        if rng.random() < 0.25:
            word = rng.choice(start)
            extra = rng.choice([c for c in letters if c not in word])
            chars = [*word, extra]
            rng.shuffle(chars)
            target.append("".join(chars))
        else:
            target.append("".join(rng.sample(letters, LEN + 1)))
    return {"startWords": start, "targetWords": target}
