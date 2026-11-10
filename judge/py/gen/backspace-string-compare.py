"""Backspace String Compare at length 200: heavy runs of '#' (including more '#' than letters)
over strings that differ only before the backspaces erase them."""

SEEDS = 3


def generate(rng):
    def noisy(core):
        out = []
        for ch in core:
            out.append(ch)
            if rng.random() < 0.4:
                junk = rng.randint(1, 3)
                out += [rng.choice("abc") for _ in range(junk)] + ["#"] * junk
        if rng.random() < 0.3:
            out = ["#"] * rng.randint(1, 5) + out
        return "".join(out)[:200]

    core = "".join(rng.choice("ab") for _ in range(rng.randint(20, 60)))
    s = noisy(core)
    other = core if rng.random() < 0.5 else core[:-1] + ("a" if core[-1] == "b" else "b")
    t = noisy(other)
    return {"s": s or "#", "t": t or "#"}
