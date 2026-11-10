"""Exam Room with 10^4 seat/leave calls on n up to 10^9 seats (an array of seats is hopeless);
the seating rule is replayed here so leave() only ever names an occupied seat."""

import heapq

SEEDS = 2
CALLS = 10**4


def generate(rng):
    n = rng.choice([10**9, rng.randint(10**4, 10**5)])
    seat_p = rng.choice([0.6, 0.8])
    ops, args = ["ExamRoom"], [[n]]
    nxt, prv = {-1: n}, {n: -1}
    heap = [(-(10**18), 0, -1, n)]
    seated, where = [], {}

    def push(left, right):
        if left == -1 and right == n:
            heapq.heappush(heap, (-(10**18), 0, left, right))
        elif left == -1:
            if right > 0:
                heapq.heappush(heap, (-right, 0, left, right))
        elif right == n:
            if left < n - 1:
                heapq.heappush(heap, (-(n - 1 - left), n - 1, left, right))
        elif right - left > 1:
            d = (right - left) // 2
            heapq.heappush(heap, (-d, left + d, left, right))

    for _ in range(CALLS):
        if seated and (rng.random() >= seat_p or len(seated) == n):
            i = rng.randrange(len(seated))
            p = seated[i]
            seated[i] = seated[-1]
            where[seated[i]] = i
            seated.pop()
            del where[p]
            left, right = prv.pop(p), nxt.pop(p)
            nxt[left], prv[right] = right, left
            push(left, right)
            ops.append("leave")
            args.append([p])
            continue
        while True:
            _, p, left, right = heapq.heappop(heap)
            if nxt.get(left) == right:
                break
        nxt[left], prv[p] = p, left
        nxt[p], prv[right] = right, p
        push(left, p)
        push(p, right)
        where[p] = len(seated)
        seated.append(p)
        ops.append("seat")
        args.append([])
    return {"ops": ops, "args": args}
