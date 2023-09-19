from templates.base_invoice import BaseInvoice, IDNumType, VendorType
import vision


# TODO: internally will change its internal vendor name if it sees hanoi or hochiminh
class TextAPSInvoice(BaseInvoice):
    def __init__(self, img, orientation=0, pg_num=0):
        super().__init__(img, orientation, pg_num)

        self._prices_table_check_rect = []
        self._prices_table = self.get_prices_table()

        self._prices_rect = self.get_price_rect()
        self._invoice_num_rect = None
        self._id_num_rect = None
        self._date_rect = None

        self._date_format = None
        self._name_on_invoice = None
        self._template_name = None
        self._freight_stream_internal_name = None
        self._vendor_type = None

    def get_prices_table(self):
        pass

    def get_price_rect(self):
        pass
    
    def get_name_on_invoice(self):
        return super().get_name_on_invoice()

    def get_vendor_name(self):
        return super().get_vendor_name()
    
    def get_prices(self) -> dict:
        return super().get_prices()
    
    def get_invoice_num(self):
        return super().get_invoice_num()
    
    def get_id_num(self):
        return super().get_id_num()
    
    def get_date(self):
        return super().get_date()
    
