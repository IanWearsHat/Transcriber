from templates.base_invoice import BaseInvoice


class TextDartInvoice(BaseInvoice):
    """
    Class representing how to handle Dart's text invoice format

    Best case scenario as shown in VNM00042074
    """
    def get_template_name(self):
        return 'Dart'

    def get_vendor_name(self):
        pass

    def get_prices(self) -> dict:
        pass

    def get_date(self):
        return 'hi'

    def get_invoice_num(self):
        pass

    def get_id_num(self):
        pass


__all__ = [TextDartInvoice.__name__]
