#!/usr/bin/python3

import sys, os

ncbi_table = sys.argv[2]
name_file = sys.argv[1]


name_list = []
for line in open(name_file):
    name_list.append(line.rstrip())

#print (name_list)
for line in open(sys.argv[2]):
    elements = line.rstrip().split(',')
    #print (elements)
    #print (len(name_list))
    for name in name_list:
        if name in line:# and 'ftp' in line:
            ftp = elements[-2]
            #print (acc, elements[7], ftp)
            #print ('#NAME = :', name)
            #print (line)
            #os.system('wget ' + ftp + '/*.fna*')
            #name_list.remove(name)
            print (name.replace(' ','_')+','+elements[7].rstrip())

#print ('DONE: representative 16S sequences missing for:', name_list, len(name_list))
# for name in name_list:
#     print (name)