"""Basic Calculator II at ~3 * 10^5 characters: ~5 * 10^4 terms mixing '*' and '/' chains with
random spacing, signs chosen so the running total stays inside 32 bits."""

SEEDS = 2
BUDGET = 3 * 10**5 - 40


def generate(rng):
    parts = []
    size = 0
    total = 0

    def sp():
        return " " * rng.choice([0, 0, 1, 2])

    while True:
        # One multiplicative term, evaluated left to right with truncating division.
        value = rng.randint(0, 10**4)
        term = [str(value)]
        for _ in range(rng.randint(0, 3)):
            if rng.random() < 0.5 and value <= 10**5:
                b = rng.randint(0, 9)
                value *= b
                term.append(f"{sp()}*{sp()}{b}")
            else:
                b = rng.randint(1, 10**4)
                value //= b
                term.append(f"{sp()}/{sp()}{b}")
        text = "".join(term)
        if parts:
            op = (
                "+"
                if total - value < -(10**9) or (total + value < 10**9 and rng.random() < 0.5)
                else "-"
            )
            total = total + value if op == "+" else total - value
            text = f"{sp()}{op}{sp()}{text}"
        else:
            total = value
        if size + len(text) > BUDGET:
            break
        parts.append(text)
        size += len(text)
    return {"s": sp() + "".join(parts) + sp()}
