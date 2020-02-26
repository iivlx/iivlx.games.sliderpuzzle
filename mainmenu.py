from tkinter import * 
from tkinter.messagebox import showerror, showinfo, showwarning, askquestion

from puzzle import *

def startTK(cls):
    def inner(master, **kwargs):
        main = cls(master, **kwargs)
        master.mainloop()
        try:
            master.destroy()
        except TclError as err:
            if err.args[0]=='can\'t invoke "destroy" command: application has been destroyed':
                pass
            else:
                raise( err )
        return
    return inner

@startTK
class MainMenu(Frame):
    """The mainmenu for the application. Should be a child of the tk root,
    that is self.master should be the tk root"""
    WINDOW_POSITION_X = 800
    WINDOW_POSITION_Y = 200
    WINDOW_WIDTH = 300
    WINDOW_HEIGHT = 550
    WINDOW_BG = "yellow"
    def __init__(self, master, **kw):
        Frame.__init__(self, master, **kw)
        # Set up windows properties
        self.master.title("Slider Puzzle")
        self.resizable = (False, False)
        #
        self.puzzle = None;
        self.currentWindow = None;
        #self.resetGeometry()
        self.createMainMenu()
        # default options
        self.gridSize = 4
        self.imagePath = "puzzle.jpg"
    
    
    def createMainMenu(self):
    
        self.configure(width=self.WINDOW_WIDTH,
                       height=self.WINDOW_HEIGHT,
                       bg=self.WINDOW_BG)
        #self.geometry('%ix%i' % (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
    
        self.createLogo()
        self.createMenuBar()
        self.createMenuButtons()
        self.setKeys()
        
        self.pack_propagate(False)
        self.pack(expand=True)
        
    def createOptionsMenu(self):
        for widget in self.winfo_children():
                widget.destroy()
        self.createLogo()
        
        self.gridOptionsLabel = Label(self, bg='yellow', text="Grid Size: ")
        self.gridOptionsLabel.pack()
        self.gridOptionsEntry = Entry(self)
        self.gridOptionsEntry.insert(0, self.gridSize)
        self.gridOptionsEntry.pack()
        
        self.imageOptionsLabel = Label(self, bg='yellow', text="Image File: ")
        self.imageOptionsLabel.pack()
        self.imageOptionsEntry = Entry(self)
        self.imageOptionsEntry.insert(0, self.imagePath)
        self.imageOptionsEntry.pack()
        
        self.confirmButton = Button(self, text="Confirm", width=10, command=self.confirmOptions)
        self.confirmButton.pack(side="left",padx=30)
        
        self.cancelButton = Button(self, text="Cancel", width=10, command=self.cancelOptions)
        self.cancelButton.pack(side="right",padx=30)
        
    def confirmOptions(self):
        self.gridSize = int(self.gridOptionsEntry.get())
        self.imagePath = self.imageOptionsEntry.get()
        for widget in self.winfo_children():
                widget.destroy()
        self.createMainMenu()
    
    def cancelOptions(self):
        for widget in self.winfo_children():
                widget.destroy()
        self.createMainMenu()
        
    def createMenuBar(self, **kw):
        """ Create the main menubar and submenus"""
        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)
        # Puzzle Menu
        self.puzzlemenu = Menu(self.menubar, tearoff=0)
        self.puzzlemenu.add_command(label="New", command=self.createPuzzle)
        self.puzzlemenu.add_command(label="Close", state="disabled", command=self.closePuzzle)
        self.puzzlemenu.add_command(label="Randomize", command=self.randomize)
        self.puzzlemenu.add_command(label="Exit", command=self.confirmQuit)
        self.menubar.add_cascade(label="Puzzle", menu=self.puzzlemenu)

    def createMenuButtons(self, **kw):
        newButton = Button(self, width=self.WINDOW_WIDTH, bg="black", fg="white", text="New", command=self.createPuzzle)
        newButton.pack()#pady=(100,0))
        optionsButton = Button(self, width=self.WINDOW_WIDTH, bg="black", fg="white", text="Options", command=self.createOptionsMenu)
        optionsButton.pack()#pady=(100,0))
        exitButton = Button(self, width=self.WINDOW_WIDTH, bg="black", fg="white",  text="Exit", command=self.quit)
        exitButton.pack()#pady=(40,0))

    def createLogo(self):
        logoFont = ("ms serif", 24, "bold italic")
        logoTextUp = Label(self, text="Slider", bg="yellow", font=logoFont)
        logoTextUp.pack(pady=40)
        logoTextDown = Label(self, text="Puzzle", bg="yellow", font=logoFont)
        logoTextDown.pack(pady=40)

    def resetGeometry(self):
        
        """ Reset the default geometry for the window"""
        self.master.resizable(width=False, height=False)
        self.update_idletasks()
        w = self.cget("width")
        h = self.cget("height")
        self.master.geometry("%dx%d+%d+%d" % (w,h,self.WINDOW_POSITION_X,self.WINDOW_POSITION_Y))
    
    def setKeys(self):
        self.master.bind("<Escape>", lambda e: self.confirmQuit()) #no prompt exit
    
    def geometry(self, newGeometry):
        self.master.geometry(newGeometry)
        
    
    def randomize(self):
        if self.puzzle:
            self.currentWindow.randomizePieces()    
    
    def createPuzzle(self):
        """"""
        if not self.puzzle:
            self.pack_propagate(True)
            self.puzzlemenu.entryconfig("Close", state="normal")
            for widget in self.winfo_children():
                widget.destroy()
            self.currentWindow = PuzzleFrame(self)
            self.puzzle = Puzzle()
        else:
            if askquestion("New Puzzle", "Are you sure you want to start a new puzzle?") == "yes":
                self.closePuzzle(menu=False)
                self.createPuzzle()
                
    def closePuzzle(self, menu=True):
        self.currentWindow.destroy()
        self.currentWindow = None
        self.puzzle = None
        if menu:
            self.createMainMenu()

    def confirmQuit(self):
        if askquestion("Quit","Do you really want to quit?") == "yes":
            self.quit()