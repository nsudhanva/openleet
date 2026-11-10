"""Array of Doubled Pairs at n = 3 * 10^4: built from (x, 2x) pairs over negatives, zeros and
long doubling chains so the answer is true, or the same with one value nudged."""

SEEDS = 3
N = 3 * 10**4
LIM = 10**5


def generate(rng):
    arr = []
    while len(arr) < N:
        r = rng.random()
        if r < 0.05:
            arr += [0, 0]
        elif r < 0.3:  # doubling chain x, 2x, 4x, ... of even length
            x = rng.choice([1, -1]) * rng.randint(1, 50)
            length = 2 * rng.randint(1, 5)
            chain = [x << i for i in range(length)]
            if abs(chain[-1]) <= LIM and len(arr) + length <= N:
                arr += chain
        else:
            x = rng.choice([1, -1]) * rng.randint(1, LIM // 2)
            arr += [x, 2 * x]
    arr = arr[:N]
    if rng.random() < 0.4:
        i = rng.randrange(N)
        arr[i] = arr[i] + 1 if arr[i] < LIM else arr[i] - 1
    rng.shuffle(arr)
    return {"arr": arr}
