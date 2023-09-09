from templates.base_invoice import BaseInvoice


class TextDartInvoice(BaseInvoice):
    """
    Class representing how to handle Dart's text invoice format

    Best case scenario as shown in VNM00042074
    """
    def clean_price(self, price: str):
        price = price.replace(',', "").replace('.', "")
        return price[:-2] + '.' + price[-2:]

    def get_prices(self) -> dict:
        pass

    def get_date(self):
        pass

    def get_invoice_num(self):
        pass

    def get_id_num(self):
        pass


__all__ = [TextDartInvoice.__name__]
