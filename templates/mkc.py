from templates.base_invoice import BaseInvoice, IDNumType, VendorType
import vision


class TextMKCInvoice(BaseInvoice):
    def __init__(self, path, orientation=0, pg_num=0):
        super().__init__(path, orientation, pg_num)
        # TODO: These rects should be read from a config file
        self._vendor_name_rect = [0.05606060606060606, 0.07196969696969698, 0.5843137254901961, 0.7745098039215687]
        self._prices_rect = [0.5143939393939394, 0.803030303030303, 0.07549019607843137, 0.9372549019607843]
        self._id_num_rect = [0.39090909090909093, 0.4121212121212121, 0.08823529411764706, 0.9137254901960784]
        self._invoice_num_rect = [0.21818181818181817, 0.23333333333333334, 0.5901960784313726, 0.7627450980392156]
        self._date_rect = [0.21893939393939393, 0.2356060606060606, 0.7637254901960784, 0.9392156862745098]

        self._date_format = '%m/%d/%y'

        self._name_on_invoice = 'MKC CUSTOMS BROKERS'
        self.__freight_stream_internal_name = "MKC CUSTOMS BROKERS INT'L. CO."
        self._vendor_type = VendorType.CUSTOMS

    def get_name_on_invoice(self):
        return self._name_on_invoice

    def get_vendor_name(self):
        text = vision.get_text_from_cropped_rect_of_image(self._vendor_name_rect, self.page_img).strip()
        return text

    def get_prices(self) -> dict:
        prices_dict = {}

        text = vision.get_text_from_cropped_rect_of_image(self._prices_rect, self.page_img).strip()
        for row in text.split('\n'):
            row = row.strip()
            last_space_i = row.rfind(' ')
            price = row[last_space_i:].strip()
            category = row[:last_space_i].strip()
            prices_dict[category] = self.clean_price(price)

        return prices_dict

    def get_date(self):
        text = vision.get_text_from_cropped_rect_of_image(self._date_rect, self.page_img).strip()
        return self.format_date(text)

    def get_invoice_num(self):
        text = vision.get_text_from_cropped_rect_of_image(self._invoice_num_rect, self.page_img).strip()
        return text

    def get_id_num(self):
        # finding mawb
        text = vision.get_text_from_cropped_rect_of_image(self._id_num_rect, self.page_img).strip()
        split_text = text.split()
        for i in range(len(split_text)):
            if self.contains_num(split_text[i]) and split_text[i-1].find("Master") != -1:
                return IDNumType.MAWB, split_text[i].replace(',', '').replace(':', ' ')

    def get_data(self) -> dict:
        data = {
            "vendor": self.__freight_stream_internal_name,
            "date": self.get_date(),
            "invoice_num": self.get_invoice_num(),
            "id_num": self.get_id_num(),
            "rows": self.determine_billing_codes_and_prices(
                self.get_prices()
            )
        }
        return data


__all__ = [TextMKCInvoice.__name__]
