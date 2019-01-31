import numpy as np
import cv2


def preprocess(img):
    img_blurred = cv2.GaussianBlur(img, (5,5), 0)
    # img_blurred = cv2.bilateralFilter(img, 9, 50, 50)

    gray = cv2.cvtColor(img_blurred, cv2.COLOR_BGR2GRAY)

    sobelx = cv2.Sobel(gray,cv2.CV_8U,1,0,ksize=3)
    cv2.imshow("Sobel",sobelx)
    cv2.waitKey(0)
    ret2,threshold_img = cv2.threshold(sobelx,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cv2.imshow("Threshold",threshold_img)
    cv2.waitKey(0)
    return threshold_img


def extract_contours(threshold_img):
    element = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(17, 3))
    morph_img_threshold = threshold_img.copy()
    cv2.morphologyEx(src=threshold_img, op=cv2.MORPH_CLOSE, kernel=element, dst=morph_img_threshold)
    cv2.imshow("close morphed", morph_img_threshold)
    cv2.waitKey(0)

    element = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(2, 4))
    cv2.morphologyEx(src=morph_img_threshold, op=cv2.MORPH_OPEN, kernel=element, dst=morph_img_threshold)
    cv2.imshow("open morphed", morph_img_threshold)
    cv2.waitKey(0)

    element = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(35, 5))
    cv2.morphologyEx(src=morph_img_threshold, op=cv2.MORPH_CLOSE, kernel=element, dst=morph_img_threshold)
    cv2.imshow("close1 morphed", morph_img_threshold)
    cv2.waitKey(0)

    element = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(5, 5))
    cv2.morphologyEx(src=morph_img_threshold, op=cv2.MORPH_OPEN, kernel=element, dst=morph_img_threshold)
    cv2.imshow("open1 morphed", morph_img_threshold)
    cv2.waitKey(0)

    element = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(50, 5))
    cv2.morphologyEx(src=morph_img_threshold, op=cv2.MORPH_CLOSE, kernel=element, dst=morph_img_threshold)
    cv2.imshow("close2 morphed", morph_img_threshold)
    cv2.waitKey(0)

    contours, hierarchy = cv2.findContours(morph_img_threshold,mode=cv2.RETR_EXTERNAL,method=cv2.CHAIN_APPROX_NONE)
    return contours


def ratioCheck(area, width, height):
    ratio = float(width) / float(height)
    if ratio < 1:
        ratio = 1 / ratio

    aspect = 4.7272
    min = 15*aspect*15  # minimum area
    # min = 1000  # minimum area
    max = 125*aspect*125  # maximum area
    # max = 7000  # maximum area

    rmin = 3
    rmax = 8

    # print(area, min, max)

    if (area < min or area > max) or (ratio < rmin or ratio > rmax):
        return False
    return True

def isMaxWhite(plate):
    avg = np.mean(plate)

    if(avg>=115):
        return True
    else:
        return False

def validateRotationAndRatio(rect):
    (x, y), (width, height), rect_angle = rect

    if(width>height):
        angle = -rect_angle
    else:
        angle = 90 + rect_angle

    if angle > 15:
        return False

    if height == 0 or width == 0:
        return False

    area = height*width

    # print(area)

    if not ratioCheck(area,width,height):
        return False
    else:
        return True



def cleanAndRead(img,contours, filename):
    rects = []
    for i,cnt in enumerate(contours):
        min_rect = cv2.minAreaRect(cnt)

        if validateRotationAndRatio(min_rect):
            # print(min_rect)
            x,y,w,h = cv2.boundingRect(cnt)
            plate_img = img[y:y+h,x:x+w]


            if(isMaxWhite(plate_img)):
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # rects.append((plate_img, (x, y, w, h)))
                cv2.imwrite("custom.jpg", img)
                cv2.imshow("out", img)
                cv2.waitKey(0)
                return img


def run(path):
    img = cv2.imread(path)
    if not img is None:
        (h, w) = img.shape[:2]
        r = 500 / float(w)
        dim = (500, int(h * r))
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

        threshold_img = preprocess(resized)
        contours = extract_contours(threshold_img)

        output = cleanAndRead(resized, contours, path)
        cv2.destroyAllWindows()

        return output
