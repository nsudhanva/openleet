"""Count Beautiful Substrings II at n = 2 * 10^4 built from vowel-consonant pairs in random order,
so the vowel balance stays within 1 of zero: counting each substring's vowels costs 2 * 10^8 steps
and pairing each prefix with every earlier prefix of the same balance ~7 * 10^7."""

SEEDS = 2
N = 2 * 10**4
VOWELS = "aeiou"


def generate(rng):
    k = 1 if rng.random() < 0.5 else rng.choice((2, 4, 9, 12, 36, 100, 360, 1000))
    consonants = rng.choice(("bcdfg", "xyzbcd"))
    letters = []
    for _ in range(N // 2):
        pair = [rng.choice(VOWELS), rng.choice(consonants)]
        if rng.random() < 0.5:
            pair.reverse()
        letters += pair
    return {"s": "".join(letters), "k": k}
