"""N-ary Tree Level Order Traversal at 10^4 nodes and the maximum height: a 999-node chain
with the rest hung at random depths, so one DFS per level is ~10^7 node visits."""

SEEDS = 3
N = 10**4
HEIGHT = 999


def generate(rng):
    children = [[] for _ in range(N)]
    depth = [1] * N
    for v in range(1, HEIGHT):
        children[v - 1].append(v)
        depth[v] = depth[v - 1] + 1
    for v in range(HEIGHT, N):
        parent = rng.randrange(v)
        while depth[parent] >= HEIGHT:
            parent = rng.randrange(v)
        children[parent].append(v)
        depth[v] = depth[parent] + 1
    for kids in children:
        rng.shuffle(kids)
    vals = [rng.randint(0, 10**4) for _ in range(N)]
    out, queue = [vals[0], None], [0]
    for node in queue:
        for child in children[node]:
            out.append(vals[child])
            queue.append(child)
        out.append(None)
    while out and out[-1] is None:
        out.pop()
    return {"root": out}
