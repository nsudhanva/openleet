"""Count Items Matching a Rule: [type, color, name] items and a rule key and value."""


def check(items: list[list[str]], ruleKey: str, ruleValue: str) -> None:
    assert 1 <= len(items) <= 10**4, "1 <= items.length <= 10^4"
    assert all(len(it) == 3 for it in items), "items[i] = [type, color, name]"

    def ok(s: str) -> bool:
        return 1 <= len(s) <= 10 and s.isascii() and s.isalpha() and s.islower()

    assert all(ok(s) for it in items for s in it), "item strings are 1..10 lowercase letters"
    assert ruleKey in ("type", "color", "name"), "ruleKey is type, color or name"
    assert ok(ruleValue), "ruleValue is 1..10 lowercase letters"
