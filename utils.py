import fake_useragent

PAGE_ARGUMENT = 'page'
PAGE_QUERY = f"{PAGE_ARGUMENT}="

DEFAULT_COOKIE = {'_slid_server': '6713754d890d8b1038019b42',
                  '_slsession': '1F5FD8D1-7568-469A-A8F0-B4748E0B42DF',
                  'coords': '55.875753%2637.447279',
                  'exp_auth': '3Rd5fv0vTUylyTasdzAcqA.1',
                  'is18Confirmed': 'false',
                  'metroStoreId': '10',
                  'pdp_abc_20': '1',
                  'plp_bmpl_bage': '1'}


def get_next_page(url: str) -> str:
    page_num_index = url.find(PAGE_QUERY)
    if not page_num_index == -1:
        page_num = url[page_num_index + len(PAGE_QUERY)]
        return url.replace(PAGE_QUERY + page_num, PAGE_QUERY + f"{int(page_num) + 1}")
    return f"{url}&{PAGE_QUERY}2"


def get_fake_user_agent():
    user_agent = fake_useragent.UserAgent().random
    headers = {"User-Agent": user_agent}
    return headers


def get_pages_url(url: str, count: int) -> list[str]:
    base_url = url
    urls = []
    for i in range(1, count):
        base_url = get_next_page(base_url)
        urls.append(base_url)
    return urls


def get_cookie_from_args(coords: str, id: str) -> dict:
    cookie = DEFAULT_COOKIE
    cookie['coords'] = coords
    cookie['metroStoreId'] = id
    return cookie


async def download_task(index: int, url: str, session, path: str):
    async with session.get(url=url, headers=get_fake_user_agent()) as response:
        response_text = await response.text()
    with open(f"{path}/page_{index}.html", "w", encoding="utf-8") as file:
        file.write(response_text)
