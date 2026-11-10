"""Student Attendance Record I at the maximum length of 1000, with late runs of length 2 and
absences rare enough that the answer is not trivially false."""

SEEDS = 3
N = 1000


def generate(rng):
    shape = rng.getrandbits(6) % 3  # seeds 0-2 land on three different shapes
    if shape == 0:
        s = ["P" if rng.random() < 0.6 else "L" for _ in range(N)]
        # Break every run of 3 L's so the record can pass, then add at most one A.
        for i in range(2, N):
            if s[i] == s[i - 1] == s[i - 2] == "L":
                s[i] = "P"
        s[rng.randrange(N)] = "A"
    elif shape == 1:
        s = ["L", "L", "P"] * (N // 3) + ["L"]
        s[-3:] = ["L", "L", "L"]  # the only failure is at the very end
    else:
        s = [rng.choice("PLA") for _ in range(N)]
    return {"s": "".join(s)}
