"""Parsing a Boolean Expression at up to the maximum 2 * 10^4 characters, nested ~5000 levels
deep (mostly '!', some '&' and '|' with extra leaves), so re-scanning each subexpression's text
to split its arguments does ~5 * 10^7 character visits."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    want = rng.random() < 0.5
    core = rng.choice("tf")
    value = core == "t"
    prefixes, suffixes, length = [], [], 1
    while True:
        op = "!" if rng.random() < 0.7 else rng.choice("&|")
        if op == "!":
            pre, suf, new = "!(", ")", not value
        else:
            before = [rng.choice("tf") for _ in range(rng.randint(0, 2))]
            after = [rng.choice("tf") for _ in range(rng.randint(0, 2))]
            pre = op + "(" + "".join(c + "," for c in before)
            suf = "".join("," + c for c in after) + ")"
            leaves = [c == "t" for c in before + after]
            new = value and all(leaves) if op == "&" else value or any(leaves)
        # Keep 3 characters spare for a final '!(...)' that sets the answer to `want`.
        if length + len(pre) + len(suf) > N - 3:
            break
        prefixes.append(pre)
        suffixes.append(suf)
        length += len(pre) + len(suf)
        value = new
    expression = "".join(reversed(prefixes)) + core + "".join(suffixes)
    if value != want:
        expression = "!(" + expression + ")"
    return {"expression": expression}
