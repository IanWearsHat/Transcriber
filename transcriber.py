from PyPDF2 import PdfReader
from templates import *


path = "./pdfExamples/Dart/INVOICE - VNM00045559 - CONINT_US (30-Aug-23).pdf"
# path = "./pdfExamples/sample.pdf"
# path = "./pdfExamples/image.pdf"

# print(
#     TextDartInvoice(path).get_prices()
# )
#
# print(
#     TextDartInvoice(path).get_date()
# )
#
# print(
#     TextDartInvoice(path).get_invoice_num()
# )
print(
    TextDartInvoice(path).get_id_num()
)

# import pyautogui
#
# x, y = pyautogui.locateCenterOnScreen('test4.png', grayscale=True, confidence=0.6)
# pyautogui.moveTo(x, y)
# print(x, y)
# Problem: the image might not work at different resolutions, either with the monitor or the image
# One solution:
# Use cv to generate a bunch of resized images
# find a match using all of those images, which might not work according to the creator of PyAutoGUI
# https://stackoverflow.com/questions/45302681/running-pyautogui-on-a-different-computer-with-different-resolution

