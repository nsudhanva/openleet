"""Naming a Company at 10^4 ideas built as a first letter on a shared pool of suffixes (so many
swaps collide), so testing every ordered pair of ideas is ~10^8 steps."""

SEEDS = 2
N = 10**4
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    suffixes = set()
    while len(suffixes) < N // 2:
        suffixes.add("".join(rng.choice(LETTERS) for _ in range(rng.randint(0, 9))))
    suffixes = sorted(suffixes)
    ideas = set()
    while len(ideas) < N:
        ideas.add(rng.choice(LETTERS) + rng.choice(suffixes))
    ideas = sorted(ideas)
    rng.shuffle(ideas)
    return {"ideas": ideas}
