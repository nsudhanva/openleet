"""Distant Barcodes at n = 10^4 with ~5000 distinct codes (in half the seeds one more code fills
every other slot), so a greedy that scans every code's count per position is ~5 * 10^7 steps."""

SEEDS = 2
N = 10**4


def generate(rng):
    codes = rng.sample(range(1, 10**4 + 1), N // 2 + 1)
    # Half the seeds give one code every other slot; the rest are pairs.
    dominant = rng.random() < 0.5
    barcodes = [codes[0]] * (N // 2) + codes[1:] if dominant else codes[1:] * 2
    rng.shuffle(barcodes)
    return {"barcodes": barcodes[:N]}
