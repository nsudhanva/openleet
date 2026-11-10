"""Accounts Merge at 1000 accounts: few people with shared common names whose accounts link
into long chains through one shared email each, so merges cascade deep."""

SEEDS = 2
NAMES = ["John", "Mary", "Alex", "Sam", "Kate", "Lee", "Ann", "Bob"]


def generate(rng):
    people = rng.randint(5, 200)
    owner = [rng.randrange(people) for _ in range(1000)]
    last = {}  # person -> an email of their previous account, to chain accounts
    counter = [0] * people
    accounts = []
    for p in owner:
        name = NAMES[p % len(NAMES)]
        size = rng.randint(1, 9)
        emails = []
        if p in last and rng.random() < 0.9:
            emails.append(last[p])
        while len(emails) < size:
            emails.append(f"{name.lower()}{p}x{counter[p]}@mail.com")
            counter[p] += 1
        rng.shuffle(emails)
        last[p] = rng.choice(emails)
        accounts.append([name, *emails])
    return {"accounts": accounts}
