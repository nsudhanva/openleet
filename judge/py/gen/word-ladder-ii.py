"""Word Ladder II with 500 words of length 3-5 over small alphabets: dense graphs with many
equal-length shortest paths, the total output kept under 10^5 words."""

SEEDS = 3
N = 500
CAP = 10**5


def shortest_paths_size(begin, end, words):
    """Number of shortest sequences times their length (0 when unreachable)."""
    wordset = set(words)
    count = {begin: 1}
    frontier = [begin]
    dist = 1
    while frontier and end not in count:
        nxt = {}
        for w in frontier:
            for i in range(len(w)):
                for c in "abcdefghijklmnopqrstuvwxyz":
                    v = w[:i] + c + w[i + 1 :]
                    if v in wordset and v not in count:
                        nxt[v] = nxt.get(v, 0) + count[w]
        count.update(nxt)
        frontier = sorted(nxt)
        dist += 1
    return count.get(end, 0) * dist


def generate(rng):
    shape = rng.getrandbits(6) % 3  # seeds 0-2 land on three different shapes
    length, letters = [(4, "abcdef"), (5, "abcd"), (3, "abcdefghi")][shape]
    pool = set()
    while len(pool) < N:
        pool.add("".join(rng.choice(letters) for _ in range(length)))
    words = sorted(pool)
    rng.shuffle(words)
    # Of a few begin/end pairs, keep the one with the most output that still fits the cap.
    best = None
    for _ in range(12):
        begin = "".join(rng.choice(letters) for _ in range(length))
        end = rng.choice(words)
        if begin == end:
            continue
        size = shortest_paths_size(begin, end, words)
        if size <= CAP and (best is None or size > best[0]):
            best = (size, begin, end)
    _, begin, end = best
    return {"beginWord": begin, "endWord": end, "wordList": words}
