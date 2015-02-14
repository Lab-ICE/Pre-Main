'''
Created on Feb 11, 2015

@author: Max Ruiz
'''
from Tkinter import *
import Tkinter
from FileManip import FileManip
from NetChecker import NetChecker

class MainMenu(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master, background='white')
        self.master = master
        self.pack()

        self.initGui()

    def initGui(self):
        self.master.title("Information on Component Extractor - ICE")
        self.mainButtons()
        self.menuBar()
        self.master.config(menu=self.menubar)


    def mainButtons(self):
        bcolor = 'light blue'; tcolor = 'blue' #background and text color for buttons
        acolor = 'tan' #active background color
        baserow = 0; basecolumn = 0;
        tfont = 'Times 10'

        self.URLtoPartSpecButton = Button(self, text = 'URL to Part Spec',
             padx=5, pady=5, width=20, height=3, bg=bcolor, fg=tcolor, font=tfont,
             activebackground=acolor, state='disabled', command=lambda: self.callURLToPartSpecsApp())
        self.URLtoPartSpecButton.grid(row=baserow, column=basecolumn, padx=10, pady=10)

        self.netlistButton = Button(self, text = 'EAGLE to Net list \n Compiler and Organizer',
             padx=5, pady=5, width=20, height=3, bg=bcolor, state='disabled', fg=tcolor,
             font=tfont, activebackground=acolor, command=lambda: self.callEAGLENetlistCompilerAndOrgranizerApp())
        self.netlistButton.grid(row=baserow, column=basecolumn+1, padx=10, pady=10)

        self.netCheckerButton = Button(self, text = 'EAGLE Net Checker', padx=5,
             pady=5, width=20, bg=bcolor, height=3, state='normal', fg=tcolor,
             font=tfont, activebackground=acolor, command=lambda: self.callEAGLENetCheckerApp())
        self.netCheckerButton.grid(row=baserow+1, column=basecolumn, padx=10, pady=10)

        self.quitButton = Button(self, text='Quit', padx=5, pady=5, width=20,
             height=3,bg=bcolor, fg=tcolor, font=tfont, activebackground=acolor,
             command = self.quit)
        self.quitButton.grid(row=baserow+1, column=basecolumn+1, padx=10, pady=10)

    def menuBar(self):
        self.menubar = Menu(self)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="New Window", command=None)
        filemenu.add_command(label="Open File", command=None)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)

        '''
        editmenu = Menu(self.menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=None)

        editmenu.add_separator()

        editmenu.add_command(label="Cut", command=None)
        editmenu.add_command(label="Copy", command=None)
        editmenu.add_command(label="Paste", command=None)
        editmenu.add_command(label="Delete", command=None)
        editmenu.add_command(label="Select All", command=None)
        self.menubar.add_cascade(label="Edit", menu=editmenu)
        '''

        helpmenu = Menu(self.menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=None)
        helpmenu.add_command(label="About...", command=None)
        self.menubar.add_cascade(label="Help", menu=helpmenu)

    def callURLToPartSpecsApp(self):
        pass

    def callEAGLENetlistCompilerAndOrgranizerApp(self):
        pass

    def callEAGLENetCheckerApp(self):
        nc = NetChecker(master=Toplevel()) # has some indexing errors


if __name__ == '__main__':
    root = Tkinter.Tk()
    app = MainMenu(root)
    root.mainloop()
