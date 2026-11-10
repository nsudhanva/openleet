"""Cinema Seat Allocation with 10^4 distinct reserved seats: n up to 10^9 (iterating every row
is too slow), reservations spread wide or packed into few rows."""

SEEDS = 3
R = 10**4


def generate(rng):
    n = rng.choice([10**9, rng.randint(1000, 10**9), 1000])
    rows = rng.sample(range(1, n + 1), min(n, 3000)) if n >= 3000 else list(range(1, n + 1))
    seats = set()
    while len(seats) < R:
        seats.add((rng.choice(rows), rng.randint(1, 10)))
    reserved = sorted(seats)
    rng.shuffle(reserved)
    return {"n": n, "reservedSeats": [list(p) for p in reserved]}
