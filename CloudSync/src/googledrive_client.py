'''
Created on Feb 6, 2015

@author: Puneeth U Bharadwaj
'''
import gnupg, webbrowser, httplib2 
# import os

from apiclient import errors
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
import mimetypes
from Crypto.Hash import SHA512

#Set GPG_HOME. This is where the keys will be stored
GPG_HOME = 'F:/Cloud/GPG_Contents'
gpg = gnupg.GPG(gnupghome=GPG_HOME)
gpg.encoding = 'utf-8'

#Set download directory
LOCALDIR = 'F:/Cloud/GoogleDrive/'
TEMP_DIR = LOCALDIR + 'temp/'

pp1 = SHA512.new('5!/v\P|_y()r@ng3').hexdigest()
pp2 = SHA512.new('5!/v\P|_y()r@ng3Wit#M@|\|GO').hexdigest()

def getDriveService():
    CLIENT_ID = '771796077293-pbciose9vkavg8khhrht6pb7inr1339i.apps.googleusercontent.com'
    CLIENT_SECRET = 'g-PJ34Wwtxg36Bc3H0BhJqGE'
    OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'
    REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
    
    flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE,
                       redirect_uri=REDIRECT_URI)
    authorize_url = flow.step1_get_authorize_url()
#     print 'Go to the following link in your browser: ' + authorize_url
    webbrowser.open_new_tab(authorize_url)
    code = raw_input('Enter Google Drive verification code: ').strip()
    credentials = flow.step2_exchange(code)
    
    # Create an httplib2.Http object and authorize it with our credentials
    http = httplib2.Http()
    http = credentials.authorize(http)
    
    drive_service = build('drive', 'v2', http=http)
    
    return drive_service

class GoogleDrive:
    drive_service = getDriveService()
    
    def encrypt_and_signFile(self, FileName, FileUploadName):        
        FileEncSign = open(FileName, 'rb')
#         print '1'
        
        #Create key for encryption/decryption
#         input_data  = gpg.gen_key_input(key_type="RSA", key_length=2048, Passphrase='p3C@|\|Plac3')
        input_data  = gpg.gen_key_input(key_type="RSA", key_length=2048, Passphrase=pp1)
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
#         print '4'
#         f = open(TEMP_DIR + _file_upload, 'rb')
#         print f.read()
        
#         print '5'
        return TEMP_DIR + FileUploadName
    
    def verify_and_decryptFile(self, FileName):
#         FilePath = FileName.rsplit('/')
#         FilePathLen = len(FilePath)
#         FileNameDec = FilePath[FilePathLen - 1]
        FileNameDec = FileName.split('/')[-1]
        FileVerifyDec = open(FileName, 'rb')
#         decrypted_data = gpg.decrypt(FileVerifyDec.read(),passphrase='p3C@|\|Plac3',output=LOCALDIR + FileNameDec)
        decrypted_data = gpg.decrypt(FileVerifyDec.read(),passphrase=pp1,output=LOCALDIR + FileNameDec)
        FileVerifyDec.close()
    
    def uploadFileToGoogleDrive(self, FileName):        
#         os.mkdir(TEMP_DIR, 0777)
        
#         FilePath = FileName.rsplit('/')
#         FilePathLen = len(FilePath)
#         FileUploadName = FilePath[FilePathLen - 1]
        FileUploadName = FileName.split('/')[-1]
        FileEncSigned = self.encrypt_and_signFile(FileName, FileUploadName)
#         print _file_upload_enc_signed
         
#         print '6'
        mime_type = mimetypes.guess_type(FileName, strict = True)[0]
#         print 'mime_type', mime_type, FileName
        
#         media_body = MediaFileUpload(FileEncSigned, mimetype=mime_type, resumable=True)
        media_body = MediaFileUpload(FileEncSigned, resumable=True)
        body = {
          'title': FileUploadName,
          'mimeType': mime_type
        }
        
        file = self.drive_service.files().insert(body=body, media_body=media_body).execute()
        
#         os.remove(TEMP_DIR + FileUploadName)
#         os.removedirs(TEMP_DIR)
    
    def downloadFileFromGoogleDrive(self, FileName):
#         os.mkdir(TEMP_DIR, 0777)
        
        FileGoogleDrive = self.drive_service.files().list(q = 'trashed=False').execute()
        
        for FileItem in FileGoogleDrive['items']:
            FileId = FileItem['id']
            FileDrive = self.drive_service.files().get(fileId = FileId).execute()
            if FileDrive['title'] == FileName:
                download_url = FileDrive.get('downloadUrl')
                if download_url:
                    resp, content = self.drive_service._http.request(download_url)
                    if resp.status == 200:
#                         print 'Status: %s' % resp
                        
                        FileDownload = open(TEMP_DIR + FileName, 'a+')
                        FileDownload.write(content)
                        FileDownload.close()
                        
                        FileDownloadName = TEMP_DIR + FileName
                        
                        self.verify_and_decryptFile(FileDownloadName)
                    else:
#                         print 'An error occurred: %s' % resp
                        return None
        
#         os.remove(TEMP_DIR + FileName)
#         os.removedirs(TEMP_DIR)
                
    def listGoogleDriveFiles(self):
        Files_List = []
        Return_List = []
        
        page_token = None
        while True:
            try:
                param = {}
                if page_token:
                    param['pageToken'] = page_token
                files = self.drive_service.files().list(q = 'trashed=False').execute()
#                 print files['items']
                
                Files_List.extend(files['items'])
                page_token = files.get('nextPageToken')
                if not page_token:
                    break
            except errors.HttpError, error:
                print 'An error occurred: %s' % error
                break
            
        for item in Files_List:
            Return_List.append(item['title'])
            
        return Return_List