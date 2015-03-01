'''
Created on Jan 28, 2015

@author: Puneeth U Bharadwaj
'''

import os, time
 
# Include the Dropbox SDK libraries
from dropbox import client, rest, session
 
# going to store the access info in this file
TOKENS = 'E:/workspace/CSE6331/dropbox_token.txt'
 
# Get your app key and secret from the Dropbox developer website
APP_KEY = 'kocqylpzj1nohtb'
APP_SECRET = 'dq2ydvrfl26f2z9'
ACCESS_TYPE = 'app_folder'
 
sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
 
request_token = sess.obtain_request_token()
 
url = sess.build_authorize_url(request_token)
 
# Make the user sign in and authorize this token
print "url:", url
print "Please visit this website and press the 'Allow' button, then hit 'Enter' here."
 
raw_input()
 
# This will fail if the user didn't visit the above URL and hit 'Allow'
access_token = sess.obtain_access_token(request_token)
 
# save the key to the file so you don't need to do this again
token_file = open(TOKENS, 'w')
 
token_file.write("%s|%s" % (access_token.key, access_token.secret))
 
token_file.close()
