"""word of ~5 * 10^5 letters in ~280 runs of 1500 to 2000, with k near 2000, so a DP that sums
each run's choices one by one costs ~5 * 10^8 steps."""

SEEDS = 2
N = 5 * 10**5
ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    k = rng.randint(1900, 2000)
    parts, total, last = [], 0, ""
    while True:
        run = rng.randint(1500, 2000)
        if total + run > N:
            break
        c = rng.choice(ALPHABET)
        while c == last:
            c = rng.choice(ALPHABET)
        parts.append(c * run)
        total += run
        last = c
    return {"word": "".join(parts), "k": k}
