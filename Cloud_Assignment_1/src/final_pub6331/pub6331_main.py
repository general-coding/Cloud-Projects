'''
Created on Feb 1, 2015

@author: Puneeth U Bharadwaj
'''

from pub6331_auth import pub6331_dropbox_auth, pub6331_googledrive_auth
from pub6331_dropbox_client import pub6331_dropbox
from pub6331_googledrive_client import pub6331_googledrive 
# import rsa
import os

client = pub6331_dropbox_auth()

gauth = pub6331_googledrive_auth()
# print gauth

#Generate public and private key
# (pubkey, privkey) = rsa.newkeys(128)

#Set the folder to watch. User drops files here to sync with dropbox
path_encrypt = 'E:/workspace/CSE6331/upload/'
path_temp = 'E:/workspace/CSE6331/temp/'
path_decrypt = 'E:/workspace/CSE6331/download/'

#Start watching folder
#before = has list of files that were already present in the watch folder 'Upload'
before = dict ([(f, None) for f in os.listdir (path_encrypt)])
print 'Please add files to sync'
while True:
#     time.sleep(5)
    
    #after = contains all files and newly added files in the 'upload' folder
    after = dict ([(f, None) for f in os.listdir (path_encrypt)])
    
    #added = contains all new added files in the 'upload' folder
    added = [f for f in after if not f in before]
    
    #removed = contains list of files removed from 'upload' folder
    removed = [f for f in before if not f in after]
    
    if added:        
        for i in range(len(added)):
            #if there are multiple files were added pop each one. Use os.path utility to find base folder name
            temp_add = added.pop()
            encorsign = raw_input('Enter 1. Encrypt \t 2. Sign : ').strip()
            
#             pub6331_dropbox(path_encrypt, path_temp, path_decrypt, temp_add, None, pubkey, privkey, client)   
#             pub6331_googledrive(path_encrypt, path_temp, path_decrypt, temp_add, None, pubkey, privkey, gauth)

            pub6331_dropbox(path_encrypt, path_temp, path_decrypt, temp_add, None, client, encorsign)       
            pub6331_googledrive(path_encrypt, path_temp, path_decrypt, temp_add, None, gauth, encorsign)
    
    if removed:
        for i in range(len(removed)):
            #if any files are removed from the sync folder, the same will be deleted in dropbox and googledrive
            temp_rem = removed.pop()
            
            status = False
#             pub6331_dropbox(path_encrypt, path_temp, path_decrypt, None, temp_rem, pubkey, privkey, client)
#             pub6331_googledrive(path_encrypt, path_temp, path_decrypt, None, temp_rem, pubkey, privkey, gauth)

            pub6331_dropbox(path_encrypt, path_temp, path_decrypt, None, temp_rem, client, None)
            pub6331_googledrive(path_encrypt, path_temp, path_decrypt, None, temp_rem, gauth, None)
    
    before = after