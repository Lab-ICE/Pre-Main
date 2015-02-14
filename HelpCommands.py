'''
Created on Feb 13, 2015

@author: Max Ruiz
'''

import Tkinter
from Tkinter import *


class HelpCommands():
    def __init__(self):
        pass

    # This method goes over the fundamental use of this app.
    def help(self):
        helpWindow = Toplevel()
        helpFrame = Frame(helpWindow)
        helpLst = Listbox(helpFrame, height=10, width=50)
        helpStatement = ['To use: go to \'File\' and select open.',
                         'Choose the net list file you want to view.',
                         'Your file should be a text file.',
                         'Once loaded you can select traces showing',
                         'all the parts that are connected to that trace.',
                         'You can also save files to XML (after opened)',
                         'by going to \'File\' and selecting \'Save to XML\'']
        try:
            helpLst.delete(0, helpLst.size())
            for l in range(len(helpStatement)):
                helpLst.insert(l, helpStatement[l])
        except:
            for l in range(len(helpStatement)):
                helpLst.insert(l, helpStatement[l])
        helpFrame.pack()
        helpLst.pack()

    # This method provides a small explanation what this app is about.
    def about(self):
        aboutWindow = Toplevel()
        aboutFrame = Frame(aboutWindow)
        aboutLst = Listbox(aboutFrame, height=12, width=50)
        aboutStatement = ['Net list eXAMiner Written by Max A. Ruiz',
                          'This program is designed to help simplify trace',
                          'connection viewing and make finding part connection',
                          'errors much more clear and visible.',
                          'Net list eXAMiner is self contained using Python 2.7.X',
                          'Imported libraries contained are:',
                          '+ xml.etree.ElementTree',
                          '+ tkinter',
                          '+ filedialog',
                          '+ sys']
        try:
            aboutLst.delete(0, aboutLst.size())
            for l in range(len(aboutStatement)):
                aboutLst.insert(l, aboutStatement[l])
        except:
            for l in range(len(aboutStatement)):
                aboutLst.insert(l, aboutStatement[l])
        aboutFrame.pack()
        aboutLst.pack()

