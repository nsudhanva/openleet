"""Apply Discount Every n Orders: a Cashier constructor and getBill calls."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and ops, "ops and args are parallel"
    assert ops[0] == "Cashier" and len(args[0]) == 4, "Cashier(n, discount, products, prices)"
    n, discount, products, prices = args[0]
    assert 1 <= n <= 10**4, "1 <= n <= 10^4"
    assert 0 <= discount <= 100, "0 <= discount <= 100"
    assert 1 <= len(products) <= 200, "1 <= products.length <= 200"
    assert len(prices) == len(products), "prices.length == products.length"
    assert all(1 <= p <= 200 for p in products), "1 <= products[i] <= 200"
    assert all(1 <= p <= 1000 for p in prices), "1 <= prices[i] <= 1000"
    assert len(set(products)) == len(products), "The elements in products are unique"
    assert len(ops) - 1 <= 1000, "At most 1000 calls will be made to getBill"
    known = set(products)
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert op == "getBill" and len(a) == 2, "getBill(product, amount)"
        product, amount = a
        assert 1 <= len(product) <= len(products), "1 <= product.length <= products.length"
        assert len(amount) == len(product), "amount.length == product.length"
        assert all(p in known for p in product), "product[j] exists in products"
        assert all(1 <= m <= 1000 for m in amount), "1 <= amount[j] <= 1000"
        assert len(set(product)) == len(product), "The elements of product are unique"
