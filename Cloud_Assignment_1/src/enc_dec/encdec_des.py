'''
Created on Jan 28, 2015

@author: Puneeth U Bharadwaj
'''

import os, random, struct
from Crypto.Cipher import DES
import hashlib
import dropbox

def dropox_upload():
    client = dropbox.client.DropboxClient('S2etaYtslbAAAAAAAAAAOYGW4TnqkXbgUK-bGP9-C_9Qf_5EjGiF9jwf4Lu9_YYF')
     
    f = open('C:/Users/Puneeth U Bharadwaj/Desktop/Cloud Quiz 1/PUB_CloudQ1Online2.txt.des', 'rb')
    response = client.put_file('/PUB_CloudQ1Online2.txt.des', f)
    print 'uploaded: ', response
      
    folder_metadata = client.metadata('/')
    print 'metadata: ', folder_metadata
      
    f = client.get_file('/magnum-opus.txt')
    out = open('C:/Users/Puneeth U Bharadwaj/Desktop/Cloud Quiz 1/PUB_CloudQ1Online2.txt.des', 'wb')
    out.write(f.read())
    out.close()

def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    if not out_filename:
        out_filename = in_filename + '.des'

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = DES.new(key, DES.MODE_ECB, iv)
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
    
    print out_filename

def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = DES.new(key, DES.MODE_ECB, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)

# password = 'orange'
# key = hashlib.sha256(password).digest()
# encrypt_file(password, '../../plain.txt')
# decrypt_file(password, '../../plain.txt.enc')

encrypt_file('478     ', 'C:/Users/Puneeth U Bharadwaj/Desktop/Cloud Quiz 1/PUB_CloudQ1Online2.txt')
dropox_upload()
decrypt_file('478     ', 'C:/Users/Puneeth U Bharadwaj/Desktop/Cloud Quiz 1/PUB_CloudQ1Online2.txt.des')