"""Number of Ways to Split a String at 3 * 10^4 characters, all 0s or a multiple of three 1s spread
thinly, so trying every pair of cut points costs 4.5 * 10^8 steps."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    if rng.random() < 0.5:
        return {"s": "0" * N}
    s = ["0"] * N
    for i in rng.sample(range(N), 3 * rng.randint(1, 30)):
        s[i] = "1"
    return {"s": "".join(s)}
