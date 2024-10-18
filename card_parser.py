class CardParser:
    @staticmethod
    def parse(card, brands):
        name = CardParser.parse_name(card)
        link = CardParser.parse_link(card)
        actual_price = CardParser.parse_actual_price(card)
        old_price = CardParser.parse_old_price(card)
        id = link.split('/')[-1]
        brand = CardParser.parse_brand(brands,name)
        res = {'name':name,
               'link':link,
               'actual_price':actual_price,
               'old_price':old_price,
               'id':id,
               'brand':brand}
        return res

    @staticmethod
    def parse_link(card):
        return card.find('a', class_="product-card-photo__link reset-link")['href']

    @staticmethod
    def parse_name(card):
        return card.find('span', class_="product-card-name__text").text.strip()

    @staticmethod
    def parse_actual_price(card):
        actual_price = card.find('div', class_="product-unit-prices__actual-wrapper")
        actual_price_rubs = actual_price.find('span', class_="product-price__sum-rubles")
        actual_price_rubs = ("".join(actual_price_rubs.text.split()))

        actual_price_penny = actual_price.find("span", class_="product-price__sum-penny")
        if actual_price_penny:
            actual_price_penny = ("".join(actual_price_penny.text.split()))
            return actual_price_rubs + actual_price_penny
        else:
            return actual_price_rubs

    @staticmethod
    def parse_old_price(card):
        old_price = card.find('div', class_="product-unit-prices__old-wrapper")
        if not old_price:
            return None

        old_price_rubs = old_price.find('span', class_="product-price__sum-rubles")
        if not old_price_rubs:
            return None

        old_price_rubs = ("".join(old_price_rubs.text.split()))
        old_price_penny = old_price.find("span", class_="product-price__sum-penny")
        if old_price_penny:
            old_price_penny = ("".join(old_price_penny.text.split()))
            return old_price_rubs + old_price_penny
        else:
            return old_price_rubs

    @staticmethod
    def parse_brand(brands: str, name: str) -> str:
        for brand in brands:
            if brand in name.upper():
                return brand
        return None
