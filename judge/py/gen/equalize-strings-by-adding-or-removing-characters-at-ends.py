"""Equalize Strings by Adding or Removing Characters at Ends with six pairs of 1000-letter strings,
each a long run of one letter broken by a private letter and sharing one more letter that the
answer runs through, placed so that both growing and shrinking a candidate length and
searching for each substring fail late many times: ~10^8 steps of substring comparison, 2 to 3
seconds per seed."""

from string import ascii_lowercase

from _shapes import pick_shape

SEEDS = 6
N = 1000

# (first, second) layouts: (initial, target) as (u-run before the private letter, u-run between
# it and the shared letter); found by searching for the slowest growing and shrinking substring
# searches together.
LAYOUTS = [((900, 38), (262, 294)), ((900, 83), (238, 317)), ((879, 91), (255, 306))]


def generate(rng):
    layout = LAYOUTS[pick_shape(rng)]
    u, shared, *private = rng.sample(ascii_lowercase, 4)
    strings = []
    for (before, between), letter in zip(layout, private, strict=True):
        before += rng.randint(-4, 4)
        between += rng.randint(-4, 4)
        after = N - before - between - 2
        strings.append(u * before + letter + u * between + shared + u * after)
    return {"initial": strings[0], "target": strings[1]}
