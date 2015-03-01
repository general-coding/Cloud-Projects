'''
Created on Jan 27, 2015

@author: Puneeth U Bharadwaj

This is the dropbox project

Ref: http://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto
'''

# Include the Dropbox SDK
import os, random, struct
from dropbox import client, session
from Tkinter import Tk
from tkFileDialog import askopenfilename
from Crypto.Cipher import AES
import hashlib

def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_filename:
            Name of the input file

        out_filename:
            If None, '<in_filename>.enc' will be used.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = '../../upload/' + in_filename.split('/')[-1] + '.enc'

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))
    
    return out_filename

def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    """ Decrypts a file using AES (CBC mode) with the
        given key. Parameters are similar to encrypt_file,
        with one difference: out_filename, if not supplied
        will be in_filename without its last extension
        (i.e. if in_filename is 'aaa.zip.enc' then
        out_filename will be 'aaa.zip')
    """
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)
            
    return out_filename

# Get your app key and secret from the Dropbox developer website
# app_key='kocqylpzj1nohtb'
# app_secret='dq2ydvrfl26f2z9'
# access_type='app_folder'

# Get the stored key
token_file = open('dropbox_token.txt')
app_key, app_secret, access_type, password, token_key, token_secret = token_file.read().split('|')
token_file.close()
key = hashlib.sha256(password).digest()

# Initialize session and the client
sess = session.DropboxSession(app_key, app_secret, access_type)
sess.set_token(token_key, token_secret)

client = client.DropboxClient(sess)

# print 'linked account: ', client.account_info()

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print 'selected file: ', filename

# upfile = open('E:/workspace/CSE6331/upload/working-draft.txt', 'rb')
# upfile = open(filename, 'rb')
# l = []
# l = filename.split('/')
# # print l[-1]

encfile = encrypt_file(key, filename)

upfile = open(encfile, 'rb')
response = client.put_file('/' + filename.split('/')[-1], upfile)
print 'uploaded: ', response
upfile.close()

new_name = '../../upload/' + filename.split('/')[-1]
os.rename(encfile, new_name)
print 'encrypted file: ', new_name

# folder_metadata = client.metadata('/')
# print 'metadata: ', folder_metadata
# 
downfile, metadata = client.get_file_and_metadata('/' + filename.split('/')[-1])
# print 'downfile: ', downfile
out = open('../../download/' + filename.split('/')[-1] + '.enc', 'wb')
out.write(downfile.read())
out.close()
decrypt_file(key, '../../download/' + filename.split('/')[-1] + '.enc')
os.remove('../../download/' + filename.split('/')[-1] + '.enc')
print 'done'
# print 'metadata 2: ', metadata