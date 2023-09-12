import pytesseract as pytess
import cv2
import numpy as np
import pdf2image

# segmentation mode 4 - it's segmented by rows (this option alone makes outputs so much better)
custom_config = '--psm 4'
custom_dpi = 120


class Vision:
    @staticmethod
    def get_text_from_cropped_rect_of_image(ratio_rect: list[float], img, *, debug=False) -> str:
        height = img.shape[0]
        width = img.shape[1]

        y_start = round(ratio_rect[0] * height)
        y_end = round(ratio_rect[1] * height)
        x_start = round(ratio_rect[2] * width)
        x_end = round(ratio_rect[3] * width)

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

    # https://blog.42mate.com/opencv-tesseract-is-a-powerful-combination/
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


# TODO: maybe look at an entire column or table
# TODO: maybe use a confidence parameter

# TODO: might need to look at currency

"""
For Johne Express
Because all the documents are scanned, use Tesseract
Because the documents are slightly tilted, some pre-processing has to occur
Find the angle it's tilted at.
Then rotate it by that angle
"""

if __name__ == '__main__':
    image = Vision.convert_pdf_to_image(r"C:\Users\ianbb\PycharmProjects\FreightStreamTranscriber\pdfExamples\HTCargo\HTC230283 CONN.pdf")[0]

    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use canny edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Apply HoughLinesP method to
    # to directly obtain line end points
    # lines_list = []
    lines = cv2.HoughLinesP(
        edges,  # Input edge image
        1,  # Distance resolution in pixels
        np.pi / 180,  # Angle resolution in radians
        threshold=10,  # Min number of votes for valid line
        minLineLength=5,  # Min allowed length of line
        maxLineGap=10  # Max allowed gap between line for joining them
    )

    # Iterate over points
    for points in lines:
        # Extracted points nested in the list
        x1, y1, x2, y2 = points[0]
        # Draw the lines joing the points
        # On the original image
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # Maintain a simples lookup list for points
        # lines_list.append([(x1, y1), (x2, y2)])

    cv2.imshow("", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
