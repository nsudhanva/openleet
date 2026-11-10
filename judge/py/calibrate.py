"""A fixed piece of typical solution work, timed to tell how fast this machine runs Python
right now. The zygote runs it the moment before it forks each submission and again once the
submission has ended, so the measure sees the cache, memory pressure, neighbours and CPU
throttling the solution ran under.

On the e2-micro, CPU time per unit of work grows about 7x once its burst allowance runs out (14x
beside a memory-heavy process), with no steal time to show for it; this work slows by the same
factor (its ratio to typical solution work stayed within 15% throughout), so dividing CPU time
by it gives a time that does not depend on the machine or its load.
"""

import time

ROUNDS = 3


def work() -> int:
    """A big hash map and scattered list reads (cache misses, as on 10^5-element inputs), a
    sort, a monotonic stack, a 2-D DP, string building and fresh pages: the mix of interpreter,
    allocator and memory work most solutions are made of."""
    n = 1 << 15
    keys = [i * 2654435761 % 1_000_000_007 for i in range(n)]
    seen = {k: i for i, k in enumerate(keys)}
    hits = sum(k ^ 1 in seen for k in keys)
    big = list(range(1 << 18, 1 << 19))
    j = total = 0
    for _ in range(n):
        j = (j * 1103515245 + 12345) & ((1 << 18) - 1)
        total += big[j]
    stack: list[int] = []
    for v in sorted(keys, key=lambda v: v % 1009):
        while stack and stack[-1] > v:
            stack.pop()
        stack.append(v)
    size = 80
    dp = [[0] * size for _ in range(size)]
    for i in range(1, size):
        row, up = dp[i], dp[i - 1]
        for c in range(1, size):
            row[c] = max(up[c], row[c - 1]) + ((i ^ c) & 1)
    words = {"".join(chr(97 + (i * k) % 26) for k in range(6)) for i in range(1500)}
    pages = bytearray(4 << 20)
    for k in range(0, len(pages), 4096):
        pages[k] = 1
    return hits + total + len(stack) + dp[-1][-1] + len(words) + len(pages)


def measure() -> int:
    """CPU nanoseconds of one `work()`, the median of a few rounds (one interrupt or page
    reclaim does not decide it, a slow machine does)."""
    times = []
    for _ in range(ROUNDS):
        start = time.process_time_ns()
        work()
        times.append(time.process_time_ns() - start)
    return sorted(times)[ROUNDS // 2]
