import time
import pyautogui as gui

# rename mawb to just awb
# also the thing should be clicking on hawb list, not mawb
class Inputter:
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
        """
        # self.vendor = data['vendor']
        # self.date = data['date']
        # self.invoice_num = data['invoice_num']
        # self.rows = data['rows']
        self.vendor = ''
        self.date = ''
        self.invoice_num = ''

    def click_air_import(self):
        gui.click(x=415, y=45)

    def click_mawb_list(self):
        gui.click(x=480, y=104)

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
        gui.click(x=513, y=165)
        time.sleep(2)
        gui.press('f5')
        time.sleep(2)
        gui.write('LAI23070046')
        time.sleep(0.5)
        gui.press('enter')
        time.sleep(4)

    def access_accounting(self):
        gui.press('f7')

    def click_account_payable_header(self):
        gui.click(x=645, y=590)

    def access_account_payable(self):
        gui.press('f2')

    def check_existing_vendor_rows(self):
        pass

    def edit_vendor(self):
        # has to use % to search
        gui.click(x=288, y=383)
        gui.write(self.vendor)

    def edit_dates(self):
        # input post
        gui.click(x=300, y=410)
        gui.write(self.date)
        time.sleep(1)
        # input invoice date
        gui.click(x=470, y=410)
        gui.write(self.date)
        time.sleep(1)

    def edit_invoice_num(self):
        gui.click(x=604, y=383)
        gui.write(self.invoice_num)

    def edit_billing_code(self, billing_code):
        # have to either scroll or type to search
        # might need a list of all codes
        gui.click(x=220, y=500)
        gui.write(billing_code)

    def edit_item_description(self):
        # might not actually need to change this bc billing code
        # will autofill it
        gui.click(x=260, y=500)

    def edit_price(self, price):
        gui.click(x=845, y=500)
        gui.write(price)

    def edit_account_payable_row(self):
        # its own function because the y coordinate will change based on different rows
        time.sleep(1)
        self.edit_billing_code('')

        time.sleep(1)
        self.edit_price('')

    def run_full_pipeline(self):
        # click air import
        # click Master AWB
        # search for awb
        # Type F7
        # Click on Account Payable header
        # click on existing row if vendor exists, then F2
        # To create new row, F2
        # Edit Account Payable Fields

        # Main screen
        time.sleep(3)
        self.click_air_import()

        time.sleep(1)
        self.click_mawb_list()

        # MAWB List screen
        time.sleep(4)
        self.search_mawb()

        # Accounting screen
        time.sleep(1)
        self.access_accounting()

        time.sleep(4)
        self.click_account_payable_header()

        # Account Payable screen
        time.sleep(1)
        self.access_account_payable()

        time.sleep(1)
        self.edit_vendor()

        time.sleep(1)
        self.edit_dates()

        time.sleep(1)
        self.edit_invoice_num()

        self.edit_account_payable_row()

        # TODO: DO NOT PRESS F12 TO SAVE BECAUSE THAT WILL MAKE CHANGES TO DB
        # TODO: but eventually you press F12


if __name__ == '__main__':
    bot = Inputter({})
    bot.run_full_pipeline()
