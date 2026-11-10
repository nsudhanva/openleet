"""Maximize Active Section with Trade I on binary strings of length 10^5: short alternating
blocks (many trades to try) or long random blocks."""

SEEDS = 3
N = 10**5


def generate(rng):
    shape = rng.choice(["bits", "blocks", "alternating"])
    if shape == "bits":
        s = "".join(rng.choice("01") for _ in range(N))
    elif shape == "alternating":
        s = ("01" * N)[:N] if rng.random() < 0.5 else ("10" * N)[:N]
    else:
        parts, total, bit = [], 0, rng.choice("01")
        while total < N:
            length = min(N - total, rng.randint(1, 2000))
            parts.append(bit * length)
            total += length
            bit = "1" if bit == "0" else "0"
        s = "".join(parts)
    return {"s": s}
