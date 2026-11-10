"""Design Browser History with 5000 calls: long visit runs to build deep history, then
back/forward jumps of up to 100 steps."""

SEEDS = 2
CALLS = 5000
CHARS = "abcdefghijklmnopqrstuvwxyz."


def url(rng):
    return "".join(rng.choice(CHARS) for _ in range(rng.randint(1, 20)))


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
