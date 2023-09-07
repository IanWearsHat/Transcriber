import pytesseract as pytess
import cv2


class Vision:
    def get_accounting_invoice_num(self):
        pass


# TODO: might need to look at currency
if __name__ == '__main__':
    path = './freightStreamImages/4.3accountingWithThreeRows.png'
    # path = './freightStreamImages/4accounting.png'
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # looks at top invoice num in accounts payable table
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

    cropped = img[y_start:y_end, x_start:x_end]
    text = pytess.image_to_string(cropped)
    # text = pytess.image_to_string(img)
    print(text)

    print(cropped[mid_y][mid_x])

    # cropped[mid_y][mid_x] = 0 # to see where the middle pixel is

    # value of grayscale pixel in absence of row in AccountsPayable is 192
    # value of grayscale pixel outside AccountsPayable table is 244
    # value of grayscale pixel of row background color is 248
    cv2.imshow("", cropped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
