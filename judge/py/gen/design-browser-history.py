"""Design Browser History with 5000 calls: long visit runs to build deep history, then
back/forward jumps of up to 100 steps."""

from _shapes import random_string

SEEDS = 2
CALLS = 5000
CHARS = "abcdefghijklmnopqrstuvwxyz."


def url(rng):
    return random_string(rng, CHARS, rng.randint(1, 20))


def generate(rng):
    ops, args = ["BrowserHistory"], [[url(rng)]]
    visit_p = rng.choice([0.4, 0.7])
    for _ in range(CALLS):
        x = rng.random()
        if x < visit_p:
            ops.append("visit")
            args.append([url(rng)])
        elif x < visit_p + (1 - visit_p) / 2:
            ops.append("back")
            args.append([rng.randint(1, 100)])
        else:
            ops.append("forward")
            args.append([rng.randint(1, 100)])
    return {"ops": ops, "args": args}
