"""Maximum Employees to Be Invited to a Meeting: each employee names a favorite other employee."""


def check(favorite: list[int]) -> None:
    n = len(favorite)
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert all(0 <= f <= n - 1 for f in favorite), "0 <= favorite[i] <= n - 1"
    assert all(f != i for i, f in enumerate(favorite)), "favorite[i] != i"
