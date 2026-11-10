"""Find Players With Zero or One Losses with 10^5 unique matches among up to 10^5 players."""

SEEDS = 2
M = 10**5


def generate(rng):
    players = rng.choice([500, 10**5])
    seen, matches = set(), []
    while len(matches) < M:
        w = rng.randint(1, players)
        loser = rng.randint(1, players)
        if w != loser and (w, loser) not in seen:
            seen.add((w, loser))
            matches.append([w, loser])
    return {"matches": matches}
