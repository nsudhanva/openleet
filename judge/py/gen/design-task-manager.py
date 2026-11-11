"""Design Task Manager with 2 * 10^4 starting tasks and 2 * 10^4 calls, 40 % of them execTop
among adds, edits and removals, so scanning every task for the top is ~10^8 steps."""

import heapq

SEEDS = 2
TASKS = 2 * 10**4
CALLS = 2 * 10**4
TOP = 10**9


def generate(rng):
    ids = rng.sample(range(10**5 + 1), 10**5 + 1)
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
        if r < 0.4 or not order:
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
        if r < 0.6:
            task = ids.pop()
            put(task)
            order.append(task)
            ops.append("add")
            args.append([rng.randint(0, 10**5), task, live[task]])
        elif r < 0.8:
            put(task)
            ops.append("edit")
            args.append([task, live[task]])
        else:
            del live[task]
            ops.append("rmv")
            args.append([task])
    return {"ops": ops, "args": args}
