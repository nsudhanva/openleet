"""Minimum Number of People to Teach at the limits (500 languages, 500 users, 500 friendships):
users know 30 languages from one half of the languages and every friendship crosses the halves,
so no friends can talk and re-checking every friendship for each language is ~2 * 10^8 steps."""

SEEDS = 2
LANGS = 500
USERS = 500
FRIENDS = 500
KNOWN = 30


def generate(rng):
    half = LANGS // 2
    side = [i % 2 for i in range(USERS)]
    rng.shuffle(side)
    languages = [rng.sample(range(1 + s * half, 1 + (s + 1) * half), KNOWN) for s in side]
    pairs = set()
    while len(pairs) < FRIENDS:
        u, v = sorted(rng.sample(range(USERS), 2))
        if side[u] != side[v]:
            pairs.add((u + 1, v + 1))
    friendships = [list(p) for p in pairs]
    rng.shuffle(friendships)
    return {"n": LANGS, "languages": languages, "friendships": friendships}
