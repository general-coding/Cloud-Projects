'''
Created on Feb 2, 2015

@author: Puneeth U Bharadwaj
'''

from Tkinter import *
import Tkinter,tkFileDialog
import tkMessageBox
import ttk

def selectedVal():
    selection = str(EncryptorDecrypt.get())
    return selection

def uploadFile(): 
    file = tkFileDialog.askopenfile(parent=General,mode='rb',title='Choose a file')
    sel = selectedVal()
#     if file != None:
#         if sel == '1':
#             DropBoxObj.uploadFileToDropBox(file.name, 'Sign', False)
#             GoogleDriveObj.uploadFileToGDrive(file.name, 'Encrypt', False)
#         elif sel == '2':
#             DropBoxObj.uploadFileToDropBox(file.name, 'Encrypt', False)
#             GoogleDriveObj.uploadFileToGDrive(file.name, 'Encrypt', False)
#         else:
#             tkMessageBox.showinfo("Wrong selection", "Please select either digitally sign / encryption to proceed")
#     RefreshFileList_DBox()

"""
Method:   RefreshFileList_DBox()

Refresh the drop box file list in the list box
"""    
def RefreshFileList_DBox():
    listbox_DBox.delete(0, END)
#     FileList =DropBoxObj.listDBoxFiles()
#     for i in FileList:
#         listbox_DBox.insert(END,str(i).replace("/","") )

"""
Method:   RefreshFileList_GDrive()

Refresh the google drive file list in the list box
"""            
def RefreshFileList_GDrive():
    listbox_GDrive.delete(0, END)
#     FileList = GoogleDriveObj.listGDriveFiles()
#     for i in FileList:
#         listbox_GDrive.insert(END,str(i).replace("/","") ) 

"""
Method:   downloadFileDropBox()

Download's the file from Drop Box and decrypt's the same
"""
def downloadFileDropBox():
    Item = listbox_DBox.curselection()
    GetFile=listbox_DBox.get(Item)
    selval = selectedVal()
    
#     if selval == '1':
#         DropBoxObj.downloadFileFromDropBox(GetFile,'Sign')
#     else:
#         DropBoxObj.downloadFileFromDropBox(GetFile,'Decrypt')

"""
Method:   downloadFileGDrive()

Download's the file from Google drive and decrypt's the same
"""
def downloadFileGDrive():
    Item = listbox_GDrive.curselection()
    GetFile=listbox_GDrive.get(Item)
#     GoogleDriveObj.downloadFileFromGDrive(GetFile, 'Decrypt')

#Tkinter window object
MainWindow = Tk()
MainWindow.title('Cloud Sync App')
MainWindow.geometry('500x500')

#Get tabs using ttk Notebook
_tabs = ttk.Notebook(MainWindow)
_tabs.pack(fill = 'both', expand='yes')

#Create tabs
General = Text(MainWindow)
DBox = Text(MainWindow)
GDrive = Text(MainWindow)

#Assign names to created tabs
_tabs.add(General, text='General')
_tabs.add(DBox, text='Dropbox')
_tabs.add(GDrive, text='Google Drive')

#Create a Label to be displyed on the General Tab
GenLabel = Label(General, fg="Blue", text='Please select either Encryption or Digitally Signing method', bg='white', pady=5, font=("Helvetica", 11))
GenLabel.pack()

#User selects Encryption/Decryption or Digitally Sign
EncryptorDecrypt = IntVar()
R1 = Radiobutton(General, text="Digitally Sign", variable=EncryptorDecrypt, value=1,cursor='hand2', bg='white', command=selectedVal)
R1.pack(side=TOP)
    
R2 = Radiobutton(General, text="Encryption", variable=EncryptorDecrypt, value=2, cursor='hand2', bg='white', command=selectedVal)
R2.pack(side=TOP)
    
UploadButton = Button(General, width=15, text="Upload", cursor = 'hand2', command=uploadFile)
UploadButton.pack(pady=15)

#Drop box description label and list box to display files
DboxLabel = Label(DBox, fg="Blue", text='Please select one of the files from the list below to download', bg='white', pady=5,font=("Helvetica", 11))
DboxLabel.pack()     
listbox_DBox = Listbox(DBox,width=60, height = 17, cursor = 'arrow')
listbox_DBox.pack()

#Google Drive description label and list box to display files
DboxLabel = Label(GDrive, fg="Blue", text='Please select one of the files from the list below to download', bg='white', pady=5,font=("Helvetica", 11))
DboxLabel.pack()
listbox_GDrive = Listbox(GDrive,width=60, height = 17, cursor = 'arrow')
listbox_GDrive.pack()

#Refresh the list box to get the latest files from respective drives
RefreshFileList_DBox()
RefreshFileList_GDrive()

#Download and Refresh buttons in Drop Box tab
RefreshButtonDBox = Button(DBox, text="Refresh", cursor = 'hand2', command=RefreshFileList_DBox)
RefreshButtonDBox.pack(padx=5, pady=15, side=RIGHT)    
DownloadButtonDBox = Button(DBox, text="Download", cursor = 'hand2', command=downloadFileDropBox)
DownloadButtonDBox.pack(padx=5, pady=15, side=RIGHT)

#Download and Refresh buttons in Google Drive tab
RefreshButtonGDrive = Button(GDrive, text="Refresh", cursor = 'hand2', command=RefreshFileList_GDrive)
RefreshButtonGDrive.pack(padx=5, pady=15, side=RIGHT)    
DownloadButtonGDrive = Button(GDrive, text="Download", cursor = 'hand2', command=downloadFileGDrive)
DownloadButtonGDrive.pack(padx=5, pady=15, side=RIGHT)

MainWindow.mainloop()