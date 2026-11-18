"""Meeting Scheduler: two people's availability slots and a meeting duration."""


def check(slots1: list[list[int]], slots2: list[list[int]], duration: int) -> None:
    for slots in (slots1, slots2):
        assert 1 <= len(slots) <= 10**4, "1 <= slots.length <= 10^4"
        assert all(len(s) == 2 for s in slots), "slots[i].length == 2"
        assert all(s < e for s, e in slots), "slots[i][0] < slots[i][1]"
        assert all(0 <= v <= 10**9 for s in slots for v in s), "0 <= slots[i][j] <= 10^9"
        ordered = sorted(slots)
        assert all(ordered[i][1] < ordered[i + 1][0] for i in range(len(ordered) - 1)), (
            "no two slots of the same person intersect"
        )
    assert 1 <= duration <= 10**6, "1 <= duration <= 10^6"
