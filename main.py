from glob import glob
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import cv2
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers,models
import webbrowser
import time
from pynput.mouse import Listener, Button
from win32gui import GetWindowText, GetForegroundWindow
import PIL.ImageGrab
import cv2
import ctypes
import chess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
driver = webdriver.Chrome('./chromedriver')
driver.get('https://lichess.org/analysis')
colourModel = keras.models.load_model("colourClassify")
blackPieces = keras.models.load_model("blackPieces")
whitePieces = keras.models.load_model("whitePieces")
# webbrowser.open_new('book.pdf')

def findBoard(imageName):
    image = cv2.imread(imageName)
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
        if area > image.shape[0] * image.shape[1] * 0.10:
            x,y,w,h = cv2.boundingRect(c)
            ROI = image[y:y+h, x:x+w]
    # cv2.imshow('image', ROI)
    # time.sleep(1)

    return ROI

def chessReader(board):
    pieceArray = []
    # board = cv2.imread(fileName)
    board = cv2.resize(board, (400,400), interpolation = cv2.INTER_AREA)
    height = 400
    width = 400
    colourLabels = ['black','white','empty']
    whiteLabels = ['wRook', 'wQueen','wPawn','wKnight','wKing','wBishop']
    blackLabels = ['bRook','bQueen','bPawn','bKnight','bKing','bBishop']
    convertColour = (dict(enumerate(colourLabels))) 
    convertWhite = (dict(enumerate(whiteLabels))) 
    convertBlack = (dict(enumerate(blackLabels))) 

    for i in range (0,8):
        for z in range (0,8):
            ROI = board[int((height/8*i)):int(height/8*(i+1)), int((width/8*z)):int(width/8*(z+1))]
            eval = colourModel(ROI.reshape(1,50,50,3),training=False)[0]
            eval = eval.numpy().tolist()
            maxValue = max(eval)
            if convertColour[eval.index(maxValue)] == 'black':
                piece = blackPieces(ROI.reshape(1,50,50,3),training=False)[0]
                piece = piece.numpy().tolist()
                maxValue = max(piece)
                pieceArray.append(convertBlack[piece.index(maxValue)])
            elif convertColour[eval.index(maxValue)] == 'white':
                piece = whitePieces(ROI.reshape(1,50,50,3))[0] 
                piece = piece.numpy().tolist()
                maxValue = max(piece)
                pieceArray.append(convertWhite[piece.index(maxValue)])
            else:
                pieceArray.append('empty')

    minimalistNotation = {
        'wRook' : 'R',
        'wQueen' : 'Q',
        'wPawn' : 'P',
        'wKnight' : 'N',
        'wKing' : 'K',
        'wBishop' : 'B',
        'bRook' : 'r',
        'bQueen' : 'q',
        'bPawn' : 'p',
        'bKnight' : 'n',
        'bKing' : 'k',
        'bBishop' : 'b',
        'empty' : ' '
    }

    pieceArray= [x if x not in minimalistNotation else minimalistNotation[x] for x in pieceArray]

    return(pieceArray)

def get_fen_pieces(board):
    """
    Read board and return piece locations in fen format.
    """
    ret = None
    cnt = 0  # counter for successive empty cell along the row
    save = []  # temp container
    
    for i, v in enumerate(board):
        if v == ' ':
            cnt += 1
            
            # sum up the successive empty cell and update save
            if cnt > 1:
                save[len(save)-1] = str(cnt)
            else:
                save.append(str(cnt))  # add
        else:
            save.append(v)  # add
            cnt = 0  # reset, there is no successive number

        if (i+1)%8 == 0:  # end of row
            save.append('/')
            cnt = 0
            
    ret = ''.join(save)  # convert list to string

    return ret


previous_left = 0
pressLoc = (0,0)
releaseLoc = (0,0)

def on_click(x, y, button, pressed):
    global pressLoc
    global releaseLoc
    global previous_left
    # double click left button
    if pressed and button == Button.left:
        previous_left = time.time()
        pressLoc = (x,y)
        
    if not pressed:
        releaseLoc = (x,y)
        window = GetWindowText(GetForegroundWindow())
        if window[-6:] == 'Chrome' and window != 'Analysis board • lichess.org - Google Chrome' and time.time() - previous_left > 1.0:
            try:
                im = PIL.ImageGrab.grab((pressLoc[0],pressLoc[1],releaseLoc[0],releaseLoc[1]))
                im.save('screencapture.png')
            except:
                pass
            start = time.time()
            board_pieces = get_fen_pieces(chessReader(findBoard('screencapture.png')))
            print(time.time()-start)
            print(board_pieces)
            board = chess.Board(board_pieces[:-1])
            url = f'https://lichess.org/analysis/{board_pieces}'
            driver.get(url)


with Listener(on_click=on_click) as listener:
    listener.join()

