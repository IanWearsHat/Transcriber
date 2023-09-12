from datetime import datetime
from templates.base_invoice import BaseInvoice


def validate_data(data):
    if data['vendor'] is not str or \
            data['invoice_num'] is not str or \
            data['id_num'] is not str:
        raise TypeError

    try:
        datetime.strptime(data['date'], BaseInvoice.STD_DATE_FORMAT)
    except ValueError:
        raise ValueError("Date is not in standard format defined in BaseInvoice.")

    if data['rows'] is not list:
        raise TypeError

    for row in data['rows']:
        if row['billing_code'] is not int or \
                not row['price'].isnumeric():
            raise TypeError
