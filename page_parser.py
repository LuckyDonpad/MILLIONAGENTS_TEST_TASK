class PageParser:
    @staticmethod
    def parse_cards(soup):
        cards = soup.find_all('div', class_='product-card__content')
        return cards

    @staticmethod
    def parse_brands(soup):
        brands = soup.find('div', class_="catalog-filters-manufacturer")
        brands = brands.find_all('a', class_="catalog-checkbox__seo-link")
        result = []
        for brand in brands:
            result.append(brand.text.strip())
        return result

    @staticmethod
    def parse_pagecount(soup):
        pages = soup.find_all(class_="v-pagination__item catalog-paginate__item")
        pagecount = int(pages[-1].text)
        return pagecount
