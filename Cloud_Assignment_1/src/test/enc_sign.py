'''
Created on Feb 2, 2015

@author: Puneeth U Bharadwaj
'''

import gnupg
from Crypto.Hash import SHA512

#Set where the GPG should store the keys
GPG_HOME = 'F:/Cloud/GPG_Contents'
gpg = gnupg.GPG(gnupghome=GPG_HOME)
gpg.encoding = 'utf-8'

hex1 = SHA512.new('puneeth').hexdigest()
print hex1

hex2 = SHA512.new('bharadwaj').hexdigest()
print hex2

#Key management
# key_input_data = gpg.gen_key_input(key_type="RSA", key_length=128, passphrase='b@b\/Do||')
key_input_data = gpg.gen_key_input(key_type="RSA", key_length=128, passphrase=hex1)
key = gpg.gen_key(key_input_data)
# subkey_input_data = gpg.gen_key_input(key_type="RSA", key_length=128, passphrase='Do||b@b\/')
subkey_input_data = gpg.gen_key_input(key_type="RSA", key_length=128, passphrase=hex2)
subkey = gpg.gen_key(subkey_input_data)


infile = open('../../plain.txt', 'rb')
print key.fingerprint
print subkey.fingerprint
# encrypted_ascii_data = gpg.encrypt(infile.read(),recipients=key.fingerprint,sign=subkey.fingerprint,passphrase="Do||b@b\/", output='../../plain.txt.enc')
encrypted_ascii_data = gpg.encrypt(infile.read(),recipients=key.fingerprint,sign=subkey.fingerprint,passphrase=hex2, output='../../plain.txt.enc')
print encrypted_ascii_data.status

infile = open('../../plain.txt.enc', 'rb')
# decrypted_ascii_data = gpg.decrypt(infile.read(), passphrase='b@b\/Do||', output='../../plain.txt.dec')
decrypted_ascii_data = gpg.decrypt(infile.read(), passphrase=hex1, output='../../plain.txt.dec')

if decrypted_ascii_data.trust_level is not None and decrypted_ascii_data.trust_level>=decrypted_ascii_data.TRUST_FULLY:
    print decrypted_ascii_data.trust_text