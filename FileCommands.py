'''
Created on Feb 13, 2015

@author: Max Ruiz
'''
import tkFileDialog as tf
import tkFileDialog
import xml.etree.ElementTree as ET
import re

#Generic file IO
class FileManip():
    def __init__(self):
        self.fileOptions()

    def fileOptions(self):
        self.fopt = file_opt = {}
        file_opt['defaultextension'] = '.csv'
        file_opt['filetypes'] = [('Comma Separated Values', '.csv'), ('Excel', '.xlsx'), ('All Files', '.*')]
        file_opt['initialdir'] = 'C:\\'
        file_opt['multiple'] = False
        file_opt['title'] = 'File'

    def openFile(self):
        return tf.askopenfile(mode = 'r', **self.fopt)

    def openFilename(self):
        return tf.askopenfilename(**self.fopt)

    def saveFile(self):
        return tf.asksaveasfile(mode = 'w', **self.fopt)

    def saveFilename(self):
        return tf.asksaveasfilename(**self.fopt)

    def getDirectory(self):
        return tf.askdirectory(**self.fopt)

    def extendFileOptions(self, xopts={}):
        for opt in xopts:
            try:
                self.fopt[opt] = xopts[opt]
            except:
                # poor/bad option
                pass

# Net Checker specific file IO
class HandleFile():
    def __init__(self):
        self.fileOptions()
        self.netList = {}
        self.nets = []
        self.fName = ''

    def fileOptions(self):
        self.fopen = file_opt = {}
        file_opt['defaultextension'] = '.txt'
        file_opt['filetypes'] = [('Text File', '.txt'), ('All Files', '.*')]
        file_opt['initialdir'] = 'C:\\'
        file_opt['multiple'] = False
        file_opt['title'] = 'Select Net List Text File'

    def openUsrFile(self):
        fileDir = tf.askopenfilename(**self.fopen)
        # Must parse loaded file because it comes as the whole directory instead of just the file.
        fileName = re.findall(r'/([\w]+\.txt)', fileDir)
        try:
            self.fName = fileName[0]
        except:
            self.fName = 'Could not parse file name.'
        try:

            self.file = open(fileDir, 'r')
            self.parseNetList()
            return 'File loaded: ' + self.fName # success message
        except:
            return 'Please open a file to continue' # error message

    def parseNetList(self):
        netName = ''
        parts = []
        done = False

        for row in self.file:
            line = row.split()
            lenLine = len(line)
            # The EAGLE net list has bogus lines it generates with the actual net list
            # This will filter out the bogus lines.
            # The format for the EAGLE net list is:
            # Trace Part Pad Pin Sheet
            # Part Pad Pin Sheet
            # . . . .
            if lenLine > 1 and lenLine < 6 and line[0] != 'Net':
                if lenLine > 4:
                    if done:
                        self.netList[netName] = parts
                        self.nets.append(netName)
                        parts = []

                    netName = line[0]
                    line.remove(netName) # The first element in the array greater than 4 is
                    # removed because it follows a difference pattern
                    # than subsequent entries and it is to be separated
                    # from the rest of the data until the end
                    # when everything is stored in a dictionary under
                    # that trace name

                parts.append(line)
                done = True

        self.file.close()

    def saveFileToXML(self):
        try: # This will catch the error caused by no file loaded yet

            self.xmlFileName = self.fName.replace('.txt', '.xml')

            try: # This will catch the error based on the XML file not having been created yet
                nlt = ET.parse(self.xmlFileName)
                netroot = nlt.getroot()
                netroot.clear()
            except:
                n = ET.Element('Netlist')
                tree = ET.ElementTree(n)
                tree.write(self.xmlFileName)
                nlt = ET.parse(self.xmlFileName)
                netroot = nlt.getroot()

            for net in self.nets:
                trace = ET.SubElement(netroot, 'Trace')
                trace.set('TName', net)

                for parts in self.netList[net]:
                    part = ET.SubElement(trace, 'Part')
                    part.set('PName', parts[0])

                    pad = ET.SubElement(part, 'Pad')
                    pad.text = str(parts[1])
                    pin = ET.SubElement(part, 'Pin')
                    pin.text = str(parts[2])
                    sheet = ET.SubElement(part, 'Sheet')
                    sheet.text = str(parts[3])

            nlt.write(self.xmlFileName)
            return 'XML file has been saved as ' + self.xmlFileName # success message

        except:
            return 'Please open a net list text file first.' # error message

    def getNets(self):
        return self.nets

    def getNetlist(self):
        return self.netList

    def getFName(self):
        return self.fName
