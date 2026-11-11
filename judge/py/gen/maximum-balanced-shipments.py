"""Maximum Balanced Shipments at n = 2 * 10^4: rising weights with a dip every few hundred
parcels, so a DP that looks back for the last split runs past long unbalanced stretches,
~2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**9


def generate(rng):
    weight, w = [], 1
    for _ in range(N):
        if rng.random() < 0.004:
            weight.append(rng.randint(1, w))
        else:
            w += rng.randint(1, LIMIT // N // 2)
            weight.append(w)
    return {"weight": weight}
