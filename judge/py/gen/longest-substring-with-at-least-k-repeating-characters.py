"""Longest Substring With At Least K Repeating Characters at length 10^4: many rare letters
splitting the string often, or a k above the length (answer 0)."""

from string import ascii_lowercase

SEEDS = 3
N = 10**4


def generate(rng):
    shape = rng.choice(["split", "dense", "huge-k"])
    if shape == "split":
        chars = [rng.choice("abcde") for _ in range(N)]
        for i in rng.sample(range(N), 300):
            chars[i] = rng.choice(ascii_lowercase[5:])
        k = rng.randint(2, 30)
    elif shape == "dense":
        chars = [rng.choice(ascii_lowercase) for _ in range(N)]
        k = rng.randint(300, 420)
    else:
        chars = [rng.choice(ascii_lowercase) for _ in range(N)]
        k = rng.randint(N + 1, 10**5)
    return {"s": "".join(chars), "k": k}
