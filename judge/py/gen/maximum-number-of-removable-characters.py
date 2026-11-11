"""Maximum Number of Removable Characters with s of 2 * 10^4 letters and p a quarter of it, the
first 7500 removals off p's embedding, so the answer sits mid-list and checking each k in turn
is quadratic."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    s = "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(N))
    keep = sorted(rng.sample(range(N), N // 4))
    p = "".join(s[i] for i in keep)
    kept = set(keep)
    other = [i for i in range(N) if i not in kept]
    rng.shuffle(other)
    head = other[: 3 * N // 8]
    tail = other[3 * N // 8 :] + keep
    rng.shuffle(tail)
    return {"s": s, "p": p, "removable": head + tail[: N // 2]}
