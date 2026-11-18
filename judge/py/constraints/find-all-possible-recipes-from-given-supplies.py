"""Find All Possible Recipes from Given Supplies: recipe names, their ingredients, and supplies."""


def _word(s: str, what: str) -> bool:
    return isinstance(s, str) and 1 <= len(s) <= 10 and s.isascii() and s.islower() and s.isalpha()


def check(recipes: list[str], ingredients: list[list[str]], supplies: list[str]) -> None:
    n = len(recipes)
    assert n == len(ingredients), "n == recipes.length == ingredients.length"
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(1 <= len(row) <= 100 for row in ingredients), "1 <= ingredients[i].length <= 100"
    assert 1 <= len(supplies) <= 100, "1 <= supplies.length <= 100"
    assert all(_word(r, "") for r in recipes), "recipes[i]: 1..10 lowercase letters"
    assert all(_word(x, "") for row in ingredients for x in row), (
        "ingredients[i][j]: 1..10 lowercase letters"
    )
    assert all(_word(s, "") for s in supplies), "supplies[k]: 1..10 lowercase letters"
    assert len(set(recipes) | set(supplies)) == n + len(supplies), (
        "all the values of recipes and supplies combined are unique"
    )
    assert all(len(set(row)) == len(row) for row in ingredients), (
        "each ingredients[i] has no duplicate values"
    )
