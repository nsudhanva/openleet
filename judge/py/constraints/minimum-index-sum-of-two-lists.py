"""Minimum Index Sum of Two Lists: two lists of unique restaurant names with a common name."""


def check(list1: list[str], list2: list[str]) -> None:
    assert 1 <= len(list1) <= 1000, "1 <= list1.length <= 1000"
    assert 1 <= len(list2) <= 1000, "1 <= list2.length <= 1000"
    for name, lst in (("list1", list1), ("list2", list2)):
        assert all(isinstance(s, str) for s in lst), f"{name}[i] is a string"
        assert all(1 <= len(s) <= 30 for s in lst), f"1 <= {name}[i].length <= 30"
        assert all(c == " " or ("a" <= c <= "z") or ("A" <= c <= "Z") for s in lst for c in s), (
            f"{name}[i] consists of spaces and English letters"
        )
        assert len(set(lst)) == len(lst), f"All the strings of {name} are unique"
    assert set(list1) & set(list2), "There is at least a common string between list1 and list2"
