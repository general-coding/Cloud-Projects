'''
Created on Feb 26, 2015

@author: puneeth
'''

import csv

fname = "all_month.csv"
count = 0

result = []

first_line = True
outfile = csv.writer(open('outfile.csv', 'w'))
with open(fname, 'r') as csvfile:
    for line in csvfile.readlines():
        if first_line:
            first_line = False
            continue
        result.append(tuple(line.split(",")))
 
        for r in result:
            p = [str(x) for x in r]
            p = tuple(p)
            
            if(len(p)) == 16:        
                query = '"%s", %s, %s, %s, %s, "%s", %s, %s, %s, %s, "%s", "%s", "%s", %s%s, "%s"' % p
                
            if(len(p)) == 17:        
                query = '"%s", %s, %s, %s, %s, "%s", %s, %s, %s, %s, "%s", "%s", "%s", %s%s%s, "%s"' % p
                    
            print(query)
                
            outfile.writerow(query)
     
            count = count + 1
    
#             if count == 2:
#                 break