from templates.base_invoice import BaseInvoice, IDNumType, VendorType
import vision


# has dynamically changing price table
class TextRKInvoice(BaseInvoice):
    def __init__(self, img, orientation=0, pg_num=0):
        super().__init__(img, orientation, pg_num)
        self._boxes = vision.get_relevant_boxes(img)

        self._prices_table_check_rect = [22, 43, 21, 125]
        self._info_table_check_rect = [22, 43, 21, 132]

        self._prices_table = self.get_prices_table()
        self._info_table = self.get_info_table()

        self._vendor_name_rect = [36, 70, 57, 408]
        self._prices_rect = self.get_price_rect()
        self._invoice_num_rect = [37, 64, 19, 120]
        self._id_num_rect = [79, 103, 434, 600]
        self._date_rect = [37, 59, 218, 328]

        self._date_format = '%m/%d/%y'
        self._name_on_invoice = 'ROBERT KONG CHB, INC.'
        self._freight_stream_internal_name = 'Robert Kong, CHB'
        self._vendor_type = VendorType.CUSTOMS

    def get_prices_table(self):
        for box in self._boxes:
            text = vision.get_text_from_cropped_rect_of_image(self._prices_table_check_rect, box, has_pixel_values=True)
            if 'description' in text.lower(): #TODO: fuzzy match
                box[:40, 0:len(box[1])] = (255)
                return box
        return None

    def get_info_table(self):
        for box in self._boxes:
            text = vision.get_text_from_cropped_rect_of_image(self._info_table_check_rect, box, has_pixel_values=True)
            if 'invoice' in text.lower():
                return box
        return None
    
    def get_name_on_invoice(self):
        return self._name_on_invoice

    def get_vendor_name(self):
        text = vision.get_text_from_cropped_rect_of_image(self._vendor_name_rect, self.page_img, has_pixel_values=True).strip()
        return text
    
    def get_price_rect(self):
        lines = vision.get_horizontal_lines(self._prices_table)

        lines.sort(key=lambda x: x[1])
        smallest = lines[0]
        for pt in lines:
            if pt[1] == smallest[1]:
                smallest = min(pt, smallest, key=lambda x: x[0])
            else:
                break

        largest = lines[-1]
        for i in range(len(lines)-1, -1, -1):
            if lines[i][1] == smallest[1]:
                largest = max(lines[i], smallest, key=lambda x: x[0])
            else:
                break
        
        # TODO: change to ratios
        return [smallest[1], largest[1], smallest[0], largest[0]]
    
    def get_prices(self) -> dict:
        # TODO: change has_pixel_values to false after changing prices rect to ratios
        prices_dict = {}

        text = vision.get_text_from_cropped_rect_of_image(self._prices_rect, self._prices_table, has_pixel_values=True).strip()
        for row in text.split('\n'):
            row = row.strip()
            dollar_i = row.rfind('$')
            price = row[dollar_i+1:].strip()
            category = row[:dollar_i].strip()
            prices_dict[category] = self.clean_price(price)
        
        return prices_dict

    def get_date(self):
        text = vision.get_text_from_cropped_rect_of_image(self._date_rect, self._info_table, has_pixel_values=True).strip()
        return self.format_date(text)
    
    def get_invoice_num(self):
        text = vision.get_text_from_cropped_rect_of_image(self._invoice_num_rect, self._info_table, has_pixel_values=True).strip()
        return text
    
    def get_id_num(self):
        text = vision.get_text_from_cropped_rect_of_image(self._id_num_rect, self._info_table, has_pixel_values=True).strip()
        return IDNumType.MAWB, text


__all__ = [TextRKInvoice.__name__]
