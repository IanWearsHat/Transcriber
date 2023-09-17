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
    reference_num_column_first_row_pt = (513, 165)
    mawb_num_column_first_row_pt = (1011, 165)

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

        "rows": {
            'billing_code': price
        }

        - id_num should be a tuple with the first element
        being the num type (ex. MAWB, Internal Reference Num)
        and the second element being the actual number

        ex.
            data = {
                "vendor": 'MKC CUSTOMS BROKERS',
                "date": '072823',
                "invoice_num": '0604751',
                "rows": {
                        "AICUSTOM": "23",
                        "AI-DUTY": "32"
                },
                "id_num": (IDNumType.MAWB, '15792303271')
            }
        """

        # TODO: date should have no slashes and just have numbers
        
        self.vendor = data['vendor']
        self.date = data['date']
        self.invoice_num = data['invoice_num']
        self.price_rows = data['rows']
        self.id_num_type = data['id_num'][0]
        self.id_num = data['id_num'][1]

    def click_air_import(self):
        gui.click(*self.nav_bar_air_import_option_pt)

    def click_hawb_list(self):
        gui.click(*self.hawb_list_dropdown_option_pt)

    def search_id(self):  
        # click on reference number column
        # press F5
        # enter search term
        # press enter
        # top row will be the correct one
        # then hit F7

        if self.id_num_type == IDNumType.MAWB:
            gui.click(*self.mawb_num_column_first_row_pt)
        elif self.id_num_type == IDNumType.INTERNAL_REFERENCE:
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

    def click_billing_code_field(self):
        gui.click(*self.billing_code_first_row_pt)

    def edit_billing_code(self, billing_code):
        gui.write(billing_code, interval=0.2)

    def edit_price(self, price):
        gui.write(price, interval=0.2)

    def edit_account_payable_row(self):
        # TODO: Detect if a row already exists

        self.click_billing_code_field()

        for code, price in self.price_rows.items():
            self.edit_billing_code(code)
            time.sleep(1)

            gui.press('tab', presses=2, interval=0.1)
            time.sleep(1)

            self.edit_price(price)
            time.sleep(1)

            gui.press('tab', presses=3, interval=0.1)
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

        print("RUNNING INPUTTER")
        print(self.vendor)
        print(self.date)
        print(self.invoice_num)
        print(self.id_num_type)
        print(self.id_num)
        print(self.price_rows)

        # time.sleep(3)

        # # Main screen
        # self.click_air_import()
        # time.sleep(1)

        # self.click_hawb_list()
        # time.sleep(5)

        # # HAWB List screen
        # self.search_id()
        # time.sleep(5)

        # # Accounting screen
        # self.access_accounting()
        # time.sleep(5)

        # self.click_account_payable_header()
        # time.sleep(1)

        # # Account Payable screen
        # self.access_account_payable()
        # time.sleep(3)

        # self.edit_vendor()
        # time.sleep(2)

        # self.edit_dates()
        # time.sleep(1)

        # self.edit_invoice_num()
        # time.sleep(1)

        # self.edit_account_payable_row()

        # TODO: DO NOT PRESS F12 TO SAVE BECAUSE THAT WILL MAKE CHANGES TO DB
        # TODO: but eventually you press F12


if __name__ == '__main__':
    bot = Inputter({})
    time.sleep(3)
    bot.run_full_pipeline()

    debug = False
    if debug:
        # Main screen
        bot.click_air_import()
        time.sleep(1)

        bot.click_hawb_list()
        time.sleep(5)

        # HAWB List screen
        bot.search_id()
        time.sleep(5)

        # Accounting screen
        bot.access_accounting()
        time.sleep(5)

        bot.click_account_payable_header()
        time.sleep(1)

        # Account Payable screen
        bot.access_account_payable()
        time.sleep(3)

        bot.edit_vendor()
        time.sleep(2)

        bot.edit_dates()
        time.sleep(1)

        bot.edit_invoice_num()
        time.sleep(1)

        bot.edit_account_payable_row()
