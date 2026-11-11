"""Maximum Average Pass Ratio with 2 * 10^4 classes and 2 * 10^4 extra students, so scanning
every class for each student's best placement is 4 * 10^8 steps."""

SEEDS = 2
N = K = 2 * 10**4
LIMIT = 10**5


def generate(rng):
    classes = []
    for _ in range(N):
        total = rng.randint(1, LIMIT)
        classes.append([rng.randint(1, total), total])
    return {"classes": classes, "extraStudents": K}
