"""Check If String Is Transformable With Substring Sort Operations at n = 3 * 10^4: s falls from 9
to 0 with local noise and t sorts long stretches of it, so each digit of t is first found far
into what is left of s and simulating the moves is quadratic; on one seed s ends in 01 and t in
10, which fails only at the last step."""

from _shapes import pick_shape

SEEDS = 3
N = 3 * 10**4


def generate(rng):
    shape = pick_shape(rng)
    s = [rng.randrange(10) for _ in range(N)]
    s.sort(key=lambda d: -d - 3 * rng.random())
    t = s[:]
    for _ in range(rng.randint(3, 8)):
        i = rng.randrange(N // 2)
        j = rng.randrange(i + N // 4, N - 1)
        t[i:j] = sorted(t[i:j])
    if shape == 2:
        # The 1 would have to pass the smaller 0 before it, which no sort can do.
        s[-2:], t[-2:] = [0, 1], [1, 0]
    return {"s": "".join(map(str, s)), "t": "".join(map(str, t))}
