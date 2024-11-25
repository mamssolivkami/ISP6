def geom_avg(iterable):
    i = 0
    prod = 1

    for item in iterable:
        prod *= item
        i += 1

    if i == 0:
        return None

    return pow(prod, 1 / i)


def sum_product(*collections):
    pivot_collection = collections[0]
    res_sum = 0

    indices = pivot_collection.keys() \
        if isinstance(pivot_collection, dict) \
        else range(len(pivot_collection))

    for i in indices:
        product = 1

        for d in collections:
            product *= d[i]

        res_sum += product

    return res_sum
