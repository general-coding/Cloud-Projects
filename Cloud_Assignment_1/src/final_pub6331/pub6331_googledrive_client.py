'''
Created on Feb 1, 2015

@author: Puneeth U Bharadwaj
'''

import httplib2
# import pprint
import os
import time
import gnupg

from apiclient import errors
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from rsa.bigfile import *

# from pydrive.drive import GoogleDrive

def download_file(service, drive_file):
    """Download a file's content.
    
    Args:
      service: Drive API service instance.
      drive_file: Drive File instance.
    
    Returns:
      File's content if successful, None otherwise.
    """
    download_url = drive_file.get('downloadUrl')
    if download_url:
        resp, content = service._http.request(download_url)
        if resp.status == 200:
#             print 'Status: %s' % resp
            return content
        else:
            print 'An error occurred: %s' % resp
            return None
    else:
        # The file doesn't have any content stored on Drive.
        return None

def delete_file(service, file_id):
    """Permanently delete a file, skipping the trash.
    
    Args:
      service: Drive API service instance.
      file_id: ID of the file to delete.
    """
    try:
        service.files().delete(fileId=file_id).execute()
    except errors.HttpError, error:
        print 'An error occurred: %s' % error
        
def retrieve_all_files(service):
    result = []
    page_token = None
    while True:
        try:
            param = {}
            if page_token:
                param['pageToken'] = page_token
            files = service.files().list(q = 'trashed=false').execute()
    #         print files['items']
            
            result.extend(files['items'])
            page_token = files.get('nextPageToken')
            if not page_token:
                break
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            break
    
    return result
    
# def pub6331_googledrive(path_encrypt, path_temp, path_decrypt, temp_add, temp_rem, pubkey, privkey, gauth):
def pub6331_googledrive(path_encrypt, path_temp, path_decrypt, temp_add, temp_rem, gauth, encorsign):
#     drive = GoogleDrive(gauth)
    http = httplib2.Http()
    http = gauth.authorize(http)

#     Create an httplib2.Http object and authorize it with our credentials    
    drive_service = build('drive', 'v2', http=http)
        
    if temp_add:
#         print 'Encrypting:', temp_add
#         with open(path_encrypt + temp_add, "rb") as infile, open(path_temp + temp_add, 'wb') as outfile:
#             encrypt_bigfile(infile, outfile, pubkey)
#         
#         media_body = MediaFileUpload(path_temp + temp_add, resumable=True)
#         body = {
#           'title': temp_add
#         }
#         
#         upfile = drive_service.files().insert(body=body, media_body=media_body).execute()
#         print 'Encrypted and uploaded to Google Drive:', temp_add
#         
#         infile.close()
#         outfile.close()
#         time.sleep(10)
#         
#         print 'Downloaded from Google Drive:', temp_add
#         out = open(path_temp + temp_add, 'wb')
#         out.write(download_file(drive_service, upfile))
#         out.close()
#         
#         with open(path_temp + temp_add, 'rb') as infile, open(path_decrypt + temp_add, "wb") as outfile:
#             decrypt_bigfile(infile, outfile, privkey)
#             
#         print 'Decrypted:', temp_add, '\n'
#             
#         infile.close()
#         outfile.close()

        gpg = gnupg.GPG()
        
        if encorsign == '1':
            print 'Encrypting:', temp_add
                
            with open(path_encrypt + temp_add, "rb") as f:
                status = gpg.encrypt_file(f, 
                                          recipients=['puneeth.shopping@gmail.com'],
                                          output=path_temp + temp_add)
            
            media_body = MediaFileUpload(path_temp + temp_add, resumable=True)
            body = {
              'title': temp_add
            }
            
            upfile = drive_service.files().insert(body=body, media_body=media_body).execute()
            print 'Encrypted and uploaded to Google Drive:', temp_add
            
            f.close()
            
            time.sleep(10)
            
            print 'Downloaded from Google Drive:', temp_add
            out = open(path_temp + temp_add, 'wb')
            out.write(download_file(drive_service, upfile))
            out.close()
            
            with open(path_temp + temp_add, 'rb') as f:
                status = gpg.decrypt_file(f, passphrase='5!/v\P|_y()r@ng3Wit#M@|\|GO', output=path_decrypt + temp_add)
                
            print 'Decrypted:', temp_add, '\n'
    
            f.close()
            
        if encorsign == '2':
            print 'Signing', temp_add
            
            f = open(path_encrypt + temp_add, "rb")
            signed_data = gpg.sign_file(f, output=path_temp + temp_add)
            f.close()
            
            media_body = MediaFileUpload(path_temp + temp_add, resumable=True)
            body = {
              'title': temp_add
            }
            
            upfile = drive_service.files().insert(body=body, media_body=media_body).execute()
            print 'Signed and uploaded to Google Drive:', temp_add
            
            f.close()
            
            time.sleep(10)
            
            print 'Downloaded from Google Drive:', temp_add
            out = open(path_decrypt + temp_add, 'wb')
            out.write(download_file(drive_service, upfile))
            out.close()
             
            f = open(path_decrypt + temp_add, 'rb')
            verified = gpg.verify_file(f)
            if not verified: 
#                 raise ValueError("Signature could not be verified!")
                print "Signature could not be verified!"
            
            if verified: 
                print "The Signature was verified"
            
    if temp_rem:
        result = retrieve_all_files(drive_service)
#         print 'item list'            
        for item in result:
#             print item['id'], item['title']
            if item['title'] == temp_rem:
#                 drive_service.files().delete(fileId=item['id']).execute()
#                 print 1
                delete_file(drive_service, item['id'])
#                 print 2
                print 'Removed from Google Drive:', temp_rem