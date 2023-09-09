from templates.base_invoice import BaseInvoice
from vision import Vision


class TextMKCInvoice(BaseInvoice):
    def __init__(self, path, orientation=0, pg_num=0):
        super().__init__(path, orientation, pg_num)
        self._prices_rect = [679, 1060, 77, 956]  # should be a ratio from file in case dpi changes
        self._id_num_rect = [516, 544, 90, 932]
        self._date_rect = [289, 311, 779, 958]
        self._invoice_num_rect = [288, 308, 602, 778]

    def get_prices(self) -> dict:
        prices_dict = {}

        text = Vision.get_text_from_cropped_rect_of_image(self._prices_rect, self.page_img)
        text = text.strip()
        for row in text.split('\n'):
            row = row.strip()
            last_space_i = row.rfind(' ')
            price = row[last_space_i:].strip()
            category = row[:last_space_i].strip()
            prices_dict[category] = price

        # determining billing code and any possible combining of categories
        # should be done here
        return prices_dict

    def get_date(self):
        text = Vision.get_text_from_cropped_rect_of_image(self._date_rect, self.page_img).strip()
        return text

    def get_invoice_num(self):
        text = Vision.get_text_from_cropped_rect_of_image(self._invoice_num_rect, self.page_img).strip()
        return text

    def get_id_num(self):
        # finding mawb
        text = Vision.get_text_from_cropped_rect_of_image(self._id_num_rect, self.page_img).strip()
        split_text = text.split()
        for i in range(len(split_text)):
            if self.contains_num(split_text[i]) and split_text[i-1].find("Master") != -1:
                return split_text[i].replace(',', '').replace(':', ' ')

    def contains_num(self, string):
        for i in range(len(string)):
            if string[i].isdigit():
                return True

        return False


__all__ = [TextMKCInvoice.__name__]


if __name__ == '__main__':
    inv = TextMKCInvoice(r"C:\Users\ianbb\PycharmProjects\FreightStreamTranscriber\pdfExamples\MKC\Invoice-0604751.pdf")
    print(inv.get_prices())
    print(inv.get_id_num())
    print(inv.get_date())
    print(inv.get_invoice_num())
