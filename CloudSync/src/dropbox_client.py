'''
Created on Feb 5, 2015

@author: Puneeth U Bharadwaj
'''
import dropbox, gnupg, os
from Crypto.Hash import SHA512

#Use the Dropbox access token to connect to dropbox
client = dropbox.client.DropboxClient('S2etaYtslbAAAAAAAAAAOYGW4TnqkXbgUK-bGP9-C_9Qf_5EjGiF9jwf4Lu9_YYF')

#Set GPG_HOME. This is where the keys will be stored
GPG_HOME = 'F:/Cloud/GPG_Contents'
gpg = gnupg.GPG(gnupghome=GPG_HOME)
gpg.encoding = 'utf-8'

#Set download directory
LOCALDIR = 'F:/Cloud/Dropbox/'
TEMP_DIR = LOCALDIR + 'temp/'

pp1 = SHA512.new('5!/v\P|_y()r@ng3').hexdigest()
pp2 = SHA512.new('5!/v\P|_y()r@ng3Wit#M@|\|GO').hexdigest()

class DropBox:
    #Method: uploadFileToDropbox
    
    #FileName contains the fully qualified path of the selected file
    #FileUploadName contains the name that will be used when encrypting the file.
    #The Files names are maintained as-is for user understandability
    #Sign and encrypt with private key
    def encrypt_and_signFile(self, FileName, FileUploadName):
        FileEncSign = open(FileName, 'rb')
#         print '1'
        
        #Create key for encryption/decryption
#         input_data  = gpg.gen_key_input(key_type="RSA", key_length=2048, Passphrase='p3C@|\|Plac3')
        input_data  = gpg.gen_key_input(key_type="RSA", key_length=2048)
#                                         , Passphrase=pp1)
        _key_enc_dec = gpg.gen_key(input_data)
#         print '2'
        
        #Create key for digital signature
#         input_data  = gpg.gen_key_input(key_type="RSA", key_length=2048, Passphrase='@part/V\3nT3o8')
        input_data  = gpg.gen_key_input(key_type="RSA", key_length=2048, Passphrase=pp2)
        _key_sign = gpg.gen_key(input_data)
#         print '3'

        encrypted_signed_data = gpg.encrypt(FileEncSign.read(),
                                            recipients=_key_enc_dec.fingerprint,
                                            sign=_key_sign.fingerprint,
#                                             passphrase="@part/V\3nT3o8", 
                                            passphrase=pp2, 
                                            output=(TEMP_DIR + FileUploadName))
#         encrypted_signed_data = gpg.encrypt_file(FileEncSign, 
#                                                  recipients=_key_enc_dec.fingerprint,
#                                                  output=(TEMP_DIR + FileUploadName))
        
        print 'enc', encrypted_signed_data.ok
#         print '4'
#         f = open(TEMP_DIR + _file_upload, 'rb')
#         print f.read()
        
#         print '5'
        return TEMP_DIR + FileUploadName
    
    #Decrypt download data with public key and passphrase
    def verify_and_decryptFile(self, FileName):
#         FilePath = FileName.rsplit('/')
#         FilePathLen = len(FilePath)
#         FileNameDec = FilePath[FilePathLen - 1]
        FileNameDec = FileName.split('/')[-1]
        FileVerifyDec = open(FileName, 'rb')
#         decrypted_data = gpg.decrypt(FileVerifyDec.read(),passphrase='p3C@|\|Plac3',output=LOCALDIR + FileNameDec)
        decrypted_data = gpg.decrypt(FileVerifyDec.read(),passphrase=pp1,output=LOCALDIR + FileNameDec)
        
#         print decrypted_data.trust_level
        
        FileVerifyDec.close()
    
    #Upload the selected file to Dropbox after encryption and signing
    def uploadFileToDropbox(self, FileName):
#         os.mkdir(TEMP_DIR, 0777)
        
#         FilePath = FileName.rsplit('/')
#         FilePathLen = len(FilePath)
#         FileUploadName = FilePath[FilePathLen - 1]
        FileUploadName = FileName.split('/')[-1]
        FileEncSigned = self.encrypt_and_signFile(FileName, FileUploadName)
#         print _file_upload_enc_signed
        FileUpload = open(FileEncSigned, 'rb')
        
#         print '6'
        response = client.put_file(FileUploadName, FileUpload)
        FileUpload.close()
        
        os.remove(TEMP_DIR + FileUploadName)
#         os.removedirs(TEMP_DIR)
    
    #Download, verify and decrypt the selected file, from Dropbox    
    def downloadFileFromDropbox(self, FileName):
#         os.mkdir(TEMP_DIR, 0777)
        
        FileDownload = client.get_file(FileName)
        FileSignedDec = open(TEMP_DIR + FileName, 'wb')
        FileSignedDec.write(FileDownload.read())
        FileSignedDec.close()
        
        FileDownloadName = TEMP_DIR + FileName
        
        self.verify_and_decryptFile(FileDownloadName)
        
        os.remove(TEMP_DIR + FileName)
#         os.removedirs(TEMP_DIR)
    
    #Get a list of all the files uploaded into the Dropbox.
    #Allows user to choose the file to be downloaded    
    def listDropboxFiles(self):
        #Get folder metadata from Drobox
        Folder_Metadata = client.metadata('/')
        File_List = []
        
        #Get all files and discard directories
        for Files in Folder_Metadata['contents']:
            if Files['is_dir'] is False:
                File_List.append(Files['path'])
        
#         print _list_file
        
        return File_List