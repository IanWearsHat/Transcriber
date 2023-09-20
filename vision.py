import math
import pytesseract as pytess
import cv2
import numpy as np
import pdf2image

# segmentation mode 4 - it's segmented by rows (this option alone makes outputs so much better)
custom_config = '--psm 4'
custom_dpi = 120


def get_text_from_cropped_rect_of_image(ratio_rect: list[float], img, *, debug=False, has_pixel_values=False) -> str:
    height = img.shape[0]
    width = img.shape[1]
    
    if has_pixel_values:
        y_start = ratio_rect[0]
        y_end = ratio_rect[1]
        x_start = ratio_rect[2]
        x_end = ratio_rect[3]
    else:
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


def get_image(path):
    img = convert_pdf_to_image(path)[0] # TODO: invoice might not be on page 0
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


# https://blog.42mate.com/opencv-tesseract-is-a-powerful-combination/
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
def rotated_image(image, angle):
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
def get_horizontal_lines(image, vis_debug=False):
    # TODO: parameterize the thresholds, minLineLengths, and other arguments
    # probably in the parameters for this function so it's unique to the invoices that call it
    slope_thresh = 0.02

    if vis_debug:
        overlay = image.copy()
        overlay = cv2.cvtColor(overlay, cv2.COLOR_GRAY2BGR)
    # Convert image to grayscale
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use canny edge detection
    edges = cv2.Canny(image, 50, 150, apertureSize=3)

    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=170, lines=None, minLineLength=600, maxLineGap=20)

    line_points_list = []
    # Iterate over points
    for points in lines:
        # Extracted points nested in the list
        x1, y1, x2, y2 = points[0]
        if x2 - x1 != 0:
            slope = (y2 - y1) / (x2 - x1)
            if abs(slope) < slope_thresh:
                line_points_list.append((x1, y1))
                line_points_list.append((x2, y2))

                if vis_debug:
                    cv2.line(overlay, (x1, y1), (x2, y2), (0, 0, 255), 1)
    
    if vis_debug:
        alpha = 1
        color = image.copy()
        color = cv2.cvtColor(color, cv2.COLOR_GRAY2BGR)
        horiz = cv2.addWeighted(overlay, alpha, color, 1 - alpha, 0)
        cv2.imshow("", horiz)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    return line_points_list


def straighten_image(image):
    slope_thresh = 0.1
    vis_debug = False

    if vis_debug:
        overlay = image.copy()
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use canny edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=170, lines=None, minLineLength=50, maxLineGap=20)

    slopes_list = []
    # Iterate over points
    for points in lines:
        # Extracted points nested in the list
        x1, y1, x2, y2 = points[0]
        if x2 - x1 != 0:
            slope = (y2 - y1) / (x2 - x1)
            if abs(slope) < slope_thresh:
                slopes_list.append(slope)

                if vis_debug:
                    cv2.line(overlay, (x1, y1), (x2, y2), (0, 0, 255), 2)
    if vis_debug:
        alpha = 1
        result = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)

    avg_slope = sum(slopes_list) / len(slopes_list)
    angle = math.atan(avg_slope) * 180 / math.pi

    return rotated_image(image, angle)

def get_relevant_boxes(img, debug=False):
    # boxes code: https://stackoverflow.com/questions/57196047/how-to-detect-all-the-rectangular-boxes-in-the-given-image
    # gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    adapt_thresh= cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 5)
    thresh_inv = cv2.bitwise_not(adapt_thresh)

    # Blur the image
    blur = cv2.GaussianBlur(thresh_inv,(1,1),0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

    # find contours
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    images = []
   
    for c in contours:
        # get the bounding rect
        x, y, w, h = cv2.boundingRect(c)

        # TODO: width should be a ratio 
        if w > 700:
            blank = np.zeros((h + 40, w + 40), np.uint8)
            blank[:] = (255)
            blank[20:20+h, 20:20+w] = img[y:y+h, x:x+w]

            images.append(blank)
    
    if debug:
        for i in range(len(images)):
            cv2.imshow(str(i), images[i])
            cv2.imwrite(str(i) + '.png', images[i])
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return images


if __name__ == '__main__':
    # TODO: Get edges of tables and orient them to be correct. Then do regular ocr
    # TODO: Get bounds of tables dynamically. then do regular ocr.
    # path = r"C:\Users\ianbb\PycharmProjects\FreightStreamTranscriber\pdfExamples\HTCargo\HTC230283 CONN.pdf"
    path = r"C:\Users\ianbb\PycharmProjects\FreightStreamTranscriber\pdfExamples\RobertKong\Invoice-0033366.pdf"
    # path = r"C:\Users\ianbb\PycharmProjects\FreightStreamTranscriber\pdfExamples\JohneExpress\SCANNEDdocuments 08302023_0002.pdf"
    # path = r"C:\Users\ianbb\PycharmProjects\FreightStreamTranscriber\pdfExamples\JohneExpress\SCANNEDdocuments 08182023_0010.pdf"
    image = convert_pdf_to_image(path)[0]
    # image = straighten_image(image)
    # image = cv2.imread("test.png")
    boxes = get_relevant_boxes(path)

    i = 0
    for box in boxes:
        box = straighten_image(box)
        cv2.imshow(str(i), box)
        cv2.imwrite(str(i) + '.png', box)
        i += 1
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # boxes code: https://stackoverflow.com/questions/57196047/how-to-detect-all-the-rectangular-boxes-in-the-given-image
    # img = image
    # gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # adapt_thresh= cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 5)
    # thresh_inv = cv2.bitwise_not(adapt_thresh)

    # # Blur the image
    # blur = cv2.GaussianBlur(thresh_inv,(1,1),0)

    # thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

    # # find contours
    # contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    # mask = np.ones(img.shape[:2], dtype="uint8") * 255
    # pts = []
    # for c in contours:
    #     # get the bounding rect
    #     x, y, w, h = cv2.boundingRect(c)
    #     if w * h > 8000:
    #         pts.append((x, y, w, h))
    #         cv2.rectangle(mask, (x, y), (x + w, y + h), (0, 0, 255), -1)

    # res_final = cv2.bitwise_and(img, img, mask=cv2.bitwise_not(mask))

    # # for pt in pts:
    # #     cv2.circle(res_final, (pt), 3, (0, 0, 255), 3)
    # # res_final = get_horizontal_lines(res_final)
    # # cv2.imshow("boxes", mask)
    # # cv2.imshow("", thresh_inv)
    # cv2.imshow("final image", res_final)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # TODO: for each box, copy the box onto a slightly bigger blank image, then run the straighten function as its own image instead of the entire image
    # and then use ocr on that box for information

    # TODO: ratios for 
