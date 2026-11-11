"""Largest Multiple of Three at the maximum 10^4 digits, with a digit sum that no single digit
can fix, so trying every pair of digits to drop costs ~5 * 10^7 checks."""

SEEDS = 2
N = 10**4


def generate(rng):
    # The sum is r mod 3 but no digit is: only two digits of the other non-zero residue fix it.
    r = rng.choice([1, 2])
    other = (2, 5, 8) if r == 1 else (1, 4, 7)
    while True:
        digits = [rng.choice((0, 3, 6, 9, *other)) for _ in range(N)]
        if sum(digits) % 3 == r:
            return {"digits": digits}
