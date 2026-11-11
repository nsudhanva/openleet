"""Count Vowel Strings in Ranges with 4 * 10^4 short words and 4 * 10^4 queries each spanning
most of the array, so answering each query by a scan costs ~1.3 * 10^9 steps."""

SEEDS = 2
N = 4 * 10**4
Q = 4 * 10**4


def generate(rng):
    vowels, letters = "aeiou", "abcdefghijklmnopqrstuvwxyz"
    words = []
    for _ in range(N):
        k = rng.randint(1, 4)
        first = rng.choice(vowels if rng.random() < 0.6 else letters)
        last = rng.choice(vowels if rng.random() < 0.6 else letters)
        words.append(first if k == 1 else first + "".join(rng.choices(letters, k=k - 2)) + last)
    queries = []
    for _ in range(Q):
        lo = rng.randrange(N // 5)
        queries.append([lo, rng.randrange(N - N // 5, N)])
    return {"words": words, "queries": queries}
