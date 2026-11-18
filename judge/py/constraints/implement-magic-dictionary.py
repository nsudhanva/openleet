"""Implement Magic Dictionary: calls on a MagicDictionary (one buildDict, then searches)."""

LOWER = set("abcdefghijklmnopqrstuvwxyz")


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and ops and ops[0] == "MagicDictionary", "constructor first"
    assert args[0] == [], "MagicDictionary() takes no arguments"
    built = 0
    searches = 0
    for op, a in zip(ops[1:], args[1:], strict=True):
        if op == "buildDict":
            assert len(a) == 1, "buildDict takes one argument"
            assert built == 0, "buildDict will be called only once"
            assert searches == 0, "buildDict will be called before search"
            built += 1
            d = a[0]
            assert 1 <= len(d) <= 100, "1 <= dictionary.length <= 100"
            assert all(1 <= len(w) <= 100 for w in d), "1 <= dictionary[i].length <= 100"
            assert all(set(w) <= LOWER for w in d), (
                "dictionary[i] consists of only lower-case English letters"
            )
            assert len(set(d)) == len(d), "All the strings in dictionary are distinct"
        else:
            assert op == "search", "only buildDict and search are called"
            assert len(a) == 1, "search takes one argument"
            searches += 1
            w = a[0]
            assert 1 <= len(w) <= 100, "1 <= searchWord.length <= 100"
            assert set(w) <= LOWER, "searchWord consists of only lower-case English letters"
    assert searches <= 100, "At most 100 calls will be made to search"
