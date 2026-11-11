"""Length of the Longest Valid Substring with a 2 * 10^4-letter word and 2 * 10^4 forbidden
strings, two of them cutting the word near its middle, so checking every substring of the current
window instead of the last ten letters costs ~10^8 lookups."""

SEEDS = 2
N = 2 * 10**4
F = 2 * 10**4


def generate(rng):
    letters = "abcdefghijklmnopqrstuvwxyz"
    word = "".join(rng.choice(letters) for _ in range(N))
    present = {word[i : i + 10] for i in range(N - 9)}
    forbidden = set()
    while len(forbidden) < F - 2:
        w = "".join(rng.choice(letters) for _ in range(10))
        if w not in present:
            forbidden.add(w)
    forbidden = sorted(forbidden)
    for cut in (N // 3, 2 * N // 3):
        forbidden.append(word[cut : cut + 6])
    rng.shuffle(forbidden)
    return {"word": word, "forbidden": forbidden}
