def get_pagination_urls(base_url, skip, limit, filter, total):
    params = []
    if filter:
        params.append(f"filter={filter}")
    if limit:
        params.append(f"limit={limit}")

    def build_url(skip_value):
        param_str = "&".join(params + [f"skip={skip_value}"])
        return f"{base_url}?{param_str}"

    next_page = build_url(skip + limit) if skip + limit < total else None
    prev_page = build_url(max(skip - limit, 0)) if skip > 0 else None
    return next_page, prev_page
