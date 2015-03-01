'''
Created on Feb 1, 2015

@author: Puneeth U Bharadwaj
'''
import Tkinter
from Tkinter import *
from tkFileDialog import askopenfilenames
 
class multifilesApp(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)                                 

    def initializeUI(self):
        self.master.title('Select Files Application')
        self.grid()

        # Create the button to select files
        self.button_file_select = Button(self.master, text='Select Files', command=self.selectFiles, width=10)
        self.button_file_select.grid(row=30, column=70)
        self.button_file_select.pack()
        
        self.button_quit = Button(self.master, text='Quit', command=quit, width=10)
        self.button_quit.grid(row=50, column=70)
        self.button_quit.pack()

    def selectFiles(self):
        files = askopenfilenames()
        InputFileList = root.tk.splitlist(files)
        print('Files = ', InputFileList)

# Begin Main
# if __name__ == "__main__":
root = Tk()
root.minsize(width=400, height=100)
root.maxsize(width=400, height=200)
root.geometry("1200x800")

# Call the parser GUI application
app = multifilesApp(master=root)
app.initializeUI()

app.mainloop()