'''
Created on Jan 29, 2015

@author: Puneeth U Bharadwaj

Ref: http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html
'''

import os, time

path_to_watch = "../../download"
before = dict ([(f, None) for f in os.listdir (path_to_watch)])
while 1:
    time.sleep (5)
    after = dict ([(f, None) for f in os.listdir (path_to_watch)])
    added = [f for f in after if not f in before]
    removed = [f for f in before if not f in after]
    if added:
        print "Added: ", ", ".join (added)
        
    if removed: 
        print "Removed: ", ", ".join (removed)
        
    before = after