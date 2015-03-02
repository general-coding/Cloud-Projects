'''
Created on Feb 9, 2015

@author: Puneeth U Bharadwaj
'''

import gnupg
from pprint import pprint

def exportkeys():
    gpg = gnupg.GPG()
    ascii_armored_public_keys = gpg.export_keys('66C8F2C8')
    ascii_armored_private_keys = gpg.export_keys('66C8F2C8', True)
    with open('pub_keys.asc', 'w') as f:
        f.write(ascii_armored_public_keys)
        f.write(ascii_armored_private_keys)
        
    gpg.send_keys('keyserver.ubuntu.com')

def importkeys(filename, servername, keyid):
    gpg = gnupg.GPG()
    if filename:
        key_data = open(filename, 'r').read()
        import_result = gpg.import_keys(key_data)
    
    if servername:
        res = gpg.recv_keys(servername, keyid)
        pprint(res.results)
        

def listkeys():
    gpg = gnupg.GPG()
    pub_key = gpg.list_keys()
    print 'public key'
    pprint (pub_key)
    pri_key = gpg.list_keys(True)
    print 'private key'
    pprint(pri_key)
    
def enc_string(unencrypted_string ):
    gpg = gnupg.GPG()
    encrypted_data = gpg.encrypt(unencrypted_string, 'puneeth.shopping@gmail.com')
    encrypted_string = str(encrypted_data)
    
    print 'encrypted string'
    print 'ok: ', encrypted_data.ok
    print 'status: ', encrypted_data.status
    print 'stderr: ', encrypted_data.stderr
    print 'unencrypted_string: ', unencrypted_string
    print 'encrypted_string: ', encrypted_string
    return encrypted_string

def dec_string(encrypted_string):
    gpg = gnupg.GPG()
    encrypted_data= str(encrypted_string)
    decrypted_data = gpg.decrypt(encrypted_data, passphrase='M@ster2016')
    
    print 'decrypted string'
    print 'ok: ', decrypted_data.ok
    print 'status: ', decrypted_data.status
    print 'stderr: ', decrypted_data.stderr
    print 'decrypted string: ', decrypted_data.data

def enc_file(infile):
    gpg = gnupg.GPG()
    with open(infile, 'rb') as f:
        status = gpg.encrypt_file(f,
                                  recipients=['nixtar9991@gmail.com'],
                                  output='leo_enc.jpg',
                                  always_trust=True)
    
    print 'encrypted file'    
    print 'ok: ', status.ok
    print 'status: ', status.status
    print 'stderr: ', status.stderr
    print 'decrypted string: ', status.data
    
    return 'pub_enc.txt.gpg'

def dec_file(infile):
    gpg = gnupg.GPG()
    with open(infile, 'rb') as f:
        status = gpg.decrypt_file(f, passphrase='M@ster2016', output='Image0010.jpg')
    
    print 'decrypted file'
    print 'ok: ', status.ok
    print 'status: ', status.status
    print 'stderr: ', status.stderr
    print 'decrypted string: ', status.data
    
def sign_file(infile):
    gpg = gnupg.GPG()
    with open(infile, 'rb') as f:
        status = gpg.sign_file(f, passphrase='M@ster2016', detach=True, output=infile+'.gpg')
        
def verify_file(infile, signfile):
    gpg = gnupg.GPG()
    with open(signfile, 'rb') as f:
        status = gpg.verify_file(f, infile)
        
    if status:
        print 'verified'
    else:
        print 'unverified'
    
# exportkeys()
# importkeys(None, 'keyserver.ubuntu.com', '0x31BC35BA')
# listkeys()
# encrypted_string = enc_string('cloud computing')
# decrypted_string = dec_string(encrypted_string)
# encrypted_file = enc_file('leodec.jpg')
decrypted_file = dec_file('Image0010.jpg.enc')
# sign_file('a.jpg')
# verify_file('a.jpg', 'a.jpg.gpg')