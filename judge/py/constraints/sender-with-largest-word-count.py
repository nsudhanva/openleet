"""Sender With Largest Word Count: parallel lists of messages and sender names."""

import string


def check(messages: list[str], senders: list[str]) -> None:
    n = len(messages)
    assert n == len(senders), "messages.length == senders.length"
    assert 1 <= n <= 10**4, "1 <= n <= 10^4"
    letters = set(string.ascii_letters)
    assert all(1 <= len(m) <= 100 for m in messages), "1 <= messages[i].length <= 100"
    assert all(set(m) <= letters | {" "} for m in messages), (
        "messages[i] consists of uppercase and lowercase English letters and ' '"
    )
    assert all(m == m.strip(" ") for m in messages), "messages[i] has no leading or trailing spaces"
    assert all("  " not in m for m in messages), (
        "words in messages[i] are separated by a single space"
    )
    assert all(1 <= len(s) <= 10 for s in senders), "1 <= senders[i].length <= 10"
    assert all(set(s) <= letters for s in senders), "senders[i] consists of English letters only"
