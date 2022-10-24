# ChessReaderAI
An AI which uses computer vision to detect chess positions in PDF's then opens up a digital board for gameplay

Demonstration:


How it works:

Three main parts work together to make this possible.

1: Computer vision is used to detect where the chessboard would be in an image.
2. An AI then classifies a particular square as being either empty, containing a white piece, or a black piece
3. An AI classifies the piece into the type of piece it is.

How its used:

Right now it uses Selenium because this implementation is more of a proof of concept than a finished idea. This would work far better as a website.

You open your chessbook and click and drag roughly an outline of the chessboard on the screen (overshooting the area is better). It will then open up your browser.

How its trained:

Training is a tedious process of manually sorting images into folders. Ive only trained it on 2 books myself currently so the ability for the AI to generalise is not great. You would need to do ideally 50 different piece sets from different sources for this to work amazingly. Once you have sorted into the folders the AI is trained on the dataset to recognise the pieces. To speed up the training process I have included a folder called autofilter which has the AI sort the data first based on what it thinks, meaning that rather than classifying every piece, you can just fix the mistakes made by the AI. I have included a book in autofilter for testing it out on.

Otherwise, the code mostly speaks for itself and is fairly well commented. 

File by File:
The folders: Black pieces, whitePieces and colourClassify are the individual AI's. The folders book, potential boards, squares, and pieces contain the data extracted from the book. Book folder is the pages of the book, potential boards is the boards that were detected, squares are the squares, and pieces are the specific pieces.

ColourAI, WhiteAI and BlackAI are the training code for training the AI's. PdfReader reads the PDF. Main actually uses the AIs. 
