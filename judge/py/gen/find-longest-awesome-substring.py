"""Find Longest Awesome Substring at length 5 * 10^4: two halves over eight digits joined by the
other two digits, so no awesome substring spans both halves and checking substrings, all of them
or longest first, is over 2 * 10^8 steps."""

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    digits = list("0123456789")
    rng.shuffle(digits)
    p, q, rest = digits[0], digits[1], digits[2:]
    # Prefix parities of p and q are 00 in the first half and 11 in the second: two bits apart.
    left = rng.randint(N // 3, 2 * N // 3)
    s = [rng.choice(rest) for _ in range(left)] + [p, q]
    s += [rng.choice(rest) for _ in range(N - len(s))]
    return {"s": "".join(s)}
