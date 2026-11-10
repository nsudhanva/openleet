"""Count the Number of Consistent Strings with 10^4 words of length 10 and a mid-sized
allowed set, so about half the words need a full scan."""

SEEDS = 2
W = 10**4
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    allowed = "".join(rng.sample(LETTERS, rng.randint(1, 26)))
    words = []
    for _ in range(W):
        if rng.random() < 0.5:
            words.append("".join(rng.choice(allowed) for _ in range(10)))
        else:
            words.append("".join(rng.choice(LETTERS) for _ in range(rng.randint(1, 10))))
    return {"allowed": allowed, "words": words}
