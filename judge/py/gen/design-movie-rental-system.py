"""Design Movie Rental System with 10^5 entries (one movie in 5 * 10^4 shops) and 10^5 calls:
3 * 10^4 rentals first, then searches and reports among more rentals and drops, so sorting or
taking the five smallest of the rented set or a movie's shops per query is ~10^4 queries of
~3 * 10^4 entries each."""

SEEDS = 2
SHOPS = 10**5
ENTRIES = 10**5
POPULAR = 5 * 10**4
CALLS = 10**5
RENTED = 3 * 10**4


def generate(rng):
    hot = rng.randint(1, 10**4)
    pairs = {(shop, hot) for shop in rng.sample(range(SHOPS), POPULAR)}
    while len(pairs) < ENTRIES:
        pairs.add((rng.randrange(SHOPS), rng.randint(1, 10**4)))
    pairs = sorted(pairs)
    rng.shuffle(pairs)
    entries = [[shop, movie, rng.randint(1, 10**4)] for shop, movie in pairs]
    ops, args = ["MovieRentingSystem"], [[SHOPS, entries]]
    free, rented = list(pairs), []

    def move(src, dst):
        j = rng.randrange(len(src))
        src[j], src[-1] = src[-1], src[j]
        dst.append(src.pop())
        return list(dst[-1])

    for _ in range(RENTED):
        ops.append("rent")
        args.append(move(free, rented))
    while len(ops) <= CALLS:
        r = rng.random()
        if r < 0.4:
            ops.append("report")
            args.append([])
        elif r < 0.7:
            ops.append("search")
            args.append([hot if rng.random() < 0.7 else rng.choice(pairs)[1]])
        elif r < 0.85 and free:
            ops.append("rent")
            args.append(move(free, rented))
        elif rented:
            ops.append("drop")
            args.append(move(rented, free))
    return {"ops": ops, "args": args}
