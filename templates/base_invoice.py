from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum


class IDNumType(Enum):
    MAWB = 1
    INTERNAL_REFERENCE = 2


class VendorType(Enum):
    TRUCKING = 1
    CUSTOMS = 2
    AGENT = 3
    ISC = 4


# TODO: perhaps making everything lowercase before processing individual fields
# could make the vision better in case it reads some letter as lowercase
class BaseInvoice(ABC):
    """
    Add each field as its own method

    Each should return what is exactly inputted into FreightStream
    """

    STD_DATE_FORMAT = "%m%d%Y"

    def __init__(self, img, orientation=0, pg_num=0):
        """All rects and formats should be defined in the subclass"""
        # TODO: table height might change depending on rows.
        # Whereas MKC has a constant space for every field,
        # HTC does not have a constant space for prices.
        # Meaning, the size and shape of the table changes for prices depending
        # on if there are 2 rows or 3 rows, or any number of rows
        self.page_img = img

        self._vendor_name_rect = None
        self._prices_rect = None
        self._invoice_num_rect = None
        self._id_num_rect = None
        self._date_rect = None

        self._date_format = None
        self._name_on_invoice = None
        self._freight_stream_internal_name = None
        self._vendor_type = None

    @abstractmethod
    def get_name_on_invoice(self):
        pass

    # in the future should have a config file of all the boxes for invoices
    # these should be automatically initialized from the file on class creation
    @abstractmethod
    def get_vendor_name(self):
        pass

    @abstractmethod
    def get_prices(self) -> dict:
        """Should determine Billing Code and any possible grouping of categories"""
        # TODO: need a list of all codes
        pass

    @abstractmethod
    def get_invoice_num(self):
        pass

    @abstractmethod
    def get_id_num(self):
        """Should be MAWB, but could be reference num or AWB"""
        pass

    @abstractmethod
    def get_date(self):
        # A date format has to be loaded ex. for mkc its
        # date_str = '08/01/23'
        # date_format = '%m/%d/%y'
        #
        # date_obj = datetime.strptime(date_str, date_format)
        pass

    def get_data(self) -> dict:
        data = {
            "vendor": self._freight_stream_internal_name,
            "date": self.get_date(),
            "invoice_num": self.get_invoice_num(),
            "id_num": self.get_id_num(),
            "rows": self.determine_billing_codes_and_prices(
                self.get_prices()
            )
        }
        return data

    def clean_price(self, price: str):
        price = price.replace(',', "").replace('.', "")
        return price[:-2] + '.' + price[-2:]

    def format_date(self, text):
        try:
            date_obj = datetime.strptime(text, self._date_format)
        except ValueError:
            return None
        return date_obj.strftime(BaseInvoice.STD_DATE_FORMAT)

    def contains_num(self, string):
        for i in range(len(string)):
            if string[i].isdigit():
                return True

        return False

    def get_trucking_dict(self, prices_dict):
        price = sum(prices_dict.values())
        # TODO: If trucking, the prices rect should be the total price and just return that as the price
        # instead of having to add them in this sum
        return {"AITRUCK": price}

    def get_customs_dict(self, prices_dict):
        clearance_fee = 0
        duty = 0
        for category, price in prices_dict.items():
            cleaned = category.lower()
            if 'duti' in cleaned or 'duty' in cleaned:
                duty = float(price)
            else:
                clearance_fee += float(price)

        code_dict = {}
        if duty != 0:
            code_dict.update({
                "AI-DUTY": duty
            })

        if clearance_fee != 0:
            code_dict.update({
                "AICUSTOM": clearance_fee
            })

        return code_dict

    def get_agent_dict(self, prices_dict):
        air_freight = 0
        profit = 0
        other = 0
        for category, price in prices_dict.items():
            cleaned = category.lower()

            if 'freight' in cleaned:
                air_freight = float(price)
            elif 'profit' in cleaned:
                profit = float(price)
            else:
                other += float(price)

        code_dict = {
            "AI1AIRFRT": air_freight,
            "AIPROFIT": profit
        }
        if other != 0:
            code_dict.update({
                "AI-ORIGIN": other
            })

        return code_dict
    
    def change_floats_to_strings(self, in_dict):
        for code in in_dict.keys():
            in_dict[code] = str(in_dict[code])

    def determine_billing_codes_and_prices(self, prices_dict) -> dict:
        return_dict = None
        if self._vendor_type == VendorType.TRUCKING:
            return_dict = self.get_trucking_dict(prices_dict)
        elif self._vendor_type == VendorType.CUSTOMS:
            return_dict = self.get_customs_dict(prices_dict)
        elif self._vendor_type == VendorType.AGENT:
            return_dict = self.get_agent_dict(prices_dict)
        elif self._vendor_type == VendorType.ISC:
            pass
        
        self.change_floats_to_strings(return_dict)
    
        return return_dict
