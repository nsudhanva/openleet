"""Word Search II on a 12 x 12 board of few letters with 3 * 10^4 words of up to 10 letters
over the same letters, so most prefixes are live and per-word DFS is far too slow."""

SEEDS = 2
SIZE = 12
N = 3 * 10**4


def generate(rng):
    letters = "ab" if rng.random() < 0.5 else "abcde"
    board = [[rng.choice(letters) for _ in range(SIZE)] for _ in range(SIZE)]
    words = set()
    while len(words) < N:
        words.add("".join(rng.choice(letters) for _ in range(rng.randint(1, 10))))
        if letters == "ab" and len(words) >= 2046:  # all strings over 'ab' up to length 10
            letters = "abc"
    words = sorted(words)
    rng.shuffle(words)
    return {"board": board, "words": words}
