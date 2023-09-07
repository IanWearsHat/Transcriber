from invoices.base_invoice import BaseInvoice


class TextDartInvoice(BaseInvoice):
    """
    Class representing how to handle Dart's text invoice format

    Best case scenario as shown in VNM00042074
    """
    def clean_price(self, price: str):
        price = price.replace(',', "").replace('.', "")
        return price[:-2] + '.' + price[-2:]

    def get_prices(self) -> dict:
        prices = {}

        sub = self.get_substring('DESCRIPTION CHARGES IN USD', 'TOTAL CHARGES')

        for row in sub.split('\n'):
            name_start = row.find('(')
            name_end = row.find(')')
            name = row[name_start+1:name_end]

            price = row.split()[-1]
            price = self.clean_price(price)

            prices[name] = price

        return prices

    def get_date(self):
        sub = self.get_substring('INVOICE DATE', 'CUSTOMER ID')
        sub = sub.split('-')
        return ' '.join([sub[1], sub[0], sub[2]])

        # TODO: the date could be the due date too, right now it's only the invoice date

    def get_invoice_num(self):
        sub = self.get_substring('INVOICE', 'Page 1 of ')
        return sub


__all__ = [TextDartInvoice.__name__]
