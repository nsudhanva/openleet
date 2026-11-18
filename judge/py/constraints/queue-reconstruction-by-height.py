"""Queue Reconstruction by Height: [height, people in front who are at least as tall] pairs."""


def check(people: list[list[int]]) -> None:
    assert isinstance(people, list), "people is an array"
    n = len(people)
    assert 1 <= n <= 2000, "1 <= people.length <= 2000"
    assert all(isinstance(p, list) and len(p) == 2 for p in people), "people[i].length == 2"
    assert all(0 <= h <= 10**6 for h, _ in people), "0 <= hi <= 10^6"
    assert all(0 <= k < n for _, k in people), "0 <= ki < people.length"
    queue: list[list[int]] = []
    for h, k in sorted(people, key=lambda p: (-p[0], p[1])):
        assert k <= len(queue), "the queue can be reconstructed"
        queue.insert(k, [h, k])
    for i, (h, k) in enumerate(queue):
        assert sum(1 for g, _ in queue[:i] if g >= h) == k, "the queue can be reconstructed"
