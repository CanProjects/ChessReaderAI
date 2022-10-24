from glob import glob
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import cv2
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers,models
import uuid

colourLabels = ['black','white','empty']
whiteLabels = ['wRook', 'wQueen','wPawn','wKnight','wKing','wBishop']
blackLabels = ['bRook','bQueen','bPawn','bKnight','bKing','bBishop']
convertColour = (dict(enumerate(colourLabels))) 
convertWhite = (dict(enumerate(whiteLabels))) 
convertBlack = (dict(enumerate(blackLabels))) 
colourModel = keras.models.load_model("colourClassify")
blackPieces = keras.models.load_model("blackPieces")
whitePieces = keras.models.load_model("whitePieces")

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images

for i in load_images_from_folder('squares'):

    eval = colourModel(i.reshape(1,50,50,3),training=False)[0]
    eval = eval.numpy().tolist()
    maxValue = max(eval)
    filename = str(uuid.uuid4())
    if convertColour[eval.index(maxValue)] == 'black':
        cv2.imwrite(f'pieces\\black\\{filename}.png', i)
    elif convertColour[eval.index(maxValue)] == 'white':
        cv2.imwrite(f'pieces\\white\\{filename}.png', i)    
    else:
        cv2.imwrite(f'pieces\\empty\\{filename}.png', i)    

for i in load_images_from_folder('pieces\\black'):
    eval = blackPieces(i.reshape(1,50,50,3),training=False)[0]
    eval = eval.numpy().tolist()
    # print(eval)
    maxValue = max(eval)
    filename = str(uuid.uuid4())
    folderName = convertBlack[eval.index(maxValue)]
    cv2.imwrite(f'pieces\\{folderName}\\{filename}.png', i)

        
for i in load_images_from_folder('pieces\\white'):
    eval = whitePieces(i.reshape(1,50,50,3),training=False)[0]
    eval = eval.numpy().tolist()
    # print(eval)
    maxValue = max(eval)
    filename = str(uuid.uuid4())
    folderName = convertWhite[eval.index(maxValue)]
    cv2.imwrite(f'pieces\\{folderName}\\{filename}.png', i)



# def chessReader(board):
#     colourLabels = ['black','white','empty']
#     whiteLabels = ['wRook', 'wQueen','wPawn','wKnight','wKing','wBishop']
#     blackLabels = ['bRook','bQueen','bPawn','bKnight','bKing','bBishop']
#     convertColour = (dict(enumerate(colourLabels))) 
#     convertWhite = (dict(enumerate(whiteLabels))) 
#     convertBlack = (dict(enumerate(blackLabels))) 
#     colourModel = keras.models.load_model("colourClassify")
#     blackPieces = keras.models.load_model("blackPieces")
#     whitePieces = keras.models.load_model("whitePieces")
#     for i in range (0,8):
#         for z in range (0,8):
#             ROI = board[int((height/8*i)):int(height/8*(i+1)), int((width/8*z)):int(width/8*(z+1))]
#             eval = colourModel.predict(ROI.reshape(1,50,50,3))
#             eval = eval[0].tolist()
#             maxValue = max(eval)
#             if convertColour[eval.index(maxValue)] == 'black':
#                 piece = blackPieces.predict(ROI.reshape(1,50,50,3)) 
#                 piece = piece[0].tolist()
#                 maxValue = max(piece)
#                 pieceArray.append(convertBlack[piece.index(maxValue)])
#             elif convertColour[eval.index(maxValue)] == 'white':
#                 piece = whitePieces.predict(ROI.reshape(1,50,50,3)) 
#                 piece = piece[0].tolist()
#                 maxValue = max(piece)
#                 pieceArray.append(convertWhite[piece.index(maxValue)])
#             else:
#                 pieceArray.append('empty')

#     minimalistNotation = {
#         'wRook' : 'R',
#         'wQueen' : 'Q',
#         'wPawn' : 'P',
#         'wKnight' : 'N',
#         'wKing' : 'K',
#         'wBishop' : 'B',
#         'bRook' : 'r',
#         'bQueen' : 'q',
#         'bPawn' : 'p',
#         'bKnight' : 'n',
#         'bKing' : 'k',
#         'bBishop' : 'b',
#         'empty' : ' '
#     }

#     pieceArray= [x if x not in minimalistNotation else minimalistNotation[x] for x in pieceArray]

#     return(pieceArray)


