"""Count Ways to Build Rooms at n = 2 * 10^4: a spine of 10^4 rooms with small random subtrees
hanging off it, so computing each room's subtree size by its own walk costs ~10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    spine = N // 2
    parent = [-1] + [i - 1 for i in range(1, spine)]
    for i in range(spine, N):
        # Hang the rest off random spine rooms or off rooms already hanging.
        parent.append(
            rng.randrange(spine) if i == spine or rng.random() < 0.6 else rng.randrange(spine, i)
        )
    label = [0, *rng.sample(range(1, N), N - 1)]
    prev_room = [0] * N
    for i in range(N):
        prev_room[label[i]] = -1 if i == 0 else label[parent[i]]
    return {"prevRoom": prev_room}
