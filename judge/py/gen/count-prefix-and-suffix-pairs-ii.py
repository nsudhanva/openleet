"""Count Prefix and Suffix Pairs II, with the 5 * 10^5 total split between up to 99,000 short,
mostly distinct words and long words of "a" of at most 10^5 letters each (the statement's
bound). Slicing every prefix and suffix of the long words costs up to 10^10 byte copies each;
testing every pair of short words costs up to 5 * 10^9 string tests."""

SEEDS = 3
TOTAL = 500_000  # the statement's bound on the sum of the lengths
LONGEST = 10**5  # the statement's bound on one word's length
CHAIN = 20
# Per seed: the short words' letters, their lengths and their number. Many letters and words
# make them distinct; fewer words leave more of the total to the long one.
LETTERS = ("abcdefghijklmnopqrstuvwxyz", "abcdefghijklmnopqrstuvwxyz", "abcdefgh")
LENGTHS = ((3, 4), (4, 4), (4, 5))
SHORT = (14_000, 99_000, 40_000)


def generate(rng):
    shape = rng.getrandbits(6) % 3
    letters, (low, high), count = LETTERS[shape], LENGTHS[shape], SHORT[shape]
    words = ["".join(rng.choices(letters, k=rng.randint(low, high))) for _ in range(count)]
    # Powers of one letter, so the long word of that letter has many prefix-and-suffix partners.
    words += ["a" * k for k in rng.sample(range(1, CHAIN + 1), min(8, CHAIN))]
    rng.shuffle(words)
    left = TOTAL - sum(map(len, words))
    while left > 0:
        long = min(LONGEST, left)
        words.insert(rng.randrange(len(words) + 1), "a" * long)
        left -= long
    return {"words": words}
