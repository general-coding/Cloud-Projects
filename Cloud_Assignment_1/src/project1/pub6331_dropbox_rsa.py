'''
Created on Jan 29, 2015

@author: Puneeth U Bharadwaj

Ref: http://stuvel.eu/files/python-rsa-doc/usage.html
'''

import rsa
from rsa.bigfile import *
from dropbox import client, session
from Tkinter import Tk
from tkFileDialog import askopenfilename
import os

(pubkey, privkey) = rsa.newkeys(128)

# Get the stored key
token_file = open('dropbox_token.txt')
app_key, app_secret, access_type, password, token_key, token_secret = token_file.read().split('|')
token_file.close()

# Initialize session and the client
sess = session.DropboxSession(app_key, app_secret, access_type)
sess.set_token(token_key, token_secret)

client = client.DropboxClient(sess)

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
in_filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print 'selected file: ', in_filename

enc_filename = '../../upload/' + in_filename.split('/')[-1]

with open(in_filename, 'rb') as infile, open(enc_filename, 'wb') as outfile:
    encrypt_bigfile(infile, outfile, pubkey)

upfile = open(enc_filename, 'rb')
response = client.put_file('/' + in_filename.split('/')[-1], upfile)
print 'uploaded: ', response
upfile.close()

new_name = '../../upload/' + in_filename.split('/')[-1]
os.rename(enc_filename, new_name)
print 'encrypted file: ', new_name

downfile, metadata = client.get_file_and_metadata('/' + in_filename.split('/')[-1])
out = open('../../download/' + in_filename.split('/')[-1] + '.enc', 'wb')
out.write(downfile.read())
out.close()
 
with open('../../download/' + in_filename.split('/')[-1] + '.enc', 'rb') as infile, open('../../download/' + in_filename.split('/')[-1], 'wb') as outfile:
    decrypt_bigfile(infile, outfile, privkey)
    
os.remove('../../download/' + in_filename.split('/')[-1] + '.enc')

print 'done'