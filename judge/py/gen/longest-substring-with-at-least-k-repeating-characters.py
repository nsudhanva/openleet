"""Longest Substring With At Least K Repeating Characters at length 10^4: many rare letters
splitting the string often, or a k above the length (answer 0)."""

SEEDS = 3
N = 10**4
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    shape = rng.choice(["split", "dense", "huge-k"])
    if shape == "split":
        chars = [rng.choice("abcde") for _ in range(N)]
        for i in rng.sample(range(N), 300):
            chars[i] = rng.choice(LETTERS[5:])
        k = rng.randint(2, 30)
    elif shape == "dense":
        chars = [rng.choice(LETTERS) for _ in range(N)]
        k = rng.randint(300, 420)
    else:
        chars = [rng.choice(LETTERS) for _ in range(N)]
        k = rng.randint(N + 1, 10**5)
    return {"s": "".join(chars), "k": k}
