from templates.base_invoice import BaseInvoice, IDNumType, VendorType
import vision


# internally will change its internal vendor name if it sees hanoi or hochiminh
class TextAPSInvoice(BaseInvoice):
    def __init__(self, img, orientation=0, pg_num=0):
        super().__init__(img, orientation, pg_num)
        self._boxes = vision.get_relevant_boxes(img)

        self._prices_table_check_rect = [21, 44, 200, 352]
        self._prices_table = self.get_prices_table()

        self._vendor_name_rect = [38, 62, 447, 873]
        self._prices_rect = self.get_price_rect()
        self._invoice_num_rect = [233, 258, 722, 882]
        self._id_num_rect = [353, 380, 722, 882]
        self._date_rect = [263, 282, 722, 882]

        self._date_format = '%d/%m/%Y'
        self._name_on_invoice = None
        self._freight_stream_internal_name = self.determine_name()
        self._vendor_type = VendorType.AGENT

    def get_prices_table(self):
        for box in self._boxes:
            text = vision.get_text_from_cropped_rect_of_image(self._prices_table_check_rect, box, has_pixel_values=True)
            if 'description' in text.lower():
                box[:40, 0:len(box[1])] = (255)
                box[-40:, 0:len(box[1])] = (255)
                return box
        return None

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
    
    def determine_name(self):
        text = vision.get_text_from_cropped_rect_of_image(self._vendor_name_rect, self.page_img, has_pixel_values=True).strip()
        if 'hanoi' in text.lower():
            return 'APS South East Asia Co., Ltd.'
        else:
            return 'APS South East Asia Co., Ltd. (Hochiminh)'

    def get_name_on_invoice(self):
        return self._freight_stream_internal_name

    def get_vendor_name(self):
        #TODO: there is a thailand office
        return self._freight_stream_internal_name
    
    def get_prices(self) -> dict:
        start_y = self._prices_rect[0]
        end_y = self._prices_rect[1]

        category_start_x = 73
        category_end_x = 471
        category_rect = [start_y, end_y, category_start_x, category_end_x]

        price_start_x = 767
        price_end_x = 902
        prices_rect = [start_y, end_y, price_start_x, price_end_x]

        categories = []
        text = vision.get_text_from_cropped_rect_of_image(category_rect, self._prices_table, has_pixel_values=True)
        for row in text.split('\n'):
            row = row.strip()
            if row:
                categories.append(row)
        
        prices = []
        text = vision.get_text_from_cropped_rect_of_image(prices_rect, self._prices_table, has_pixel_values=True)
        for row in text.split('\n'):
            row = row.strip()
            if row:
                prices.append(row)

        return dict(zip(categories, prices))
    
    def get_date(self):
        text = vision.get_text_from_cropped_rect_of_image(self._date_rect, self.page_img, has_pixel_values=True).strip()
        return self.format_date(text)
    
    def get_invoice_num(self):
        text = vision.get_text_from_cropped_rect_of_image(self._invoice_num_rect, self.page_img, has_pixel_values=True).strip()
        return text
    
    def get_id_num(self):
        text = vision.get_text_from_cropped_rect_of_image(self._id_num_rect, self.page_img, has_pixel_values=True).strip()
        return IDNumType.MAWB, text.replace('-', '')
    

__all__ = [TextAPSInvoice.__name__]
