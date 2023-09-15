import time
import pyautogui as gui
from templates.base_invoice import IDNumType


# rename mawb to just awb
# also the thing should be clicking on hawb list, not mawb
class Inputter:
    # Main menu
    nav_bar_air_import_option_pt = (415, 45)
    hawb_list_dropdown_option_pt = (480, 108)

    # HAWB List
    # TODO: These 2 are not correct, they have to be in the HAWB list
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
                'billing_code': price
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

    def click_hawb_list(self):
        gui.click(*self.hawb_list_dropdown_option_pt)

    def search_id(self):
        # the invoice does not have a reference number
        # it should be the mawb, so use that instead
        # however, the other steps should be the same
        
        # click on reference number column
        # press F5
        # enter search term
        # press enter
        # top row will be the correct one
        # then hit F7

        if self.id_num[0] == IDNumType.MAWB:
            gui.click(*self.mawb_num_column_first_row_pt)
        elif self.id_num[0] == IDNumType.INTERNAL_REFERENCE:
            gui.click(*self.reference_num_column_first_row_pt)
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
        # TODO: implement this check

        # TODO: Handling duplicate pdfs could be checked here
        # meaning if there is an existing vendor row, then there is a duplicate pdf (or the pdf has already been inputted)
        # and then the program would stop here.
        #
        # It would be a problem if there were so many pdfs coming in, but because a pdf might come in only every 5 hours
        # or so, it doesn't matter if the program stops to check.
        # also, this program would run when the computer is not being used, so it doesn't really matter how long it takes
        # for the bot to determine whether the pdf has been inputted or not.
        pass

    def edit_vendor(self):
        gui.click(*self.vendor_field_pt)
        gui.write('%' + self.vendor)
        time.sleep(1)

        gui.press('enter')
        time.sleep(4)

        # TODO: If needed, OCR the entire column of names and choose from that
        # click on the first row
        gui.click(*self.reference_num_column_first_row_pt, clicks=2, interval=0.25)
        time.sleep(4)

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
        time.sleep(1)

        gui.press('enter')

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
        # TODO: row might be the same height as in vision, which is 22
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

        self.click_hawb_list()
        time.sleep(4)

        # HAWB List screen
        self.search_id()
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