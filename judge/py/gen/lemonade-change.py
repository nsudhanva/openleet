"""Lemonade Change with 10^5 bills: a long payable sequence, sometimes with one unpayable
bill near the end."""

SEEDS = 2
N = 10**5


def generate(rng):
    fives = tens = 0
    bills = []
    for _ in range(N - 1):
        options = [5]
        if fives >= 1:
            options.append(10)
        if (tens >= 1 and fives >= 1) or fives >= 3:
            options.append(20)
        bill = rng.choice(options)
        if bill == 5:
            fives += 1
        elif bill == 10:
            fives -= 1
            tens += 1
        elif tens >= 1:
            tens -= 1
            fives -= 1
        else:
            fives -= 3
        bills.append(bill)
    bills.append(rng.choice([5, 10, 20]))
    return {"bills": bills}
