"""Robot Return to Origin on 2 * 10^4 moves: a balanced walk (true) or one off by a single move."""

SEEDS = 2


def generate(rng):
    half = [rng.choice("UL") for _ in range(10**4)]
    moves = half + [{"U": "D", "L": "R"}[m] for m in half]
    rng.shuffle(moves)
    if rng.random() < 0.5:
        i = rng.randrange(len(moves))
        moves[i] = {"U": "L", "D": "R", "L": "D", "R": "U"}[moves[i]]
    return {"moves": "".join(moves)}
