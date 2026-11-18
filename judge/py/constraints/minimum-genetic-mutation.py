"""Minimum Genetic Mutation: start and end genes of 8 letters and a bank of valid genes."""


def check(startGene: str, endGene: str, bank: list[str]) -> None:
    assert 0 <= len(bank) <= 10, "0 <= bank.length <= 10"
    for g in [startGene, endGene, *bank]:
        assert len(g) == 8, "startGene.length == endGene.length == bank[i].length == 8"
        assert all(c in "ACGT" for c in g), "genes consist only of 'A', 'C', 'G', 'T'"
