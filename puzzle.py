from tkinter import *
from PIL import ImageTk, Image
from random import randint

class PuzzleFrame(Frame):
    """"""
    WINDOW_BG = "lightgrey"
    def __init__(self, master, **kw):
        Frame.__init__(self, master, **kw)
        # set window options
        #self.config(bg="grey")        
        #self.master.geometry("%ix%i" % (self.fullImage.width(), self.fullImage.height()))
        self.resizeable = (False, False)
        # image options
        self.imagePath = master.imagePath
        self.puzzleImage = Image.open(self.imagePath)
        self.fullImage = ImageTk.PhotoImage(self.puzzleImage)
        # puzzle options
        self.gridSize = self.master.gridSize
        self.pieceColumns = self.gridSize
        self.pieceRows = self.gridSize
        self.emptyPiece = (self.gridSize-1,self.gridSize-1) # position of empty piece
        self.moveCount = 0
        # piece information
        self.pieceWidth = self.fullImage.width()/self.pieceColumns
        self.pieceHeight = self.fullImage.height()/self.pieceRows
        #print(self.pieceColumns, self.pieceRows)
         
        self.images = [] # Tk PhotoImage objects -- couldnt delete
        self.labels = [] # Reference to labels holding images
                
        self.createGrid()
        self.randomizePieces()
        #self.createStatusBar()
        
        
    def createStatusBar(self):
        self.statusBar = Frame(self, background="yellow", width=800, height=200)
        #print(self.master.winfo_width())
        self.moveVar = IntVar()
        self.statusBar.movelabel = Label(self.statusBar, bd=1, relief=SUNKEN, text="Moves: ", font=('arial',10,'normal')).grid(row=0,column=0)
        self.statusBar.movevarlabel = Label(self.statusBar, bd=1, relief=SUNKEN,
                           textvariable=self.moveVar, font=('arial',10,'normal'))
        self.moveVar.set(self.moveCount)
        self.statusBar.movevarlabel.grid(row=0,column=1)
        self.statusBar.grid(row=4,column=0,columnspan=4)
        
        
    def createGrid(self):
        for i in range(0,self.pieceRows):
            for j in range(0,self.pieceColumns):
                if i==self.pieceRows-1 and j == self.pieceColumns-1:
                    break
                self.tempImage = self.puzzleImage.crop((self.pieceWidth*j, self.pieceHeight*i, self.pieceWidth*(j+1), self.pieceHeight*(i+1)))
                self.tempImage = ImageTk.PhotoImage(self.tempImage)
                self.tempLabel = Label(self, image=self.tempImage)
                self.tempLabel.grid(row=i, column=j)
                
                self.tempLabel.bind('<Button-1>', self.clickPiece)
                
                self.images.append(self.tempImage)
                self.labels.append(self.tempLabel)
        
        self.configure(bg=self.WINDOW_BG)
        self.pack(expand=True)
        
    
    def findPieceByRC(self, r,c):
        for piece in self.labels:
            gridInfo = piece.grid_info()
            if gridInfo['row'] == r and gridInfo['column'] == c:
                return piece
        
    def clickPiece(self, event):
        """ Check if piece is in row or column with empty piece, if so slide all pieces down towards empty slot
        """
        r = event.widget.grid_info()['row']
        c = event.widget.grid_info()['column']
        er, ec = self.emptyPiece
        
        #print('clicked: %i, %i' %(r, c))
        
        if r==er: # pieces are on same row as empty
            if c < ec: # columns slide right
                numToSlide = ec-c
                for i in range(0,numToSlide):
                    piece = self.findPieceByRC(r, ec-1-i)
                    piece.grid(row=r,column=ec-i)
                
            elif c > ec: # slide left
                numToSlide = c-ec
                for i in range(0,numToSlide):
                    piece = self.findPieceByRC(r, ec+1+i)
                    piece.grid(row=r,column=ec+i)
            self.emptyPiece = (r, c)
            self.moveCount += 1
            #self.moveVar.set(self.moveCount)
        elif c==ec: # pieces on same column
            if r < er: # slide down
                numToSlide = er-r
                for i in range(0,numToSlide):
                    piece = self.findPieceByRC(er-1-i, c)
                    piece.grid(row=er-i,column=c)
            if r > er:
                numToSlide = r-er
                for i in range(0,numToSlide):
                    piece = self.findPieceByRC(er+1+i, c)
                    piece.grid(row=er+i,column=c)
            self.emptyPiece = (r, c)
            self.moveCount += 1
            #self.moveVar.set(self.moveCount)

    def randomizePieces(self):
        for i in range(0,1000):
            er, ec = self.emptyPiece
            rr = randint(0,self.pieceRows-1)
            rc = randint(0,self.pieceColumns-1)
            if not (rr==er and rc==ec):
                self.swapPiece(rr, rc)
        
        rr = self.gridSize-1
        rc = self.gridSize-1
        if not (rr==er and rc==ec):
                self.swapPiece(rr, rc)
        
        
    
    def swapPiece(self,r,c):
        er, ec = self.emptyPiece
        piece = self.findPieceByRC(r, c)
        piece.grid(row=er, column=ec)
        self.emptyPiece = (r, c)
        
class Puzzle:
    def __init__(self):
        self.puzzleImage = None
        