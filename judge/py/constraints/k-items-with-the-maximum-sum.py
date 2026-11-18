"""K Items With the Maximum Sum: counts of 1s, 0s and -1s and a pick count k."""


def check(numOnes: int, numZeros: int, numNegOnes: int, k: int) -> None:
    assert 0 <= numOnes <= 50, "0 <= numOnes <= 50"
    assert 0 <= numZeros <= 50, "0 <= numZeros <= 50"
    assert 0 <= numNegOnes <= 50, "0 <= numNegOnes <= 50"
    assert 0 <= k <= numOnes + numZeros + numNegOnes, "0 <= k <= numOnes + numZeros + numNegOnes"
