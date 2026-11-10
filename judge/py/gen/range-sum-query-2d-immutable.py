"""Range Sum Query 2D on a 200 x 200 matrix with 10^4 mostly large regions, so summing each
region directly is too slow."""

SEEDS = 2
SIZE = 200


def generate(rng):
    matrix = [[rng.randint(-(10**4), 10**4) for _ in range(SIZE)] for _ in range(SIZE)]
    ops, args = ["NumMatrix"], [[matrix]]
    for _ in range(10**4):
        r1, r2 = sorted((rng.randrange(SIZE // 4), rng.randrange(SIZE * 3 // 4, SIZE)))
        c1, c2 = sorted((rng.randrange(SIZE // 4), rng.randrange(SIZE * 3 // 4, SIZE)))
        if rng.random() < 0.2:
            r1, r2 = sorted((rng.randrange(SIZE), rng.randrange(SIZE)))
            c1, c2 = sorted((rng.randrange(SIZE), rng.randrange(SIZE)))
        ops.append("sumRegion")
        args.append([r1, c1, r2, c2])
    return {"ops": ops, "args": args}
