"""Robot Collisions at n = 10^5: every robot left of the middle moves right and every robot
right of it moves left, so ~n collisions happen at one meeting point and rescanning for the next
colliding pair after each one is O(n^2), as is deleting each destroyed robot from a list."""

SEEDS = 2
N = 10**5
LIMIT = 10**9


def generate(rng):
    positions = sorted(rng.sample(range(1, LIMIT + 1), N))
    top = rng.choice([5, LIMIT])
    healths = [rng.randint(1, top) for _ in range(N)]
    directions = ["R"] * (N // 2) + ["L"] * (N - N // 2)
    order = list(range(N))
    rng.shuffle(order)
    return {
        "positions": [positions[i] for i in order],
        "healths": [healths[i] for i in order],
        "directions": "".join(directions[i] for i in order),
    }
