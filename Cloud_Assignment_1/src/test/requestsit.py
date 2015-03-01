'''
Created on Jan 30, 2015

@author: Puneeth U Bharadwaj
'''

import dropbox
import time
import requests

# Get the stored key
access_token_file = open('E:/workspace/CSE6331/src/project1/access_token.txt')
access_token = access_token_file.read()
access_token_file.close()

client = dropbox.client.DropboxClient(access_token)

cursor = None
while True:
    result = client.delta(cursor)
    cursor = result['cursor']
    if result['reset']:
        print 'RESET'

    for path, metadata in result['entries']:
        print metadata
        if metadata is not None:
            print '%s : created/updated' % path
        else:
            print '%s : deleted' % path

    # if has_more is true, call delta again immediately
    if not result['has_more']:
 
        changes = False
        # poll until there are changes
        while not changes:
            response = requests.get('https://api-notify.dropbox.com/1/longpoll_delta',
                params={
                    'cursor': cursor,  # latest cursor from delta call
                    'timeout': 120  # default is 30 seconds
                })
            data = response.json()
 
            changes = data['changes']
            if not changes:
                print 'Timeout, polling again...'
 
            backoff = data.get('backoff', None)
            if backoff is not None:
                print 'Backoff requested. Sleeping for %d seconds...' % backoff
                time.sleep(backoff)
                print 'Resuming polling...'
