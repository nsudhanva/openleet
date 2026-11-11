"""Minimum Cost to Make All Characters Equal on a length-10^5 binary string that changes at about
19 of every 20 positions, so performing each inversion character by character is quadratic."""

SEEDS = 2
N = 10**5


def generate(rng):
    bits = [rng.randint(0, 1)]
    for _ in range(N - 1):
        bits.append(bits[-1] ^ (rng.random() < 0.95))
    return {"s": "".join(map(str, bits))}
