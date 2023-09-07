import unittest

from templates.dart import TextDartInvoice


class TextDartTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.paths = [
            r"C:\Users\ianbb\PycharmProjects\FreightStreamTranscriber\pdfExamples\Dart\INVOICE - VNM00042074 - CONINT_US (05-Dec-22).PDF",
            r"C:\Users\ianbb\PycharmProjects\FreightStreamTranscriber\pdfExamples\Dart\INVOICE - VNM00045559 - CONINT_US (30-Aug-23).PDF",
            r"C:\Users\ianbb\PycharmProjects\FreightStreamTranscriber\pdfExamples\Dart\INVOICE - VNM00045632 - CONINT_US (31-Aug-23).PDF",
            r"C:\Users\ianbb\PycharmProjects\FreightStreamTranscriber\pdfExamples\Dart\INVOICE - VNM00045640 - CONINT_US (31-Aug-23).PDF",
            r"C:\Users\ianbb\PycharmProjects\FreightStreamTranscriber\pdfExamples\Dart\INVOICE - VNM00045687 - CONINT_US (31-Aug-23).PDF"
        ]
        cls.price_names = ['International Freight', 'Handling Charges']
        cls.prices = [
            ['3816.00', '238.50'],
            ['465.36', '19.55'],
            ['242.62', '21.60'],
            ['1854.65', '108.50'],
            ['1314.18', '103.91']
        ]
        cls.dates = [
            'Dec 05 22',
            'Aug 30 23',
            'Aug 31 23',
            'Aug 31 23',
            'Aug 31 23'
        ]
        cls.invoice_nums = [
            'VNM00042074',
            'VNM00045559',
            'VNM00045632',
            'VNM00045640',
            'VNM00045687'
        ]
        cls.ids = [
            '60724323994',
            '12555500981',
            '73855645741',
            '21793168950',
            '61866049885'
        ]

    def test_all_prices_are_correct(self):
        for i in range(len(self.paths)):
            inv = TextDartInvoice(self.paths[i])
            test_prices = inv.get_prices()
            exp_prices = self.prices[i]

            for pair_i in range(len(self.price_names)):
                name = self.price_names[pair_i]
                price = exp_prices[pair_i]
                self.assertEqual(test_prices[name], price)

    def test_all_dates_are_correct(self):
        for i in range(len(self.paths)):
            inv = TextDartInvoice(self.paths[i])
            self.assertEqual(inv.get_date(), self.dates[i])

    def test_all_invoice_nums_are_correct(self):
        for i in range(len(self.paths)):
            inv = TextDartInvoice(self.paths[i])
            self.assertEqual(inv.get_invoice_num(), self.invoice_nums[i])

    def test_all_ids_are_correct(self):
        for i in range(len(self.paths)):
            inv = TextDartInvoice(self.paths[i])
            self.assertEqual(inv.get_id_num(), self.ids[i])


if __name__ == '__main__':
    test = TextDartTest()
    test.setUpClass()
    test.test_all_prices_are_correct()
