"""Find Smallest Letter Greater Than Target on 10^4 sorted letters with long runs, the target
often at or past the last letter so the answer wraps around."""

SEEDS = 3
N = 10**4


def generate(rng):
    alphabet = sorted(rng.sample("abcdefghijklmnopqrstuvwxyz", rng.randint(2, 26)))
    letters = [rng.choice(alphabet) for _ in range(N - 2)]
    letters = sorted([*letters, alphabet[0], alphabet[-1]])
    target = rng.choice([letters[-1], "z", rng.choice("abcdefghijklmnopqrstuvwxyz")])
    return {"letters": letters, "target": target}
