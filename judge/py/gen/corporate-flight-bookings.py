"""Corporate Flight Bookings with 2 * 10^4 bookings over 2 * 10^4 flights, mostly spanning
nearly every flight, so per-flight updates cost ~4 * 10^8."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    wide = rng.random() < 0.5
    bookings = []
    for _ in range(N):
        if wide:
            first = rng.randint(1, 50)
            last = rng.randint(N - 50, N)
        else:
            first = rng.randint(1, N)
            last = rng.randint(first, N)
        bookings.append([first, last, rng.randint(1, 10**4)])
    return {"bookings": bookings, "n": N}
