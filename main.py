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
    main()
