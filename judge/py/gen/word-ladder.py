"""Word Ladder with 5000 words over a tiny alphabet so the graph is dense (every word has
many neighbours), and begin/end at opposite corners or unreachable."""

from _shapes import pick_shape

SEEDS = 3
N = 5000


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        length, letters = 6, "abcde"
    elif shape == 1:
        length, letters = 10, "abc"
    else:
        length, letters = 4, "abcdefghij"
    begin = letters[0] * length
    # Unreachable variant: 'z' is outside the alphabet, so the end has no neighbours.
    end = "z" * length if shape == 2 else letters[-1] * length
    pool = {end}
    while len(pool) < N:
        w = "".join(rng.choice(letters) for _ in range(length))
        if w != begin:
            pool.add(w)
    words = sorted(pool)
    rng.shuffle(words)
    return {"beginWord": begin, "endWord": end, "wordList": words}
