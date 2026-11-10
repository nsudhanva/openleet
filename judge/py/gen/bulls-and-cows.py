"""Bulls and Cows at length 1000: random digits, or a guess that is a near-permutation of the
secret so cows dominate."""

SEEDS = 2
N = 1000


def generate(rng):
    secret = [rng.choice("0123456789") for _ in range(N)]
    if rng.random() < 0.5:
        guess = [rng.choice("0123456789") for _ in range(N)]
    else:
        guess = list(secret)
        rng.shuffle(guess)
    return {"secret": "".join(secret), "guess": "".join(guess)}
