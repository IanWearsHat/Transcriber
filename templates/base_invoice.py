from abc import ABC, abstractmethod
from PyPDF2 import PdfReader
import uuid

class BaseInvoice(ABC):
    """
    Add each field as its own method

    Each should return what is exactly inputted into FreightStream
    """

    def __init__(self, path, orientation=0, pg_num=0):
        self.path = path
        self.reader = PdfReader(path)
        page = self.reader.pages[pg_num]
        self.text = page.extract_text(orientation)

    def write_text_to_file(self):
        with open(self.path + ".txt", 'w', encoding='utf-8') as f:
            f.write(self.text)

    def get_substring(self, start, end):
        start_i = self.text.find(start) + len(start)
        end_i = self.text.find(end)
        return self.text[start_i:end_i].strip()

    @abstractmethod
    def get_prices(self) -> dict:
        pass

    @abstractmethod
    def get_date(self):
        pass

    @abstractmethod
    def get_invoice_num(self):
        pass

    @abstractmethod
    def get_id_num(self):
        """Should be MAWB, but could be reference num or AWB"""
        pass
