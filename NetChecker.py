'''
Created on Sep 18, 2014

@author: Max Ruiz
'''

import xml.etree.ElementTree as ET
import re
from Tkinter import *
import tkFileDialog
import sys

#------------------------------

class NetChecker(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.initGui() # Sets up gui - all frames and widgets

        self.traceList.bind('<<ListboxSelect>>', self.updatePartsList)
        self.partsList.bind('<<ListboxSelect>>', self.updatePadPinSheet)

        self.fillMenuButtons() # adds file menu for extra functionality

        if master != None:
            master.title('ICE - Net Checker')
            master.config(menu=self.menubar)
            self.pack()


    def initGui(self):
        self.initNetCheckFrame()
        self.initEagleFileNameLB()
        self.initLog()
        self.initTraceList()
        self.initPartsList()
        self.initPadPinSheetList()

    # Overall frame that contains all other frames and widgets
    # It resides in the main Tk() root frame
    # The reason for this frame is because it can have a label
    def initNetCheckFrame(self):
        self.netCheckFrame = LabelFrame(self, text='Net list eXAMiner')
        self.mainFrame = self.netCheckFrame
        self.netCheckFrame.pack()

    # List box widget that displays name of opened file
    def initEagleFileNameLB(self):
        eagleLblFrm = LabelFrame(self.mainFrame, text='EAGLE Net list')
        self.eagFLB = Listbox(eagleLblFrm, height=1, width=15)
        self.eagFLB.pack(side='left')
        self.eagFLB.insert(0, 'No File')
        eagleLblFrm.pack(anchor=W)

    # Log will display user activity as well as display user errors
    def initLog(self):
        logFrame = LabelFrame(self.mainFrame, text='Log')
        self.logLst = Listbox(logFrame, height=7, width=151)
        self.logLst.pack()
        logFrame.pack(side='bottom', anchor=W)

    # This list box will display all traces found in an EAGLE CAD generated net list
    # The list box will fill up only after a proper file has been chosen and parsed
    def initTraceList(self):
        trcLstFrm = LabelFrame(self.mainFrame, text='Traces')
        traceScrlBr = Scrollbar(trcLstFrm)
        traceScrlBr.pack(side='left', fill=Y)
        self.traceList = Listbox(trcLstFrm, width=40, height=21)
        self.traceList.pack(side='left')
        trcLstFrm.pack(side='left')
        traceScrlBr.config(command=self.traceList.yview)

    # This list box will display all parts attached to a specific trace
    # when a user clicks on the corresponding trace
    def initPartsList(self):
        prtLstFrm = LabelFrame(self.mainFrame, text='Parts')
        partsScrlBr = Scrollbar(prtLstFrm)

        # This trace label will show the name of the trace under inspection
        # while the user is looking at the parts list
        self.trcLabel = StringVar()
        self.trcLabel.set('-')
        self.trcLblForPrtLst = Label(prtLstFrm, textvariable=self.trcLabel, width=15)
        self.trcLblForPrtLst.pack(side='top', anchor=W)

        partsScrlBr.pack(side='left', fill=Y)
        self.partsList = Listbox(prtLstFrm, width=40, height=20)
        self.partsList.pack(side='left')

        prtLstFrm.pack(side='left')
        partsScrlBr.config(command=self.partsList.yview)

    # Three list boxes are generated here because they are all tied together
    # The list boxes will display the Pad, Pins, and Sheets respectively
    # for each part a user selects from the parts list box
    def initPadPinSheetList(self):
        pdLstFrm = LabelFrame(self.mainFrame, text='Pad')
        pnLstFrm = LabelFrame(self.mainFrame, text='Pin')
        sheetLstFrm = LabelFrame(self.mainFrame, text='Sheet')

        self.padLst = Listbox(pdLstFrm, height=21, width=20)
        self.padLst.pack(side='top')

        self.pinLst = Listbox(pnLstFrm, height=21, width=20)
        self.pinLst.pack(side='top')

        self.sheetLst = Listbox(sheetLstFrm, height=21, width=20)
        self.sheetLst.pack(side='top')

        pdLstFrm.pack(side='left')
        pnLstFrm.pack(side='left')
        sheetLstFrm.pack(side='left')

    # This function is used to iterate through the parts belonging to a
    # specific trace that the user has selected from the trace list box
    # and loads them into the parts list box.
    def updatePartsList(self, event):
        # Delete any parts currently in the parts list box
        self.partsList.delete(0, self.partsList.size())

        # get selected trace name from trace list box selection
        self.curTrcTxt = self.traceList.get(self.traceList.curselection()[0])
        self.trcLabel.set(self.curTrcTxt)

        partLists = []
        self.parts = []
        for traces in self.traces:
            if self.curTrcTxt == traces:
                partLists = self.netList[traces] # load in part lists into another list

        for parts in partLists:
            self.parts.append(parts[0]) # take first element of each part list (Name of Part)

        for i in range(len(self.parts)):
            # self.partsList is a list box being filled with the names of parts from partLists
            # notice the different placement of "s"'s in the var name
            self.partsList.insert(i, str(self.parts[i]))

        self.curTrcTxt = self.traceList.get(self.traceList.curselection()[0])
        self.log = str(self.curTrcTxt)
        self.updateLog()

    # The trace list box updates only once after the user has selected which file they want
    # to view.
    def updateTraceList(self):
        for i in range(len(self.traces)):
            self.traceList.insert(i, str(self.traces[i]))

    # The Pad, Pin and Sheet list boxes need to be updated each time a new part has been
    # selected from the parts list box. This function will fill each respective list box
    # with its respective information.
    def updatePadPinSheet(self, event):
        if self.padLst.size() > 0:
            self.padLst.delete(0, self.padLst.size())
        if self.pinLst.size() > 0:
            self.pinLst.delete(0, self.pinLst.size())
        if self.sheetLst.size() > 0:
            self.sheetLst.delete(0, self.sheetLst.size())

        self.curPrtTxt = self.partsList.get(self.partsList.curselection()[0])

        self.log = self.curTrcTxt + ' -> ' + str(self.curPrtTxt)
        self.updateLog()

        for x in self.netList[self.curTrcTxt]:
            if x[0] == self.curPrtTxt:
                self.padLst.insert(1, x[1])
                self.pinLst.insert(1, x[2])
                self.sheetLst.insert(1, x[3])

    # This function will update the file name list box to let the user see which file
    # they are viewing. The list box is visible at the top left side of the window.
    def updateEagleFileNameLB(self):
        try:
            self.eagFLB.delete(0, self.eagFLB.size())
            self.eagFLB.insert(0, self.usrFileName)
        except:
            self.eagFLB.insert(0, self.usrFileName)

    # This command takes the string variable "self.log" and loads it into the log list box
    def updateLog(self):
        try:
            self.logLst.delete(0)
        except:
            pass
        self.logLst.insert(0, self.log)

    # This function uses Tkinter's filedialog library to allow the user to find their net list
    # text file. It is protected to only except text files.
    def openUsrFile(self):
        fileDir = tkFileDialog.askopenfilename(title = "Choose user net list", filetypes = (("Text files","*.txt"),("all files","*.*")))
        # Must parse loaded file because it comes as the whole directory instead of just the file.
        fileName = re.findall(r'/([\w]+\.txt)', fileDir)
        try:
            self.usrFileName = fileName[0]
            self.usrF = open(self.usrFileName, 'r')
            self.parseFile()
            self.log = 'File loaded: ' + self.usrFileName
            self.updateLog()
            self.updateEagleFileNameLB()
        except:
            self.log = "Please open a file to continue"
            self.updateLog()

    # This file will take the loaded net list text file the user has loaded and parse it
    # according to the typical format EAGLE CAD exports their net list files as.
    # The function then stores everything into a program stored dictionary and
    # consecutive lists for traces -> parts -> pads,pins,sheets
    # The use of program based memory storage will be removed in the next update and
    # will look everything up frame a generated XML document for more robust data storage
    # and access.
    def parseFile(self):

        self.netList = {}
        netName = ''
        parts = []
        done = False

        for line in self.usrF:
            l = line
            c = l.split()
            # The EAGLE net list has bogus lines it generates with the actual net list
            # This will filter out the bogus lines.
            # The format for the EAGLE net list is:
            # Trace Part Pad Pin Sheet
            # Part Pad Pin Sheet
            # . . . .
            if len(c) > 1 and len(c) < 6 and c[0] != 'Net':
                if len(c) > 4:
                    if done:
                        self.netList[netName] = parts
                        parts = []

                    netName = c[0]
                    c.remove(netName) # The first element in the array greater than 4 is
                    # removed because it follows a difference pattern
                    # than subsequent entries and it is to be separated
                    # from the rest of the data until the end
                    # when everything is stored in a dictionary under
                    # that trace name

                parts.append(c)
                done = True

        self.usrF.close()

        self.traces = list(x for x in self.netList.keys())
        self.updateTraceList()

    # This method stores the user-loaded EAGLE CAD net list file into an xml file.
    # This method is currently an optional one, however this will be changed to
    # a required option in the next update.
    def saveFileToXML(self):
        try: # This will catch the error caused by no file loaded yet

            self.xmlFileName = self.usrFileName.replace('.txt', '.xml')

            try: # This will catch the error based on the XML file not having been created yet
                nlt = ET.parse(self.xmlFileName)
                net = nlt.getroot()
                net.clear()
            except:
                n = ET.Element('Netlist')
                tree = ET.ElementTree(n)
                tree.write(self.xmlFileName)
                nlt = ET.parse(self.xmlFileName)
                net = nlt.getroot()

            # Measurements for statistics
            numOfTraces = 0
            numOfParts = 0
            maxSheets = 0

            for key in self.netList.keys():
                trace = ET.SubElement(net, 'Trace')
                trace.set('TName', key)
                numOfTraces = numOfTraces + 1

                for parts in self.netList[key]:
                    part = ET.SubElement(trace, 'Part')
                    part.set('PName', parts[0])
                    numOfParts = numOfParts + 1

                    pad = ET.SubElement(part, 'Pad')
                    pad.text = str(parts[1])
                    pin = ET.SubElement(part, 'Pin')
                    pin.text = str(parts[2])
                    sheet = ET.SubElement(part, 'Sheet')
                    sheet.text = str(parts[3])
                    t0 = int(parts[3])
                    if t0 > maxSheets:
                        maxSheets = t0

            nlt.write(self.xmlFileName)
            self.log = 'XML file has been saved as ' + self.xmlFileName
            self.updateLog()
        except:
            self.log = 'Please open a net list text file first.'
            self.updateLog()

    ''' Future update methods
    def addTraceAttribute(self):
        pass

    def addPartAttribute(self):
        pass

    def addPadAttribute(self):
        pass

    def addPinAttribute(self):
        pass
    '''

    # This method creates a separate instance of the net list eXAMiner application.
    def newInstance(self):
        newApp = Toplevel()
        app = NetChecker(master=newApp)
        #app.mainloop()

    # This method provides a small explanation what this app is about.
    def aboutCommand(self):
        aboutWindow = Toplevel()
        aboutFrame = Frame(aboutWindow)
        aboutLst = Listbox(aboutFrame, height=12, width=50)
        aboutStatement = ['Net list eXAMiner Written by Max A. Ruiz',
                          'This program is designed to help simplify trace',
                          'connection viewing and make finding part connection',
                          'errors much more clear and visible.',
                          'Net list eXAMiner is self contained using Python 3.4',
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

    # This method goes over the fundamental use of this app.
    def helpCommand(self):
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

    # This method is used to generate the file menu. The file menu is applied
    # to the Tk() root frame, not the self.mainFrame that everything else belongs to.
    # This is because it was meant to be this way.
    def fillMenuButtons(self):
        self.menubar = Menu(self)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="New Window", command=self.newInstance)
        filemenu.add_command(label="Open File", command=self.openUsrFile)
        filemenu.add_command(label="Save to XML", command=self.saveFileToXML)

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
        helpmenu.add_command(label="Help Index", command=self.helpCommand)
        helpmenu.add_command(label="About...", command=self.aboutCommand)
        self.menubar.add_cascade(label="Help", menu=helpmenu)

'''
root = Tk()
app = NetView(master=root)
app.mainloop()
'''
