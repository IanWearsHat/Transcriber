from datetime import datetime
from templates.base_invoice import BaseInvoice, IDNumType


def validate_data(data):
    if type(data['vendor']) is not str or \
            type(data['id_num'][0]) is not IDNumType or \
            type(data['id_num'][1]) is not str or \
            type(data['invoice_num']) is not str:
        raise TypeError("Vendor, invoice num, or id num is not string.")

    try:
        datetime.strptime(data['date'], BaseInvoice.STD_DATE_FORMAT)
    except ValueError:
        raise ValueError("Date is not in standard format defined in BaseInvoice.")

    if type(data['rows']) is not dict:
        raise TypeError("Rows should be dict.")

    for billing_code, price in data['rows'].items():
        if type(billing_code) is not str or \
                not price.replace('.', '').isnumeric():
            raise TypeError("Billing code should be string and price should be numeric")
