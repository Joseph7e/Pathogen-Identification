#!/usr/bin/python3

import sys
acc_list = []
for line in open(sys.argv[1]):
    acc_list.append(line.rstrip())

for line in open(sys.argv[2]):
    elements = line.rstrip().split(',')
    for acc in acc_list:
        if acc in line:
            # numbers = elements[7].split('_')[1]
            # first = numbers[:3]
            # second = numbers[3:6]
            # third = numbers[6:9]
            # print (line)
            ftp = elements[-2]
            #print (acc, elements[7], ftp)
            print ('wget ' + ftp + '/*.gff*')
