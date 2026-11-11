"""Swap For Longest Repeated Character Substring at n = 2 * 10^4: one letter broken by two to four
other letters, so growing a window from every start is ~10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    main = rng.choice("abcdefghijklmnopqrstuvwxyz")
    text = [main] * N
    for i in rng.sample(range(N), rng.randint(2, 4)):
        text[i] = rng.choice("abcdefghijklmnopqrstuvwxyz")
    return {"text": "".join(text)}
