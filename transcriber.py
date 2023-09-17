import templates
from templates.base_invoice import BaseInvoice, IDNumType, VendorType
import vision
from validation import validate_data
from inputter import Inputter


def _validate_vendor_name(template):
    # Vendor name should be in the correct spot
    intended_name = template.get_template_name()
    vendor_name = template.get_vendor_name()

    if intended_name != vendor_name:  # TODO: perhaps fuzzy match here
        raise ValueError


def _validate_prices(template):
    # Prices should all be numeric
    prices = template.get_prices()
    for price in prices.values():
        if not price.replace('.', '').isnumeric():
            raise ValueError


def _validate_id_num(template):
    # id num should be in a format depending on whether it uses MAWB, HAWB, or Internal Ref Num
    id_type, id_num = template.get_id_num()
    if id_type == IDNumType.MAWB:
        if not id_num.isnumeric() and len(id_num) != 11:
            raise ValueError
    elif id_type == IDNumType.INTERNAL_REFERENCE:
        if id_num[:3] != 'LAI' and not id_num[3:].isnumeric() and len(id_num) != 11:
            raise ValueError


def _validate_date(template):
    # Date should not be None
    date = template.get_date()
    if date is None:
        raise ValueError


def determine_invoice_template(path):
    template_gen = (cls for cls in templates.__dict__.values() if isinstance(cls, type))
    for template_cls in template_gen:
        img = vision.get_image(path)  # TODO: invoice might not be on page 0

        template_obj = template_cls(img)

        try:
            _validate_vendor_name(template_obj)
            _validate_prices(template_obj)
            _validate_id_num(template_obj)
            _validate_date(template_obj)

            return template_obj
        except ValueError:
            continue

    return None


def transcribe(path):
    inv_cls = determine_invoice_template(path)

    if inv_cls is not None:
        inv_data = inv_cls.get_data()
        validate_data(inv_data)

        return inv_data


if __name__ == '__main__':
    path = r"C:\Users\ianbb\PycharmProjects\FreightStreamTranscriber\pdfExamples\MKC\Invoice-0604764.pdf"
    inv_obj = determine_invoice_template(path)
    print(inv_obj.get_data())
