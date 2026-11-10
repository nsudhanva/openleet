"""Rabbits in Forest at the maximum 1000 answers, with values clustered so groups overflow and
must be split."""

SEEDS = 2


def generate(rng):
    if rng.random() < 0.5:
        answers = [rng.randint(0, 5) for _ in range(1000)]
    else:
        answers = [rng.randint(0, 999) for _ in range(1000)]
    return {"answers": answers}
