'''
Created on Feb 3, 2015

@author: Puneeth U Bharadwaj
'''

from Tkinter import Tk, Text, Label, Button, Listbox, Scrollbar, END, RIGHT, Y, BOTH
from ttk import Notebook
import tkFileDialog
import tkMessageBox
import dropbox_client
# import googledrive_client

#Upload File. Here the user selects the file to uploaded
def uploadFile():
    _file_selected = tkFileDialog.askopenfile(parent=_tab_upload, title="Choose a file", mode='rb')
#     print _file_selected.read()
    if _file_selected == None:
        tkMessageBox.showerror("Error!", "Please select a file to upload")
    else:
        _client_dropbox.uploadFileToDropbox(_file_selected.name)
#         _client_googledrive.uploadFileToGoogleDrive(_file_selected.name)
        tkMessageBox.showinfo("Info!", _file_selected.name.split('/')[-1] + " is uploaded successfully")

def downloadFile_Dropbox():
    _file_item = _listbox_dropBox.curselection()
    _file_selected = _listbox_dropBox.get(_file_item)    
    _client_dropbox.downloadFileFromDropbox(_file_selected)
    tkMessageBox.showinfo("Info!", "Downloaded " + _file_selected + " from Dropbox")
    
def refresh_dropbox_list():
    _listbox_dropBox.delete(0, END)
    _list_file = _client_dropbox.listDropboxFiles()
    for _file in _list_file:
        _listbox_dropBox.insert(END,str(_file).replace("/",""))
        
def downloadFile_GoogleDrive():
    _file_item = _listbox_googleDrive.curselection()
    _file_selected = _listbox_googleDrive.get(_file_item)
#     _client_googledrive.downloadFileFromGoogleDrive(_file_selected)
    tkMessageBox.showinfo("Info!", "Downloaded " + _file_selected + " from Google Drive")
    
def refresh_googledrive_list():
    _listbox_googleDrive.delete(0, END)
#     _list_file = _client_googledrive.listGoogleDriveFiles()
#     for _file in _list_file:
#         _listbox_googleDrive.insert(END, str(_file).replace("/",""))

#Create the objects to communicate with DBox
_client_dropbox = dropbox_client.DropBox()
# _client_googledrive = googledrive_client.GoogleDrive()

#Create a Main Window to display
MainWindow = Tk()
MainWindow.title('Cloud Sync')
MainWindow.minsize(500, 500)
MainWindow.maxsize(500, 500)

#Create tabs
_tabs = Notebook(MainWindow)
_tabs.pack(fill='both', expand='yes')

_tab_upload = Text(MainWindow)
_tab_dropBox = Text(MainWindow)
_tab_googleDrive = Text(MainWindow)

#Add tabs to the Main Window
_tabs.add(_tab_upload, text='Upload')
_tabs.add(_tab_dropBox, text='Dropbox')
_tabs.add(_tab_googleDrive, text='Google Drive')

#Label is used to display information to user
_label_upload = Label(_tab_upload, fg='Red', text='Choose a file to upload', bg='white', font=("Calibri", 10))
_label_upload.pack(pady=10)

#Button let's the user select a file to upload
_button_upload = Button(_tab_upload, text="Upload", pady=5, width=10, command=uploadFile)
_button_upload.pack(pady=10)

#Lets user choose the file to be downloaded from Dropbox/Google Drive
_label_dropBox = Label(_tab_dropBox, fg='Red', text='Choose a file to download', bg='white', font=("Calibri", 10))
_label_dropBox.pack(pady=10)
_listbox_dropBox = Listbox(_tab_dropBox, width=50, height=15)
_listbox_dropBox.pack(pady=10, fill=BOTH, expand=True)
# for line in range(1000):
#     _listbox_dropBox.insert(END, line)
_scrollbar_dropbox = Scrollbar(_listbox_dropBox)
_scrollbar_dropbox.pack(side=RIGHT, fill=Y)
_scrollbar_dropbox.config(command=_listbox_dropBox.yview)

_label_googleDrive = Label(_tab_googleDrive, fg='Red', text='Choose a file to download', bg='white', font=("Calibri", 10))
_label_googleDrive.pack(pady=10)
_listbox_googleDrive = Listbox(_tab_googleDrive, width=50, height=15)
_listbox_googleDrive.pack(pady=10, fill=BOTH, expand=True)
# for line in range(1000):
#     _listbox_googleDrive.insert(END, line)
_scrollbar_googleDrive = Scrollbar(_listbox_googleDrive)
_scrollbar_googleDrive.pack(side=RIGHT, fill=Y)
_scrollbar_googleDrive.config(command=_listbox_googleDrive.yview)

# #Refresh the list before download
refresh_dropbox_list()
refresh_googledrive_list()

#Lets user download a selected file or refresh the listh
# _button_download_dropBox=Button(_tab_dropBox, text="Download", command=downloadFile_Dropbox)
# _button_download_dropBox.pack(padx=5, pady=10, side=RIGHT)
# _button_refresh_dropBox=Button(_tab_dropBox, text="Refresh", command=refresh_dropbox_list)
# _button_refresh_dropBox.pack(padx=5, pady=10, side=RIGHT)

# _button_download_googleDrive=Button(_tab_googleDrive, text="Download", command=downloadFile_GoogleDrive)
# _button_download_googleDrive.pack(padx=5, pady=10, side=RIGHT)
# _button_refresh_googleDrive=Button(_tab_googleDrive, text="Refresh", command=refresh_googledrive_list)
# _button_refresh_googleDrive.pack(padx=5, pady=10, side=RIGHT)

MainWindow.mainloop()