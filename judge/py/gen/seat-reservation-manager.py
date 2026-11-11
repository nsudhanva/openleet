"""Seat Reservation Manager with n = 10^5 and 6 * 10^4 calls: 3 * 10^4 reserves, then
unreserve/reserve pairs on random reserved seats, so finding the smallest free seat by a scan
costs ~1.5 * 10^4 per call."""

SEEDS = 2
N = 10**5
CALLS = 6 * 10**4


def generate(rng):
    ops, args = ["SeatManager"], [[N]]
    reserved = []
    first = CALLS // 2
    for seat in range(1, first + 1):
        ops.append("reserve")
        args.append([])
        reserved.append(seat)
    while len(ops) - 1 < CALLS:
        j = rng.randrange(len(reserved))
        reserved[j], reserved[-1] = reserved[-1], reserved[j]
        seat = reserved.pop()
        ops.append("unreserve")
        args.append([seat])
        ops.append("reserve")
        args.append([])
        reserved.append(seat)
    return {"ops": ops[: CALLS + 1], "args": args[: CALLS + 1]}
