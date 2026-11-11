"""Equalize Strings by Adding or Removing Characters at Ends with two 1000-letter runs of one
letter, each broken by a private letter and sharing one more letter that the answer (~450 to 600
long) runs through, placed so that growing or shrinking a candidate length and searching for
each substring fails late many times: extending a match from every pair of positions is ~10^8
steps."""

from string import ascii_lowercase

from _shapes import pick_shape

SEEDS = 3
N = 1000

# (first, second) layouts: (initial, target) as (u-run before the private letter, u-run between
# it and the shared letter); found by searching for the slowest growing (shapes 0 and 2) and
# shrinking (shape 1) substring searches.
LAYOUTS = [((14, 115), (259, 278)), ((394, 383), (530, 15)), ((14, 115), (259, 278))]


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
