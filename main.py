import keyboard
import time
from pathlib import Path
import subprocess
import pyautogui as gui

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
    time.sleep(3)
    window = gui.getWindowsWithTitle("FMS 2")
    if window:
        window[0].activate()
        time.sleep(0.5)

        # exits freightstream because there might be an afk program termination
        Inputter.exit_freightstream()

    fs_path = r"C:\Program Files (x86)\Freightstream\FreightStream2.1\fms2000.exe"
    subprocess.run(fs_path)

    Inputter.login_to_freightstream()
    
    # TODO: needs to focus on FreightStream if it's open
    # TODO: needs to open and then focus on FreightStream if it's not open
    # TODO: if there are multiple pdfs that have been downloaded, then close all tabs except for hawb list and then go from there instead of having to open up all tabs over again
    run = True
    # while run:
    if keyboard.is_pressed('p'):
        run = False

    Watchdog().run()

    # TODO: currently keeps redownloading the same pdfs because the method that reads from inbox does not mark the emails as read
    if _has_new_attachments():
        for pdf_path in _get_all_new_attachments():
            print(pdf_path)
            time.sleep(10)

            data = transcribe(pdf_path)

            if data:
                Inputter(data).run_full_pipeline()

    _delete_all_new_attachments()

    # time.sleep(2)
    time.sleep(0.02)


if __name__ == '__main__':
    main()

    # # TODO: what if the file has not even been opened on freightstream
    # # TODO: after searching for the id num, screenshot and check if the file is even there
    # # main()
    # import vision
    # from templates import *
    # path = r"C:\Users\ianbb\PycharmProjects\FreightStreamTranscriber\pdfExamples\MKC\Invoice-0604751.pdf"
    # path = r"C:\Users\ianbb\PycharmProjects\FreightStreamTranscriber\pdfExamples\APS-HoChiMinh\CONNECTED- DAE-ASA23090014.pdf"
    # # path = r"C:\Users\ianbb\PycharmProjects\FreightStreamTranscriber\pdfExamples\APS-HoChiMinh\CONNECTED- DAE-ASA23090018.pdf"
    # # path = r"C:\Users\ianbb\PycharmProjects\FreightStreamTranscriber\pdfExamples\RobertKong\Invoice-0033366.pdf"
    # # path = r"C:\Users\ianbb\PycharmProjects\FreightStreamTranscriber\pdfExamples\RobertKong\Invoice-0033610_table_size_changed.pdf"
    # img = vision.get_image(path)
    # inv = TextAPSInvoice(img)
    # # inv.get_prices_table()
    # # print(inv.get_prices())
    # # print(inv.get_id_num())
    # # print(inv.get_date())
    # # print(inv.get_invoice_num())
    # print(inv.get_data())