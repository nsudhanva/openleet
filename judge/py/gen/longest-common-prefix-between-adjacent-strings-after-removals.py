"""Longest Common Prefix Between Adjacent Strings After Removals with 2 * 10^4 short words where
only one adjacent pair, in the middle, shares a prefix, so rescanning the adjacent prefixes for
every removal costs ~2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    # Adjacent words never share a first letter, except one pair near the middle with a long
    # common prefix: no scan from either end can stop early at the global maximum.
    pair = rng.randint(N // 3, 2 * N // 3)
    longest = "".join(rng.choice("abc") for _ in range(40))
    words = []
    for i in range(N):
        if i == pair:
            words.append(longest)
        elif i == pair + 1:
            words.append(longest[: rng.randint(20, 35)])
        else:
            banned = {words[-1][0]} if words else set()
            if i == pair - 1:
                banned.add(longest[0])
            first = rng.choice([c for c in "abc" if c not in banned])
            words.append(first + "".join(rng.choice("abc") for _ in range(rng.randint(0, 3))))
    return {"words": words}
