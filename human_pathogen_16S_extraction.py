#!/usr/bin/python3

from Bio import SeqIO
import sys

sequence_dict = {}



for seq_record in SeqIO.parse(sys.argv[2], "fasta"):
    current_header = str(seq_record.id)
    current_seq = str(seq_record.seq)
    sequence_dict[current_header] = current_seq


for line in open(sys.argv[1]):
    if line[0] != '#':
        genus, species, strain, cp_num, length, g_len, accession = line.rstrip().split(',')
        flag = False
        for header in sequence_dict.keys():
            if accession in header:
                #print (accession, header)
                flag = True
        if flag == False:
            print ("Did not find", accession)




