"""Calculate Score After Performing Instructions at n = 5 * 10^4: runs of adds joined by jumps
that visit every instruction once before the walk ends, so checking visits against a list of
past indices is quadratic."""

SEEDS = 2
N = 5 * 10**4
V = 10**5


def generate(rng):
    blocks, start = [], 0
    while start < N:
        end = min(N, start + rng.randint(1, 20))
        blocks.append(range(start, end))
        start = end
    rest = blocks[1:]
    rng.shuffle(rest)
    blocks = [blocks[0], *rest]
    instructions, values = [""] * N, [0] * N
    for b, block in enumerate(blocks):
        for i in block[:-1]:
            instructions[i], values[i] = "add", rng.randint(-V, V)
        last = block[-1]
        if b + 1 < len(blocks):
            instructions[last], values[last] = "jump", blocks[b + 1][0] - last
        elif rng.random() < 0.5:
            instructions[last], values[last] = "jump", rng.randrange(N) - last or N - last
        else:
            instructions[last], values[last] = "add", rng.randint(-V, V)
    return {"instructions": instructions, "values": values}
