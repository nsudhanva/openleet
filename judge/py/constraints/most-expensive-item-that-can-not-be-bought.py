"""Most Expensive Item That Can Not Be Bought: two distinct primes."""


def _is_prime(x: int) -> bool:
    if x < 2:
        return False
    i = 2
    while i * i <= x:
        if x % i == 0:
            return False
        i += 1
    return True


def check(primeOne: int, primeTwo: int) -> None:
    assert 1 < primeOne < 10**4 and 1 < primeTwo < 10**4, "1 < primeOne, primeTwo < 10^4"
    assert _is_prime(primeOne) and _is_prime(primeTwo), "primeOne, primeTwo are prime numbers"
    assert primeOne != primeTwo, "primeOne and primeTwo are distinct"
    assert primeOne * primeTwo < 10**5, "primeOne * primeTwo < 10^5"
