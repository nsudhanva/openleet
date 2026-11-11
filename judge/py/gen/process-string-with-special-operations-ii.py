"""Process String with Special Operations II at the maximum 10^5 characters ending in ~33 '#'
doublings that grow the result to ~10^14 characters, so building the string explodes where
walking the operations backward is O(n)."""

SEEDS = 2
N = 10**5
TAIL = 10**4
HASHES = 45
CAP = 4 * 10**14


def generate(rng):
    s, m = [], 0
    hashes = set(rng.sample(range(N - TAIL, N), HASHES))
    for i in range(N):
        if i in hashes and 0 < 2 * m <= CAP:
            c = "#"
            m *= 2
        else:
            r = rng.random()
            if r < 0.6:
                c = rng.choice("abcdefghijklmnopqrstuvwxyz")
                m += 1
            elif r < 0.8:
                c = "*"
                m = max(0, m - 1)
            else:
                c = "%"
        s.append(c)
    return {"s": "".join(s), "k": rng.randrange(m)}
