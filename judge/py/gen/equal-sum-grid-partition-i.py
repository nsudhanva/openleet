"""Equal Sum Grid Partition I on a 1 x 10^5 or 10^5 x 1 grid with an even total but no equal
cut, so re-summing both sides for each of the 10^5 cuts is ~10^10 additions."""

SEEDS = 2
N = 10**5


def generate(rng):
    while True:
        vals = [rng.randint(1, 10**5) for _ in range(N)]
        if sum(vals) % 2:
            vals[0] += 1 if vals[0] < 10**5 else -1
        total, prefix = sum(vals), 0
        for v in vals[:-1]:
            prefix += v
            if 2 * prefix == total:
                break
        else:
            break
    grid = [vals] if rng.random() < 0.5 else [[v] for v in vals]
    return {"grid": grid}
