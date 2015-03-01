'''
Created on Feb 1, 2015

@author: Puneeth U Bharadwaj
'''

import dropbox
import webbrowser

from oauth2client.client import OAuth2WebServerFlow
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive

def pub6331_dropbox_auth():
    # Get the stored key
    access_token_file = open('access_token.txt')
    access_token = access_token_file.read()
    access_token_file.close()
    
    #Connect to dropbox using Generated Access Token. Go to the appconsole to get generate this token
    client = dropbox.client.DropboxClient(access_token)
    
    return client

def pub6331_googledrive_auth():
#     gauth = GoogleAuth()
#     gauth.LocalWebserverAuth()
#     
#     return gauth
    token_file = open('E:/workspace/CSE6331/src/project1/google_tokens.txt')
    CLIENT_ID, CLIENT_SECRET = token_file.read().split('|')
    token_file.close()
    
    # Check https://developers.google.com/drive/scopes for all available scopes
    OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'
    
    # Redirect URI for installed apps
    REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
    
    # Run through the OAuth flow and retrieve credentials
    flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, redirect_uri=REDIRECT_URI)
    authorize_url = flow.step1_get_authorize_url()
#     print 'Go to the following link in your browser: ' + authorize_url
    webbrowser.open_new_tab(authorize_url)
    code = raw_input('Enter verification code: ').strip()
    credentials = flow.step2_exchange(code)
    
    return credentials