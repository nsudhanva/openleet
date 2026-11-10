"""Find the Difference at the maximum length: s of 1000 letters and t a shuffle of s plus one."""

SEEDS = 2


def generate(rng):
    alpha = "abcdefghijklmnopqrstuvwxyz"[: rng.choice([2, 26])]
    s = [rng.choice(alpha) for _ in range(1000)]
    t = [*s, rng.choice(alpha)]
    rng.shuffle(t)
    return {"s": "".join(s), "t": "".join(t)}
