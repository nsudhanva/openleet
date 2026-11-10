"""Tag Validator near the 500-char limit: deeply nested valid tags mixing CDATA and loose
'>' / ']' text, sometimes with one character corrupted."""

SEEDS = 3
LIMIT = 500
UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
TEXT = "abcdefghijXYZ0123456789 ]>!./["
ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789<>/![]. "


def build(rng, budget, depth):
    name = "".join(rng.choice(UPPER) for _ in range(rng.randint(1, 9)))
    inner = budget - 2 * len(name) - 5
    parts = []
    used = 0
    tries = 0
    while used < inner and tries < 40 and (depth == 0 or rng.random() < 0.85):
        tries += 1
        kind = rng.randrange(3)
        room = inner - used
        if kind == 0 and depth < 12 and room > 25:
            piece = build(rng, rng.randint(25, min(room, 200)), depth + 1)
        elif kind == 1 and room > 15:
            body = "".join(rng.choice(ALPHABET) for _ in range(rng.randint(0, min(room - 12, 30))))
            while "]]>" in body:
                body = body.replace("]]>", "]>")
            piece = "<![CDATA[" + body + "]]>"
        else:
            piece = "".join(rng.choice(TEXT) for _ in range(rng.randint(1, min(room, 15))))
        if used + len(piece) > inner:
            continue
        parts.append(piece)
        used += len(piece)
    return "<" + name + ">" + "".join(parts) + "</" + name + ">"


def generate(rng):
    corrupt = rng.random() < 0.5
    code = build(rng, LIMIT, 0)
    if corrupt:
        i = rng.randrange(len(code))
        code = code[:i] + rng.choice(ALPHABET) + code[i + 1 :]
    return {"code": code[:LIMIT]}
