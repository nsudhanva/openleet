"""Find Substring With Given Hash Value at length 10^4 with k near n / 2 and the only matching
window last, so hashing each window from scratch is ~2.5 * 10^7 steps."""

SEEDS = 2
N = 10**4


def generate(rng):
    while True:
        k = rng.randint(N * 2 // 5, N * 3 // 5)
        modulo = rng.randint(5 * 10**8, 10**9)
        power = rng.randint(2, modulo - 1)
        s = "".join(chr(97 + rng.randrange(26)) for _ in range(N))
        vals = [ord(c) - 96 for c in s]
        # Hash every window right to left, as hash(s[i:i+k]) = sum(val(s[i+j]) * power^j).
        top = pow(power, k - 1, modulo)
        h = 0
        for j in range(N - 1, N - 1 - k, -1):
            h = (h * power + vals[j]) % modulo
        target, unique = h, True
        for i in range(N - k - 1, -1, -1):
            h = ((h - vals[i + k] * top) * power + vals[i]) % modulo
            if h == target:
                unique = False
                break
        if unique:
            return {"s": s, "power": power, "modulo": modulo, "k": k, "hashValue": target}
