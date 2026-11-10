"""Kth Smallest in a BST with 10^4 distinct values: a right-leaning chain 10^4 deep (k near
n) or a random-insertion BST."""

SEEDS = 2
N = 10**4


def level_order(root, left, right, val):
    out, queue, i = [], [root], 0
    while i < len(queue):
        node = queue[i]
        i += 1
        if node is None:
            out.append(None)
            continue
        out.append(val[node])
        queue.append(left[node])
        queue.append(right[node])
    while out and out[-1] is None:
        out.pop()
    return out


def generate(rng):
    vals = sorted(rng.sample(range(10**4 + 1), N))
    left, right = [None] * N, [None] * N
    if rng.random() < 0.5:
        for i in range(N - 1):
            right[i] = i + 1
        root = 0
        k = rng.randint(N - 100, N)
    else:
        order = list(range(N))
        rng.shuffle(order)
        root = order[0]
        for node in order[1:]:
            cur = root
            while True:
                if node < cur:
                    if left[cur] is None:
                        left[cur] = node
                        break
                    cur = left[cur]
                else:
                    if right[cur] is None:
                        right[cur] = node
                        break
                    cur = right[cur]
        k = rng.randint(1, N)
    return {"root": level_order(root, left, right, vals), "k": k}
