import pytesseract as pytess
import cv2
import numpy as np
import pdf2image


class Vision:
    def get_accounting_invoice_num(self):
        pass

# TODO: maybe look at an entire column or table
# TODO: maybe use a confidence parameter

# TODO: might need to look at currency
if __name__ == '__main__':
    path = './freightStreamImages/4.3accountingWithThreeRows.png'
    # path = './freightStreamImages/4accounting.png'
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # coordinates for top invoice num in accounts payable table
    y_start = 618
    y_end = 650
    x_start = 667
    x_end = 790

    row_y_diff = 22

    mid_x = (x_end - x_start) // 2
    mid_y = (y_end - y_start) // 2

    # for _ in range(4):
    #     y_start += row_y_diff
    #     y_end += row_y_diff

    # coordinates for whole invoice num column
    # y_start = 618
    # y_end = 716
    # x_start = 667
    # x_end = 790

    # coordinates for whole table without row numbers
    y_start = 618
    y_end = 717
    x_start = 213
    x_end = 1044

    # coordinates for row numbers
    # y_start = 618
    # y_end = 717
    # x_start = 194
    # x_end = 212

    cropped = img[y_start:y_end, x_start:x_end]
    # text = pytess.image_to_string(cropped)
    r_config = '--psm 4' # ocr knows it's segmented by rows (this option alone makes outputs so much better)
    text = pytess.run_and_get_output(cropped, extension='txt', config=r_config)

    print(text)


    def convert_pdf_to_image(document, dpi):
        images = []
        images.extend(
            list(
                map(
                    lambda image: cv2.cvtColor(
                        np.asarray(image), code=cv2.COLOR_RGB2BGR
                    ),
                    pdf2image.convert_from_path(document, dpi=dpi),
                )
            )
        )
        return images


    def rotate_image(image, angle):
        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
        return result


    img = convert_pdf_to_image(
        r"C:\Users\ianbb\PycharmProjects\FreightStreamTranscriber\pdfExamples\JohneExpress\SCANNEDdocuments 08302023_0002.pdf",
        300)[0]

    img = rotate_image(img, 1.5)
    # img = rotate_image(img, 15)
    # print(cropped[mid_y][mid_x])

    # cropped[mid_y][mid_x] = 0 # to see where the middle pixel is

    # value of grayscale pixel in absence of row in AccountsPayable is 192
    # value of grayscale pixel outside AccountsPayable table is 244
    # value of grayscale pixel of row background color is 248
    cv2.imshow("", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    """
    For Johne Express
    Because all the documents are scanned, use Tesseract
    Because the documents are slightly tilted, some pre-processing has to occur
    Find the angle it's tilted at. 
    Then rotate it by that angle
    """
