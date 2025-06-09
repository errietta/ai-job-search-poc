from sqlalchemy import Integer


def query_dict_to_sqlalchemy(model, query, filter_dict):
    for key, value in filter_dict.items():
        if "__" in key:
            field, op = key.split("__", 1)
            col = getattr(model, field, None)
            if not col:
                continue
            if op == "ilike":
                query = query.filter(col.ilike(f"%{value}%"))
            elif op == "eq":
                query = query.filter(col == value)
            elif op == "gte":
                query = query.filter(col.cast(Integer) >= value)
            elif op == "lte":
                query = query.filter(col.cast(Integer) <= value)
        else:
            col = getattr(model, key, None)
            if not col:
                continue
            query = query.filter(col == value)

    return query
