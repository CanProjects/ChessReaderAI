import numpy as np
from matplotlib import pyplot as plt
import cv2

def detector(imageName,seedNumber):

    # Load image, grayscale, Gaussian blur, Otsu's threshold
    image = imageName
    copy = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (13,13), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Two pass dilate with horizontal and vertical kernel
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,2))
    dilate = cv2.dilate(thresh, horizontal_kernel, iterations=2)
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,1))
    dilate = cv2.dilate(dilate, vertical_kernel, iterations=2)

    # Find contours, filter using contour threshold area, and draw rectangle
    cnts = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv2.contourArea(c)
        if area > image.shape[0] * image.shape[1] * 0.01 and area < image.shape[0] * image.shape[1] - 10000:
            x,y,w,h = cv2.boundingRect(c)
            ROI = image[y:y+h, x:x+w]
            cv2.imwrite('potentialBoards/{}.png'.format(seedNumber), ROI)
            cv2.rectangle(copy,(x,y),(x+w,y+h),(36,255,12),2)
    # cv2.imshow('thresh', thresh)
    # cv2.imshow('dilate', dilate)
    # cv2.imshow('image', cv2.resize(image, None, fx=2, fy=2))
    # cv2.waitKey()

# detector('capture.png')