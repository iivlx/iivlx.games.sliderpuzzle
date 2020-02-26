#!/usr/bin/env python3
""" Slider Puzzle
Slider Puzzle

Written in Python3 with tkinter library

""" 
from tkinter import *
from mainmenu import MainMenu

__author__ = "iivlx"
__date__ = (9,9,2017) #d,m,y
__version__ = "0.0.1"

# Mainloop
if __name__=="__main__":
    # Initialize root
    root = Tk()
    # Start program at MainMenu
    MainMenu(root)