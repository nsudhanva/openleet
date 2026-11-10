"""Word Ladder II with 500 words of length 3-5 over small alphabets: dense graphs with many
equal-length shortest paths, the total output kept under 10^5 words."""

from string import ascii_lowercase

from _shapes import pick_shape, random_string

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
                for c in ascii_lowercase:
                    v = w[:i] + c + w[i + 1 :]
                    if v in wordset and v not in count:
                        nxt[v] = nxt.get(v, 0) + count[w]
        count.update(nxt)
        frontier = sorted(nxt)
        dist += 1
    return count.get(end, 0) * dist


def generate(rng):
    shape = pick_shape(rng)
    length, letters = [(4, "abcdef"), (5, "abcd"), (3, "abcdefghi")][shape]
    pool = set()
    while len(pool) < N:
        pool.add(random_string(rng, letters, length))
    words = sorted(pool)
    rng.shuffle(words)
    # Of a few begin/end pairs, keep the one with the most output that still fits the cap.
    best = None
    for _ in range(12):
        begin = random_string(rng, letters, length)
        end = rng.choice(words)
        if begin == end:
            continue
        size = shortest_paths_size(begin, end, words)
        if size <= CAP and (best is None or size > best[0]):
            best = (size, begin, end)
    assert best is not None, "one of the 12 pairs fits the cap"
    _, begin, end = best
    return {"beginWord": begin, "endWord": end, "wordList": words}
