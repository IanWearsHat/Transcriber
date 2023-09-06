from PyPDF2 import PdfReader
from invoices import *


path = "./pdfExamples/Dart/INVOICE - VNM00045559 - CONINT_US (30-Aug-23).pdf"
# path = "./pdfExamples/sample.pdf"
# path = "./pdfExamples/image.pdf"

print(
    TextDartInvoice(path).get_prices()
)

print(
    TextDartInvoice(path).get_date()
)

print(
    TextDartInvoice(path).get_invoice_num()
)

