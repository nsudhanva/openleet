"""Reconstruct Itinerary with 300 tickets among a handful of airports, built from one random
walk out of JFK (so a full itinerary exists), with many duplicate tickets and dead ends for
greedy lexical choice."""

SEEDS = 2


def generate(rng):
    k = rng.choice([3, 6])
    airports = ["JFK", "AAA", "ABC", "ZZZ", "MUC", "LHR", "SFO"][: k + 1]
    cur, tickets = "JFK", []
    for _ in range(300):
        nxt = rng.choice([a for a in airports if a != cur])
        tickets.append([cur, nxt])
        cur = nxt
    rng.shuffle(tickets)
    return {"tickets": tickets}
