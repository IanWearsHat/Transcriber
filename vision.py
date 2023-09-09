import pytesseract as pytess
import cv2
import numpy as np
import pdf2image

# segmentation mode 4 - it's segmented by rows (this option alone makes outputs so much better)
custom_config = '--psm 4'
custom_dpi = 120


class Vision:
    @staticmethod
    def get_text_from_cropped_rect_of_image(rect: list[int], img, *, debug=False) -> str:
        # gotta make this into a ratio so that the dpi can change
        y_start = rect[0]
        y_end = rect[1]
        x_start = rect[2]
        x_end = rect[3]

        cropped = img[y_start:y_end, x_start:x_end]
        if debug:
            cv2.imshow("", cropped)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return pytess.run_and_get_output(cropped, extension='txt', config=custom_config)

    @staticmethod
    def get_image(path):
        img = Vision.convert_pdf_to_image(path)[0] # TODO: invoice might not be on page 0
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img

    @staticmethod
    def convert_pdf_to_image(document):
        images = []
        images.extend(
            list(
                map(
                    lambda image: cv2.cvtColor(
                        np.asarray(image), code=cv2.COLOR_RGB2BGR
                    ),
                    pdf2image.convert_from_path(document, dpi=custom_dpi),
                )
            )
        )
        return images

    # https://stackoverflow.com/questions/9041681/opencv-python-rotate-image-by-x-degrees-around-specific-point
    @staticmethod
    def rotate_image(image, angle):
        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
        return result

    def get_table(self):
        path = r"C:\Users\ianbb\PycharmProjects\FreightStreamTranscriber\image_invoice.png"
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # gotta make this into a ratio so that the dpi can change
        length = 1020
        height = 1320

        y_start = 679
        y_end = 1060
        x_start = 77
        x_end = 956

        cropped = img[y_start:y_end, x_start:x_end]
        r_config = '--psm 4'   # ocr knows it's segmented by rows (this option alone makes outputs so much better)
        text = pytess.run_and_get_output(cropped, extension='txt', config=r_config)

        print(text)

    def get_mawb(self):
        path = r"C:\Users\ianbb\PycharmProjects\FreightStreamTranscriber\image_invoice.png"
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # gotta make this into a ratio so that the dpi can change
        length = 1020
        height = 1320

        y_start = 516
        y_end = 544
        x_start = 90
        x_end = 932

        cropped = img[y_start:y_end, x_start:x_end]
        r_config = '--psm 4'  # ocr knows it's segmented by rows (this option alone makes outputs so much better)
        text = pytess.run_and_get_output(cropped, extension='txt', config=r_config)

        print(text)


# TODO: maybe look at an entire column or table
# TODO: maybe use a confidence parameter

# TODO: might need to look at currency
if __name__ == '__main__':
    vis = Vision()
    vis.get_table()
    vis.get_mawb()
    # path = './freightStreamImages/4.3accountingWithThreeRows.png'
    # # path = './freightStreamImages/4accounting.png'
    # img = cv2.imread(path)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #
    # # coordinates for top invoice num in accounts payable table
    # y_start = 618
    # y_end = 650
    # x_start = 667
    # x_end = 790
    #
    # row_y_diff = 22
    #
    # mid_x = (x_end - x_start) // 2
    # mid_y = (y_end - y_start) // 2
    #
    # # for _ in range(4):
    # #     y_start += row_y_diff
    # #     y_end += row_y_diff
    #
    # # coordinates for whole invoice num column
    # # y_start = 618
    # # y_end = 716
    # # x_start = 667
    # # x_end = 790
    #
    # # coordinates for whole table without row numbers
    # y_start = 618
    # y_end = 717
    # x_start = 213
    # x_end = 1044
    #
    # # coordinates for row numbers
    # # y_start = 618
    # # y_end = 717
    # # x_start = 194
    # # x_end = 212
    #
    #
    # length = 1020
    # height = 1320
    #
    # y_start = 679
    # y_end = 1060
    # x_start = 77
    # x_end = 956
    #
    # cropped = img[y_start:y_end, x_start:x_end]
    # # text = pytess.image_to_string(cropped)
    # r_config = '--psm 4' # ocr knows it's segmented by rows (this option alone makes outputs so much better)
    # text = pytess.run_and_get_output(cropped, extension='txt', config=r_config)
    #
    # print(text)
    #
    #
    # def convert_pdf_to_image(document, dpi):
    #     images = []
    #     images.extend(
    #         list(
    #             map(
    #                 lambda image: cv2.cvtColor(
    #                     np.asarray(image), code=cv2.COLOR_RGB2BGR
    #                 ),
    #                 pdf2image.convert_from_path(document, dpi=dpi),
    #             )
    #         )
    #     )
    #     return images
    #
    #
    # def rotate_image(image, angle):
    #     image_center = tuple(np.array(image.shape[1::-1]) / 2)
    #     rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    #     result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    #     return result
    #
    #
    # # img = convert_pdf_to_image(r"C:\Users\ianbb\PycharmProjects\FreightStreamTranscriber\pdfExamples\MKC\Invoice-0604751.pdf", 120)[0]
    #
    # # cv2.imwrite('image_invoice.png', img)
    #
    #
    #
    #
    # # img = rotate_image(img, 1.5)
    #
    # # print(cropped[mid_y][mid_x])
    #
    # # cropped[mid_y][mid_x] = 0 # to see where the middle pixel is
    #
    # # value of grayscale pixel in absence of row in AccountsPayable is 192
    # # value of grayscale pixel outside AccountsPayable table is 244
    # # value of grayscale pixel of row background color is 248
    # # cv2.imshow("", img)
    # # cv2.waitKey(0)
    # # cv2.destroyAllWindows()
    #
    # """
    # For Johne Express
    # Because all the documents are scanned, use Tesseract
    # Because the documents are slightly tilted, some pre-processing has to occur
    # Find the angle it's tilted at.
    # Then rotate it by that angle
    # """
