import cv2
import numpy as np
from matplotlib import pyplot as plt
from detector import detector
import fitz
import os 

########## Make folders "book" and "potentialBoards" and "squares" before running.

########## Convert book to images

pdffile = "book.pdf"
zoom = 3
doc = fitz.open(pdffile)
for page in doc:
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix = mat)
    pix.save(f"book/{page.number}.png")

# Extract chessboards from images and writes to potentialBoards

for i in range (0,doc.page_count):
    detector(cv2.imread(f"book/{i}.png"),i)

############# Remove images that are the wrong dimensions for a chessboard.
############# For my particular book, this is around 433x433

for filename in os.listdir("potentialBoards"):
    f = os.path.join("potentialBoards", filename)
    board = cv2.imread(f)
    dimensions = board.shape
    height = dimensions[0]
    width = dimensions[1]
    if height < 330 or width < 330 or height > 380 or width > 380:
        os.remove(f)

########### Resize boards to 400x400.

for filename in os.listdir("potentialBoards"):
    f = os.path.join("potentialBoards", filename)
    board = cv2.imread(f)
    resized = cv2.resize(board, (400,400), interpolation = cv2.INTER_AREA)
    cv2.imwrite(f'{f}',resized)


######## Cut images into individual squares. Before running this code
######## Remove all remaining non-chessboard images from potentialBoards folder manually (Shouldnt be any)

for filename in os.listdir("potentialBoards"):
    f = os.path.join("potentialBoards", filename)
    board = cv2.imread(f)
    dimensions = board.shape
    height = dimensions[0]
    width = dimensions[1]
    for i in range (0,8):
        for z in range (0,8):
            ROI = board[int((height/8*i)):int(height/8*(i+1)), int((width/8*z)):int(width/8*(z+1))]
            cv2.imwrite(f'squares/{str(i) + str(z) + str(filename)}', ROI)


############### Resize all images to 50 x 50

for filename in os.listdir("squares"):
    f = os.path.join("squares", filename)
    board = cv2.imread(f)
    resized = cv2.resize(board, (50,50), interpolation = cv2.INTER_AREA)
    cv2.imwrite(f'{f}',resized)


############# Sort squares folder into pieces manually. If you change your folder view to large icons, and then sort by size
############# it wont take long because the folder sort will basically do it for you. (similar pieces have similar image size)
############# eta 30 mins? Make folder called pieces, containing 
############'wRook', 'wQueen','wPawn','wKnight','wKing','wBishop','empty','bRook','bQueen','bPawn','bKnight','bKing','bBishop'
############ 'black' (copy all black pieces), 'white' (copy all white pieces)
########### Then train all the individual AI's (colourAI, whiteAI, blackAI)



