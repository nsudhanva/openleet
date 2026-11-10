"""Buddy Strings at length 2 * 10^4: equal strings, strings differing at exactly two far-apart
positions (swappable or not), or at three positions."""

SEEDS = 3
N = 2 * 10**4


def generate(rng):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    s = [rng.choice(alphabet) for _ in range(N)]
    goal = list(s)
    shape = rng.choice(["equal", "swap", "two", "three"])
    if shape == "swap":
        i, j = rng.randrange(N // 10), rng.randrange(N - N // 10, N)
        while s[i] == s[j]:
            s[j] = rng.choice(alphabet)
            goal[j] = s[j]
        goal[i], goal[j] = s[j], s[i]
    elif shape in ("two", "three"):
        for i in rng.sample(range(N), 2 if shape == "two" else 3):
            goal[i] = rng.choice([c for c in alphabet if c != s[i]])
    return {"s": "".join(s), "goal": "".join(goal)}
