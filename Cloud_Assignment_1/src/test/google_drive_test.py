'''
Created on Jan 30, 2015

@author: Puneeth U Bharadwaj
'''

import httplib2
import webbrowser
import pprint
import time

from apiclient import errors
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow

token_file = open('E:/workspace/CSE6331/src/project1/google_tokens.txt')
CLIENT_ID, CLIENT_SECRET = token_file.read().split('|')
token_file.close()

# Check https://developers.google.com/drive/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

# Redirect URI for installed apps
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

# Path to the file to upload
# FILENAME = 'E:/workspace/CSE6331/src/project1/document.txt'
# FILENAME = 'F:\Zips\microblog-version-0.3.zip'
# FILENAME = 'F:/bimbim.txt'
FILENAME = 'F:/Softwares/DropboxInstaller.exe'

# Run through the OAuth flow and retrieve credentials
flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE,
                           redirect_uri=REDIRECT_URI)
authorize_url = flow.step1_get_authorize_url()
print 'Go to the following link in your browser: ' + authorize_url
print webbrowser.open_new_tab(authorize_url)
code = raw_input('Enter verification code: ').strip()
credentials = flow.step2_exchange(code)

# Create an httplib2.Http object and authorize it with our credentials
http = httplib2.Http()
http = credentials.authorize(http)

drive_service = build('drive', 'v2', http=http)

# Insert a file
media_body = MediaFileUpload(FILENAME, resumable=True)
body = {
'title': FILENAME
}
   
file = drive_service.files().insert(body=body, media_body=media_body).execute()
pprint.pprint(file)

# time.sleep(10)

# print 'id:', file['id']

# drive_service.files().delete(fileId=file['id']).execute()

result = []
page_token = None
while True:
    try:
        param = {}
        if page_token:
            param['pageToken'] = page_token
        files = drive_service.files().list(q = 'trashed=False').execute()
        print files['items']
        
        result.extend(files['items'])
        page_token = files.get('nextPageToken')
        if not page_token:
            break
    except errors.HttpError, error:
        print 'An error occurred: %s' % error
        break

print 'item list'
for item in result:
    print result
    print item['id'], item['title'], item['trashed']
    if item['title'] == 'hamachi_inst.exe':
        drive_service.files().delete(fileId=item['id']).execute()
     