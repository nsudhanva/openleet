"""Freedom Trail: a ring string and a key string that can be spelled from the ring."""


def check(ring: str, key: str) -> None:
    assert 1 <= len(ring) <= 100, "1 <= ring.length <= 100"
    assert 1 <= len(key) <= 100, "1 <= key.length <= 100"
    ok = set("abcdefghijklmnopqrstuvwxyz")
    assert set(ring) <= ok and set(key) <= ok, "ring and key are lowercase English letters"
    assert set(key) <= set(ring), "key can always be spelled by rotating ring"
