"""Dungeon Game on a 200 x 200 grid: mostly damage with scattered healing orbs, so the path
choice matters across the whole grid."""

SEEDS = 2
SIZE = 200


def generate(rng):
    heal = rng.choice([0.1, 0.3])
    dungeon = [
        [
            rng.randint(1, 1000) if rng.random() < heal else rng.randint(-1000, 0)
            for _ in range(SIZE)
        ]
        for _ in range(SIZE)
    ]
    return {"dungeon": dungeon}
