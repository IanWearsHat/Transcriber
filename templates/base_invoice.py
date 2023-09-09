from abc import ABC, abstractmethod
from vision import Vision

# TODO: perhaps making everything lowercase before processing individual fields
# could make the vision better in case it reads some letter as lowercase
class BaseInvoice(ABC):
    """
    Add each field as its own method

    Each should return what is exactly inputted into FreightStream
    """

    def __init__(self, path, orientation=0, pg_num=0):
        self._prices_rect = None
        self._date_rect = None
        self._invoice_num_rect = None
        self._id_num_rect = None

        self.path = path
        self.page_img = Vision.get_image(self.path)  # TODO: invoice might not be on page 0

    # in the future should have a config file of all the boxes for invoices
    # these should be automatically initialized from the file on class creation
    @abstractmethod
    def get_prices(self) -> dict:
        """Should determine Billing Code and any possible grouping of categories"""
        pass

    @abstractmethod
    def get_date(self):
        # TODO: needs a way to format dates correctly
        pass

    @abstractmethod
    def get_invoice_num(self):
        pass

    @abstractmethod
    def get_id_num(self):
        """Should be MAWB, but could be reference num or AWB"""
        pass
