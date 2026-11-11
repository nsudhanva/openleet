"""Power Grid Maintenance with c = 10^5 stations in one or three grids: every station goes
offline in increasing order, then 10^5 checks on offline stations make a solution that walks
a grid's stations from the lowest do ~5 * 10^9 steps (a sorted list of the grid deletes at
its front, ~4 * 10^10 bytes moved)."""

SEEDS = 3
C = 100_000
OFFLINE = 100_000
CHECKS = 100_000


def generate(rng):
    shape = rng.getrandbits(6) % 3
    if shape == 0:  # one path
        connections = [[u, u + 1] for u in range(1, C)]
    elif shape == 1:  # one tree hanging each station off a recent one
        connections = [[rng.randrange(max(1, u - 40), u), u] for u in range(2, C + 1)]
    else:  # three paths, stations 1, 2, 0 mod 3
        connections = [[u, u + 3] for u in range(1, C - 2)]
    queries = [[2, x] for x in range(1, OFFLINE + 1)]
    queries += [[1, x] for x in rng.choices(range(1, OFFLINE + 1), k=CHECKS)]
    return {"c": C, "connections": connections, "queries": queries}
