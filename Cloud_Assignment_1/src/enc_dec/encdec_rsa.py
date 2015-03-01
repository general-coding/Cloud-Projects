'''
Created on Jan 29, 2015

@author: Puneeth U Bharadwaj

Ref: http://stuvel.eu/files/python-rsa-doc/usage.html
'''

import rsa
from rsa.bigfile import *

(pubkey, privkey) = rsa.newkeys(512)
print pubkey
print privkey

message = 'hi'
 
crypto = rsa.encrypt(message, pubkey)
print '1', crypto
 
message = rsa.decrypt(crypto, privkey)
print '2', message
 
message = 'Go'
signature = rsa.sign(message, privkey, 'SHA-1')
print 'sign', signature
 
message = 'Go'
print 'verify', rsa.verify(message, signature, pubkey)
 
print 'sign a.jpg'
with open('F:/input.txt', 'rb') as msgfile:
    signature = rsa.sign(msgfile, privkey, 'SHA-1')
 
print 'signature', signature
 
print 'verify a.jpg'
with open('F:/input.txt', 'rb') as msgfile:
    print rsa.verify(msgfile, signature, pubkey)
 
print 'enc a.jpg get a.jpg.enc'
with open('F:/a.jpg', 'rb') as infile, open('F:/a.jpg.enc', 'wb') as outfile:
    encrypt_bigfile(infile, outfile, pubkey)
   
print 'dec a.jpg.enc get b.jpg'
with open('F:/a.jpg.enc', 'rb') as infile, open('F:/b.jpg', 'wb') as outfile:
    decrypt_bigfile(infile, outfile, privkey)