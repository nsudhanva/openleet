"""Compare Version Numbers at length 500: ~100 revisions with leading zeros that compare equal
until a difference at the very end, or trailing zero revisions on one side only."""

SEEDS = 3


def generate(rng):
    def render(revs):
        return ".".join("0" * rng.randint(0, 2) + str(v) for v in revs)

    revs = [rng.randint(0, 99) for _ in range(rng.randint(60, 90))]
    shape = rng.choice(["equal-zeros", "last", "random"])
    if shape == "equal-zeros":
        a, b = revs, [*revs, *[0] * rng.randint(1, 30)]
    elif shape == "last":
        last = revs[-1] + rng.choice([1, -1]) if revs[-1] else 1
        a, b = revs, [*revs[:-1], last]
    else:
        a = revs
        b = [rng.randint(0, 2**31 - 1) for _ in range(rng.randint(1, 30))]
    v1, v2 = render(a), render(b)
    v1, v2 = v1[:500].rstrip("."), v2[:500].rstrip(".")
    return (
        {"version1": v1, "version2": v2} if rng.random() < 0.5 else {"version1": v2, "version2": v1}
    )
