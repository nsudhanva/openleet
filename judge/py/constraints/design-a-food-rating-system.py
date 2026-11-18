"""Design a Food Rating System: FoodRatings(foods, cuisines, ratings), then its calls."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and ops, "ops and args have the same non-zero length"
    assert ops[0] == "FoodRatings" and len(args[0]) == 3, (
        "FoodRatings(foods, cuisines, ratings) comes first"
    )
    foods, cuisines, ratings = args[0]
    n = len(foods)
    assert 1 <= n <= 2 * 10**4, "1 <= n <= 2 * 10^4"
    assert len(cuisines) == n and len(ratings) == n, (
        "n == foods.length == cuisines.length == ratings.length"
    )
    for name, arr in (("foods", foods), ("cuisines", cuisines)):
        assert all(isinstance(s, str) for s in arr), f"{name}[i] is a string"
        assert all(1 <= len(s) <= 10 for s in arr), f"1 <= {name}[i].length <= 10"
        assert all("a" <= c <= "z" for s in arr for c in s), (
            f"{name}[i] consists of lowercase English letters"
        )
    assert all(1 <= r <= 10**8 for r in ratings), "1 <= ratings[i] <= 10^8"
    assert len(set(foods)) == n, "all the strings in foods are distinct"
    food_set = set(foods)
    cuisine_set = set(cuisines)
    assert len(ops) - 1 <= 2 * 10**4, "at most 2 * 10^4 calls to changeRating and highestRated"
    for op, a in zip(ops[1:], args[1:], strict=True):
        if op == "changeRating":
            assert len(a) == 2, "changeRating(food, newRating)"
            assert a[0] in food_set, "food is the name of a food item in the system"
        elif op == "highestRated":
            assert len(a) == 1, "highestRated(cuisine)"
            assert a[0] in cuisine_set, "cuisine is a type of cuisine of a food item in the system"
        else:
            raise AssertionError("ops are FoodRatings, changeRating, highestRated")
