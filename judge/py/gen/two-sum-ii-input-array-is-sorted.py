"""Two Sum II at n = 3 * 10^4 with exactly one valid pair: every other value is odd and the
target is odd, so only the single even value pairs up; adjacent in the middle or anywhere."""

from _shapes import pick_shape

SEEDS = 3
N = 3 * 10**4


def generate(rng):
    shape = pick_shape(rng)
    while True:
        target = rng.randrange(-999, 1000, 2)  # odd
        if shape == 0:
            # The pair sits next to each other in the middle of the array.
            target = rng.choice([-1, 1])
            a = rng.choice([0, target - 1])
        else:
            a = rng.randrange(-1000, 1001, 2)  # even
        b = target - a  # odd
        if -1000 <= b <= 1000:
            break
    odds = [x for x in range(-999, 1000, 2) if x != b]
    others = [rng.choice(odds) for _ in range(N - 2)]
    numbers = sorted([*others, a, b])
    return {"numbers": numbers, "target": target}
