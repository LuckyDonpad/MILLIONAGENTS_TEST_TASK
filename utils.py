PAGE_ARGUMENT = 'page'
PAGE_QUERY = f"{PAGE_ARGUMENT}="


def get_next_page(url: str) -> str:
    page_num_index = url.find(PAGE_QUERY)
    if not page_num_index == -1:
        page_num =  url[page_num_index + len(PAGE_QUERY)]
        return url.replace(PAGE_QUERY+page_num, PAGE_QUERY + f"{int(page_num) + 1}")
    return f"{url}&{PAGE_QUERY}2"
