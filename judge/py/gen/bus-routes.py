"""Bus Routes with 500 routes and 10^5 total stops: a chain where each route shares one stop
only with the next (answer 500, BFS fully deep), or random routes over a shared stop pool."""

SEEDS = 3
ROUTES = 500
STOPS = 10**5


def generate(rng):
    per = STOPS // ROUTES
    if rng.random() < 0.5:
        labels = rng.sample(range(10**6), ROUTES * per)
        routes = []
        for i in range(ROUTES):
            stops = labels[i * per : (i + 1) * per]
            if i:
                stops[0] = routes[-1][-1]  # shared with the previous route only
            routes.append(stops)
        source = routes[0][1]
        target = routes[-1][-2]
        for r in routes:
            rng.shuffle(r)
        return {"routes": routes, "source": source, "target": target}
    pool = rng.sample(range(10**6), rng.choice([2000, 5 * 10**4]))
    routes = [rng.sample(pool, per) for _ in range(ROUTES)]
    source = rng.choice(routes[0])
    target = rng.choice([rng.choice(pool), rng.randrange(10**6)])
    return {"routes": routes, "source": source, "target": target}
