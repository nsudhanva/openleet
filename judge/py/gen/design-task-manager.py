"""Design Task Manager with 4 * 10^4 starting tasks and 8 * 10^4 calls, 30 % of them execTop and
adds keeping the live set near 3.5 * 10^4, so scanning every live task for the top is ~10^9
steps."""

import heapq

SEEDS = 2
TASKS = 4 * 10**4
CALLS = 8 * 10**4
TOP = 10**9


def generate(rng):
    ids = rng.sample(range(10**5 + 1), 75000)
    live = {}  # taskId -> priority
    heap = []  # (-priority, -taskId), stale entries skipped

    def put(task):
        live[task] = rng.randint(0, TOP)
        heapq.heappush(heap, (-live[task], -task))

    tasks = []
    for _ in range(TASKS):
        task = ids.pop()
        put(task)
        tasks.append([rng.randint(0, 10**5), task, live[task]])
    ops, args = ["TaskManager"], [[tasks]]
    order = list(live)  # live task ids, for picking one at random
    while len(ops) <= CALLS:
        r = rng.random()
        if r < 0.3 or not order:
            ops.append("execTop")
            args.append([])
            while heap and live.get(-heap[0][1]) != -heap[0][0]:
                heapq.heappop(heap)
            if heap:
                del live[-heapq.heappop(heap)[1]]
            continue
        j = rng.randrange(len(order))
        while order[j] not in live:
            order[j] = order[-1]
            order.pop()
            if not order:
                break
            j = rng.randrange(len(order))
        if not order:
            continue
        task = order[j]
        if r < 0.65:
            task = ids.pop()
            put(task)
            order.append(task)
            ops.append("add")
            args.append([rng.randint(0, 10**5), task, live[task]])
        elif r < 0.9:
            put(task)
            ops.append("edit")
            args.append([task, live[task]])
        else:
            del live[task]
            ops.append("rmv")
            args.append([task])
    return {"ops": ops, "args": args}
