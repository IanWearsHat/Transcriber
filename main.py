import keyboard
import time
from pathlib import Path

from watchdog import Watchdog
from transcriber import transcribe
from inputter import Inputter


def _has_new_attachments():
    return Path("./attachments").is_dir() and len([x for x in Path("./attachments").glob("**/*") if x.is_file()]) > 0


def _get_all_new_attachments():
    return (x.resolve() for x in Path("./attachments").glob("**/*"))


def _delete_all_new_attachments():
    for file_path in Path("./attachments").glob("**/*"):
        Path(file_path).unlink()


def main():
    # TODO: needs to focus on FreightStream if it's open
    # TODO: needs to open and then focus on FreightStream if it's not open
    # TODO: if there are multiple pdfs that have been downloaded, then close all tabs except for hawb list and then go from there instead of having to open up all tabs over again
    run = True
    # while run:
    if keyboard.is_pressed('p'):
        run = False

    watcher = Watchdog()
    watcher.run()

    # TODO: currently keeps redownloading the same pdfs because the method that reads from inbox does not mark the emails as read
    if _has_new_attachments():
        for pdf_path in _get_all_new_attachments():
            time.sleep(10)

            data = transcribe(pdf_path)

            Inputter(data).run_full_pipeline()

    _delete_all_new_attachments()

    # time.sleep(2)
    time.sleep(0.02)


if __name__ == '__main__':
    # main()
    import vision
    from templates import *
    path = r"C:\Users\ianbb\PycharmProjects\FreightStreamTranscriber\pdfExamples\MKC\Invoice-0604751.pdf"
    # path = r"C:\Users\ianbb\PycharmProjects\FreightStreamTranscriber\pdfExamples\RobertKong\Invoice-0033366.pdf"
    # path = r"C:\Users\ianbb\PycharmProjects\FreightStreamTranscriber\pdfExamples\RobertKong\Invoice-0033610_table_size_changed.pdf"
    img = vision.get_image(path)
    inv = TextMKCInvoice(img)
    # inv.get_prices_table()
    # print(inv.get_prices())
    # print(inv.get_id_num())
    # print(inv.get_date())
    # print(inv.get_invoice_num())

    import inputter

    data = inv.get_data()
    bot = inputter.Inputter(data)
    stop = bot.vendor_already_exists()
    print(stop)