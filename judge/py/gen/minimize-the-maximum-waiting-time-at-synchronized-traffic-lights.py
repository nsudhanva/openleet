"""Minimize the Maximum Waiting Time at Synchronized Traffic Lights with 10^4 lights and
5 * 10^4 cars, so checking every light for every car is 5 * 10^8 steps."""

SEEDS = 2
LIGHTS = 10**4
CARS = 5 * 10**4
LIMIT = 10**9


def generate(rng):
    period = rng.randint(LIMIT // 2, LIMIT)
    lights = [rng.randint(1, period // 2) for _ in range(LIGHTS)]
    arrival = [rng.randint(1, LIMIT) for _ in range(CARS)]
    return {"period": period, "lights": lights, "arrivalTime": arrival}
