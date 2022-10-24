# ChessReaderAI
An AI which uses computer vision to detect chess positions in PDF's then opens up a digital board for gameplay


How it works:

Three main parts work together to make this possible.

1: Computer vision is used to detect where the chessboard would be in an image.
2. An AI then classifies a particular square as being either empty, containing a white piece, or a black piece
3. An AI classifies the piece into the type of piece it is.

How its used:
Right now it uses Selenium because this implementation is more of a proof of concept than a finished idea. This would work far better as a website.
