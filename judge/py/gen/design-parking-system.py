"""Design Parking System with the full 1000 addCar calls, filling some lot types well past
capacity."""

SEEDS = 2


def generate(rng):
    sizes = [rng.randint(0, 1000) for _ in range(3)]
    ops, args = ["ParkingSystem"], [sizes]
    for _ in range(1000):
        ops.append("addCar")
        args.append([rng.choice([1, 2, 3])])
    return {"ops": ops, "args": args}
