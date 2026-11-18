"""Reconstruct Itinerary: airline tickets [from, to] forming a valid itinerary from JFK."""

from collections import defaultdict


def check(tickets: list[list[str]]) -> None:
    assert 1 <= len(tickets) <= 300, "1 <= tickets.length <= 300"
    assert all(len(t) == 2 for t in tickets), "tickets[i].length == 2"
    for t in tickets:
        for p in t:
            assert len(p) == 3 and all("A" <= c <= "Z" for c in p), "3 uppercase English letters"
        assert t[0] != t[1], "fromi != toi"
    out = defaultdict(int)
    inn = defaultdict(int)
    adj = defaultdict(set)
    for a, b in tickets:
        out[a] += 1
        inn[b] += 1
        adj[a].add(b)
    assert "JFK" in out, "the itinerary begins with JFK"
    diffs = {k: out[k] - inn[k] for k in set(out) | set(inn) if out[k] != inn[k]}
    ends = [k for k, d in diffs.items() if d == -1]
    starts = [k for k, d in diffs.items() if d == 1]
    ok = (not diffs) or (
        len(diffs) == 2 and len(starts) == 1 and len(ends) == 1 and starts[0] == "JFK"
    )
    assert ok, "tickets form at least one valid itinerary from JFK"
    seen = {"JFK"}
    stack = ["JFK"]
    while stack:
        for nxt in adj[stack.pop()]:
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    assert all(a in seen for a in out), "tickets form at least one valid itinerary from JFK"
