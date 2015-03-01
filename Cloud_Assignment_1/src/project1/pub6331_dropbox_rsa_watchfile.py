'''
Created on Jan 30, 2015

@author: Puneeth U Bharadwaj
@course: CSE6331
@lab_number: Programming Assignment 1

References:
    http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html
    https://www.dropbox.com/developers/core/start/python
    https://www.dropbox.com/developers/core/docs/python
    http://stuvel.eu/files/python-rsa-doc/usage.html
    https://www.dlitz.net/software/pycrypto/api/current/Crypto.PublicKey.RSA-module.html
'''

import os, time, dropbox, rsa
from rsa.bigfile import *

# Get the stored key
access_token_file = open('access_token.txt')
access_token = access_token_file.read()
access_token_file.close()

#Connect to dropbox using Generated Access Token. Go to the appconsole to get generate this token
client = dropbox.client.DropboxClient(access_token)

#Print the linked account
# print 'linked account:', client.account_info()

#Generate public and private key
(pubkey, privkey) = rsa.newkeys(128)

#Set the folder to watch. User drops files here to sync with dropbox
path_encrypt = 'E:/workspace/CSE6331/upload/'
path_temp = 'E:/workspace/CSE6331/temp/'
path_decrypt = 'E:/workspace/CSE6331/download/'

#Start watching folder
#before = has list of files that were already present in the watch folder 'Upload'
before = dict ([(f, None) for f in os.listdir (path_encrypt)])
while True:
    time.sleep(5)
    
    #after = contains all files and newly added files in the 'upload' folder
    after = dict ([(f, None) for f in os.listdir (path_encrypt)])
    
    #added = contains all new added files in the 'upload' folder
    added = [f for f in after if not f in before]
    
    #removed = contains list of files removed from 'upload' folder
    removed = [f for f in before if not f in after]
    
    if added:
        print "Added: ", ", ".join (added)
        
        for i in range(len(added)):
            #if there are multiple files were added pop each one. Use os.path utility to find base folder name
            temp_add = added.pop()
            
            #https://www.dlitz.net/software/pycrypto/api/current/Crypto.PublicKey.RSA-module.html
            #RSA algorithm can be used for both confidentiality (encryption) and authentication (digital signature). 
            #It is worth noting that signing and decryption are significantly slower than verification and encryption. 
            #The cryptograhic strength is primarily linked to the length of the modulus n. In 2012, a sufficient length is deemed to be 2048 bits.
            with open(path_encrypt + temp_add, "rb") as infile, open(path_temp + temp_add, 'wb') as outfile:
                encrypt_bigfile(infile, outfile, pubkey)
            
            upfile = open(path_temp + temp_add, 'rb')
            response_up = client.put_file('/' + temp_add, upfile)
            print 'uploaded to dropbox:', response_up            
            
            infile.close()
            outfile.close()
            upfile.close()            
            os.remove(path_temp + temp_add)
            
            time.sleep(10)
            
            downfile = client.get_file('/' + temp_add)
            print 'downloaded from dropbox:', downfile
            out = open(path_temp + temp_add, 'wb')
            out.write(downfile.read())
            out.close()
            
            with open(path_temp + temp_add, 'rb') as infile, open(path_decrypt + temp_add, "wb") as outfile:
                decrypt_bigfile(infile, outfile, privkey)
                
            infile.close()
            outfile.close()
            os.remove(path_temp + temp_add)
    
    if removed:
        print "Removed: ", ", ".join (removed)
        for i in range(len(removed)):
            temp_rem = removed.pop()
            response_rem = client.file_delete('/' + temp_rem)
            print 'removed from dropbox:', response_rem
    
    before = after
            