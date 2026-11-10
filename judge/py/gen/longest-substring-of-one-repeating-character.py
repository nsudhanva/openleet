"""Longest Substring of One Repeating Character with s and the query list both at 10^5,
where recomputing the longest run after each update is quadratic."""

SEEDS = 2
N = 10**5
K = 10**5


def generate(rng):
    alphabet = rng.choice(["ab", "abc"])
    s = alphabet[0] * N if rng.random() < 0.5 else "".join(rng.choice(alphabet) for _ in range(N))
    chars = "".join(rng.choice(alphabet) for _ in range(K))
    indices = [rng.randrange(N) for _ in range(K)]
    return {"s": s, "queryCharacters": chars, "queryIndices": indices}
