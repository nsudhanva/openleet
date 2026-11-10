"""500 equations chaining most letters together with == and placing the contradicting != last
(or only consistent != constraints)."""

SEEDS = 3
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    contradict = rng.random() < 0.5
    eqs = []
    groups = rng.choice([1, 2, 5])
    order = list(LETTERS)
    rng.shuffle(order)
    group_of = {c: i % groups for i, c in enumerate(order)}
    while len(eqs) < 499:
        a, b = rng.choice(LETTERS), rng.choice(LETTERS)
        if group_of[a] == group_of[b]:
            eqs.append(f"{a}=={b}")
        elif rng.random() < 0.3:
            eqs.append(f"{a}!={b}")
    if contradict:
        a = rng.choice(LETTERS)
        eqs.append(f"{a}!={a}")
    else:
        eqs.append(f"{order[0]}=={order[0]}")
    return {"equations": eqs}
