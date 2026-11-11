"""People Whose List of Favorite Companies Is Not a Subset at the maximum 100 people with up to
500 companies each, nearly identical lists that differ only in a last company (a few are
plain subsets), so subset checks by list search do ~10^9 string comparisons."""

SEEDS = 2
N = 100
L = 500


def name(rng):
    return "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(rng.randint(6, 14)))


def generate(rng):
    names = set()
    while len(names) < L - 1 + N:
        names.add(name(rng))
    names = sorted(names)
    rng.shuffle(names)
    pool, extra = names[: L - 1], names[L - 1 :]
    lists = []
    for i in range(N):
        if rng.random() < 0.1:
            lists.append(rng.sample(pool, L - 1 - i))
        else:
            mine = rng.sample(pool, L - 1)
            lists.append([*mine, extra[i]])
    return {"favoriteCompanies": lists}
