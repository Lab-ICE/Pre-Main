'''
Created on Feb 14, 2015

@author: Thomas
'''

'''


@author: Thomas
'''


# Working TestBench for extracting url and placing it into a list
from Tkinter import * 
URL_List=list()

class getURL(Frame):
    def createWidgets(self):
        #Labels the GUI
        self.title_text=Label(self)
        self.title_text["text"]="URL Extractor"
        self.title_text.pack(padx=1)

        #Entry box
        self.url_input=Entry(self)
        self.url_input.pack(padx=5)
                
        self.label_display_urls=Label(self)
        self.label_display_urls["text"]="URLS"
        self.label_display_urls.pack(padx=10) 
              
        
        # def to send url to a list and delete whats in the field
        url=StringVar()  
        def returnURL():
            URL_List.append(self.url_input.get())
            self.url_input.delete(0,END)
            url.set(URL_List)
               
        #Button for excuting the action  
        self.Enter=Button(self)
        
        self.Enter["text"]="Enter"
        #Executes the returnURL
        self.Enter["command"]=returnURL
        self.Enter.pack(padx=20)
        #Displays the text in the list 
        self.display_urls=Label(self,textvariable=url,relief=RAISED)
        self.display_urls.pack(padx=15)
        
    #initializes the program
    def __init__(self,master):
        Frame.__init__(self,master)
        self.pack()
        self.createWidgets()
        
    
    
#create an instance of TK
root=Tk()
#creates a loop for the get url class
url_Widget=getURL(master=root)
url_Widget.mainloop()

#urlInputText=Label(top,text="Enter URl")
#urlInputText.pack(side=LEFT)
#urlInput=Entry(top)
#urlInput.pack(side=RIGHT)
#top.mainloop()

    