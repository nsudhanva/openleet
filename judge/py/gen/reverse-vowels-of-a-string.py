"""Reverse Vowels on 3 * 10^5 printable ASCII characters, vowel-heavy (both cases)."""

SEEDS = 2
CHARS = [chr(c) for c in range(32, 127)]


def generate(rng):
    vowel_rate = rng.choice([0.1, 0.5, 0.9])
    return {
        "s": "".join(
            rng.choice("aeiouAEIOU") if rng.random() < vowel_rate else rng.choice(CHARS)
            for _ in range(3 * 10**5)
        )
    }
