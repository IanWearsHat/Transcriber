from abc import ABC, abstractmethod
from datetime import datetime

from vision import Vision
from enum import Enum


class IDNumType(Enum):
    MAWB = 1
    INTERNAL_REFERENCE = 2


# TODO: perhaps making everything lowercase before processing individual fields
# could make the vision better in case it reads some letter as lowercase
class BaseInvoice(ABC):
    """
    Add each field as its own method

    Each should return what is exactly inputted into FreightStream
    """

    STD_DATE_FORMAT = "%m/%d/%y"

    def __init__(self, path, orientation=0, pg_num=0):
        """All rects and formats should be defined in the subclass"""
        # TODO: table height might change depending on rows.
        # Whereas MKC has a constant space for every field,
        # HTC does not have a constant space for prices.
        # Meaning, the size and shape of the table changes for prices depending
        # on if there are 2 rows or 3 rows, or any number of rows
        self._prices_rect = None
        self._date_rect = None
        self._date_format = None
        self._invoice_num_rect = None
        self._id_num_rect = None

        self.path = path
        self.page_img = Vision.get_image(self.path)  # TODO: invoice might not be on page 0

    # in the future should have a config file of all the boxes for invoices
    # these should be automatically initialized from the file on class creation
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

    def format_date(self, text):
        date_obj = datetime.strptime(text, self._date_format)
        return date_obj.strftime(BaseInvoice.STD_DATE_FORMAT)

    def contains_num(self, string):
        for i in range(len(string)):
            if string[i].isdigit():
                return True

        return False
