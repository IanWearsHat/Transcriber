import time
import pyautogui as gui


# rename mawb to just awb
# also the thing should be clicking on hawb list, not mawb
class Inputter:
    # Main menu
    nav_bar_air_import_option_pt = (415, 45)
    mawb_list_dropdown_option_pt = (480, 104)

    # MAWB List
    reference_num_column_first_row_pt = (513, 165)
    mawb_num_column_first_row_pt = (366, 165)

    # Accounting
    account_payable_header_pt = (645, 590)

    # Account Payable
    vendor_field_pt = (288, 383)
    post_date_field_pt = (300, 410)
    invoice_date_field_pt = (470, 410)
    invoice_num_field_pt = (604, 383)
    billing_code_first_row_pt = (220, 500)
    price_first_row_pt = (845, 500)

    def __init__(self, data: dict):
        """
        Initializes all data needed to be inputted
        or checked by Inputter

        :param data
        dictionary of all data
        - vendor, date, and invoice num should be strings
        - rows should follow this format
        with a list being returned and each
        element representing a row with a billing_code
        and price:

        "rows": [
            {
                'billing_code': 'code',
                'price': 'test_price'
            }
        ]

        - id_num should be a tuple with the first element
        being the num type (ex. MAWB, Internal Reference Num)
        and the second element being the actual number
        """
        # self.vendor = data['vendor']
        # self.date = data['date']
        # self.invoice_num = data['invoice_num']
        # self.rows = data['rows']
        # self.id_num = data['id_num']
        self.vendor = ''
        self.date = ''
        self.invoice_num = ''
        self.id_num = ''

    def click_air_import(self):
        gui.click(*self.nav_bar_air_import_option_pt)

    def click_mawb_list(self):
        gui.click(*self.mawb_list_dropdown_option_pt)

    def search_mawb(self):
        # the invoice does not have a reference number
        # it should be the mawb, so use that instead
        # however, the other steps should be the same
        
        # click on reference number column
        # press F5
        # enter search term
        # press enter
        # top row will be the correct one
        # then hit F7

        # TODO: logic here to check if the given dictionary contains a MAWB or internal reference number
        gui.click(*self.mawb_num_column_first_row_pt)
        time.sleep(2)

        gui.press('f5')
        time.sleep(2)

        gui.write(self.id_num)
        time.sleep(0.5)

        gui.press('enter')

    def access_accounting(self):
        gui.press('f7')

    def click_account_payable_header(self):
        gui.click(*self.account_payable_header_pt)

    def access_account_payable(self):
        gui.press('f2')

    def check_existing_vendor_rows(self):
        pass

    def edit_vendor(self):
        # TODO: has to use % to search
        gui.click(*self.vendor_field_pt)
        gui.write(self.vendor)

    def edit_dates(self):
        # input post
        gui.click(*self.post_date_field_pt)
        gui.write(self.date)
        time.sleep(1)

        # input invoice date
        gui.click(*self.invoice_date_field_pt)
        gui.write(self.date)
        time.sleep(1)

    def edit_invoice_num(self):
        gui.click(*self.invoice_num_field_pt)
        gui.write(self.invoice_num)

    def edit_billing_code(self, x, y, billing_code):
        # TODO: have to type to search
        gui.click(x=x, y=y)
        gui.write(billing_code)

    def edit_item_description(self):
        # might not actually need to change this bc billing code
        # will autofill it
        gui.click(x=260, y=500)

    def edit_price(self, x, y, price):
        gui.click(x=x, y=y)
        gui.write(price)

    def edit_account_payable_row(self):
        # its own function because the y coordinate will change based on different rows
        # TODO: Change the y coordinate for each row
        # TODO: Detect if a row already exists
        x, y = self.billing_code_first_row_pt
        self.edit_billing_code(x, y, '')
        time.sleep(1)

        x, y = self.price_first_row_pt
        self.edit_price(x, y, '')
        time.sleep(1)

    def run_full_pipeline(self):
        # click air import
        # click Master AWB
        # search for awb
        # Type F7
        # Click on Account Payable header
        # click on existing row if vendor exists, then F2
        # To create new row, F2
        # Edit Account Payable Fields
        time.sleep(3)

        # Main screen
        self.click_air_import()
        time.sleep(1)

        self.click_mawb_list()
        time.sleep(4)

        # MAWB List screen
        self.search_mawb()
        time.sleep(5)

        # Accounting screen
        self.access_accounting()
        time.sleep(4)

        self.click_account_payable_header()
        time.sleep(1)

        # Account Payable screen
        self.access_account_payable()
        time.sleep(1)

        self.edit_vendor()
        time.sleep(1)

        self.edit_dates()
        time.sleep(1)

        self.edit_invoice_num()
        time.sleep(1)

        self.edit_account_payable_row()

        # TODO: DO NOT PRESS F12 TO SAVE BECAUSE THAT WILL MAKE CHANGES TO DB
        # TODO: but eventually you press F12


if __name__ == '__main__':
    bot = Inputter({})
    bot.run_full_pipeline()
