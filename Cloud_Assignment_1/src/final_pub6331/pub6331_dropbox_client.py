'''
Created on Feb 1, 2015

@author: Puneeth U Bharadwaj
'''

import os, time
# from rsa.bigfile import *
import gnupg

# def pub6331_dropbox(path_encrypt, path_temp, path_decrypt, temp_add, temp_rem, pubkey, privkey, client):
def pub6331_dropbox(path_encrypt, path_temp, path_decrypt, temp_add, temp_rem, client, encorsign):
    # https://www.dlitz.net/software/pycrypto/api/current/Crypto.PublicKey.RSA-module.html
    # RSA algorithm can be used for both confidentiality (encryption) and authentication (digital signature). 
    # It is worth noting that signing and decryption are significantly slower than verification and encryption. 
    # The cryptograhic strength is primarily linked to the length of the modulus n. In 2012, a sufficient length is deemed to be 2048 bits.
    
    if temp_add:
#         print 'Encrypting:', temp_add
#         with open(path_encrypt + temp_add, "rb") as infile, open(path_temp + temp_add, 'wb') as outfile:
#             encrypt_bigfile(infile, outfile, pubkey)
#         
#         upfile = open(path_temp + temp_add, 'rb')
#         response_up = client.put_file('/' + temp_add, upfile)
#         print 'Encrypted and uploaded to Dropbox:', temp_add            
#         
#         infile.close()
#         outfile.close()
#         upfile.close()            
#         os.remove(path_temp + temp_add)
#         
#         time.sleep(10)
#         
#         downfile = client.get_file('/' + temp_add)
#         print 'Downloaded from Dropbox:', temp_add
#         out = open(path_temp + temp_add, 'wb')
#         out.write(downfile.read())
#         out.close()
#         
#         with open(path_temp + temp_add, 'rb') as infile, open(path_decrypt + temp_add, "wb") as outfile:
#             decrypt_bigfile(infile, outfile, privkey)
#             
#         print 'Decrypted:', temp_add, '\n'
#             
#         infile.close()
#         outfile.close()
#         os.remove(path_temp + temp_add)

        gpg = gnupg.GPG()
        
        if encorsign == '1':
            print 'Encrypting:', temp_add
            
            with open(path_encrypt + temp_add, "rb") as f:
                status = gpg.encrypt_file(f,
                                          recipients=['puneeth.shopping@gmail.com'],
                                          output=path_temp + temp_add)
            
            upfile = open(path_temp + temp_add, 'rb')
            response_up = client.put_file('/' + temp_add, upfile, overwrite=True)
            print 'Encrypted and uploaded to Dropbox:', temp_add            
            
            upfile.close()
            os.remove(path_temp + temp_add)
            
            time.sleep(10)
            
            downfile = client.get_file('/' + temp_add)
            print 'Downloaded from Dropbox:', temp_add
            out = open(path_temp + temp_add, 'wb')
            out.write(downfile.read())
            out.close()
            
            with open(path_temp + temp_add, 'rb') as f:
                status = gpg.decrypt_file(f, passphrase='5!/v\P|_y()r@ng3Wit#M@|\|GO', output=path_decrypt + temp_add)
                
            print 'Decrypted:', temp_add, '\n'
    
            f.close()
            os.remove(path_temp + temp_add)
        
        if encorsign == '2': 
            print 'Signing:', temp_add
            
            f = open(path_encrypt + temp_add, "rb")
            signed_data = gpg.sign_file(f, output=path_temp + temp_add)
            f.close()
            f = open(path_temp + temp_add, 'rb')
            response_up = client.put_file('/' + temp_add, f, overwrite=True)
            print 'Signed and uploaded to Dropbox:', temp_add
            f.close()
            
            time.sleep(10)
            
            downfile = client.get_file('/' + temp_add)
            print 'Downloaded from Dropbox:', temp_add
            out = open(path_temp + temp_add, 'wb')
            out.write(downfile.read())
            out.close()
            
            f = open(path_temp + temp_add, 'r')
            verified = gpg.verify_file(f)
            if not verified: 
#                 raise ValueError("Signature could not be verified!")
                print "Signature could not be verified!"
            
            if verified: 
                print "The Signature was verified"
                
            f.close()
    
    if temp_rem:
        response_rem = client.file_delete('/' + temp_rem)
        print 'Removed from Dropbox:', temp_rem
        
