import unittest

from invoices.dart import TextDartInvoice


class TextDartTest(unittest.TestCase):
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
            'VNM00045559',
            'VNM00045559',
            'VNM00045632',
            'VNM00045640',
            'VNM00045687'
        ]

    def test_all_prices_are_correct(self):
        for i in range(len(self.paths)):
            inv = TextDartInvoice(self.paths[i])
            test_prices = inv.get_prices()
            exp_prices = self.prices[i]

            for pair_i in range(len(self.price_names)):
                name = self.price_names[pair_i]
                price = exp_prices[pair_i]
                assert test_prices[name] == price


if __name__ == '__main__':
    test = TextDartTest()
    test.setUpClass()
    test.test_all_prices_are_correct()
