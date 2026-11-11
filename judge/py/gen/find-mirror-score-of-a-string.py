"""Find Mirror Score of a String at length 2 * 10^4: a run of a-m letters, then their mirrors
in the same order, so every match spans a long gap and scanning left for it is quadratic."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    half = N // 2
    head = [chr(97 + rng.randrange(13)) for _ in range(half)]
    tail = [chr(219 - ord(c)) for c in head]
    # a few random letters break the full matching, so the answer differs per seed
    for _ in range(N // 100):
        tail[rng.randrange(half)] = chr(97 + rng.randrange(26))
    return {"s": "".join(head + tail)}
