"""Earliest Finish Time for Land and Water Rides II with n = m = 5 * 10^4 rides, punishing the
quadratic pair scan."""

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    def side():
        return (
            [rng.randint(1, 10**5) for _ in range(N)],
            [rng.randint(1, 10**5) for _ in range(N)],
        )

    land_start, land_dur = side()
    water_start, water_dur = side()
    return {
        "landStartTime": land_start,
        "landDuration": land_dur,
        "waterStartTime": water_start,
        "waterDuration": water_dur,
    }
