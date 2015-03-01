'''
Created on Feb 9, 2015

@author: Puneeth U Bharadwaj
'''

import gnupg

# gpg = gnupg.GPG()
# input_data = gpg.gen_key_input(name_email='puneeth.shopping@gmail.com')
# key = gpg.gen_key(input_data)
# print key

# ascii_armored_public_keys = gpg.export_keys('66C8F2C8')
# ascii_armored_private_keys = gpg.export_keys('66C8F2C8', True)
# with open('mykeyfile.asc', 'wb') as f:
#     f.write(ascii_armored_public_keys)
#     f.write(ascii_armored_private_keys)

# gpg = gnupg.GPG()
# pubkey1 = gpg.export_keys('puneeth.shopping@gmail.com')
# print 'pubkey'
# print pubkey1
# 
# pubkey2 = gpg.export_keys(keyids='66C8F2C8')
# print 'pubkey with id'
# print pubkey2
# 
# if pubkey1==pubkey2:
#     print True
# else:
#     print False
# 
# prikey = gpg.export_keys('puneeth.shopping@gmail.com', True)
# print prikey

gpg = gnupg.GPG()
unencrypted_string = 'Who are you? How did you get in my house?'

# encrypted_data = gpg.encrypt(unencrypted_string, 'puneeth.shopping@gmail.com')
# encrypted_string = str(encrypted_data)
# print 'ok: ', encrypted_data.ok
# print 'status: ', encrypted_data.status
# print 'stderr: ', encrypted_data.stderr
# print 'unencrypted_string: ', unencrypted_string
# print 'encrypted_string: ', encrypted_string
# 
# decrypted_data = gpg.decrypt(encrypted_string, passphrase='5!/v\P|_y()r@ng3Wit#M@|\|GO')
# print 'ok: ', decrypted_data.ok
# print 'status: ', decrypted_data.status
# print 'stderr: ', decrypted_data.stderr
# print 'decrypted string: ', decrypted_data.data

open('my-unencrypted.txt', 'w').write('You need to Google Venn diagram.')
with open('my-unencrypted.txt', 'rb') as f:
    status = gpg.encrypt_file(
        f, recipients=['puneeth.shopping@gmail.com'],
        output='my-encrypted.txt.gpg')

print 'ok: ', status.ok
print 'status: ', status.status
print 'stderr: ', status.stderr

with open('my-encrypted.txt.gpg', 'rb') as f:
    status = gpg.decrypt_file(f, passphrase='5!/v\P|_y()r@ng3Wit#M@|\|GO', output='my-decrypted.txt')

print 'ok: ', status.ok
print 'status: ', status.status
print 'stderr: ', status.stderr