#!/usr/bin/python3

import sys
import numpy as np
from Bio import SeqIO

seq_file = sys.argv[1]
blast_file = sys.argv[2]
pathogen_info = "/home/genome/joseph7e/derek/new_database_build/pathogen_gca_file.txt"
group_name = sys.argv[3]
fecal_pathogens = "/home/genome/joseph7e/derek/enteric_specific_pathogens.csv"
#output = open(sys.argv[4],'w')


list_of_pathogens = [] #pathogen1,pathogen2,etc
list_of_fecal_pathogens = []

for line in open(fecal_pathogens):
    line = line.rstrip()
    list_of_fecal_pathogens.append(line)


for line in open("/home/genome/joseph7e/derek/new_database_build/all_pathogens_in_database.txt"):
    line = line.rstrip()
    list_of_pathogens.append(line)

total_sequences = 0
per_sample_sequence_dict = {} # sample:[number_of_seqs,number_of_pathogens,[all_pathogens],[fecal_ones])


for line in open(seq_file):
    if line.startswith('>'):
        total_sequences += 1
        line = line.replace('>','')
        sample = line.split('_')[0]
        if sample in per_sample_sequence_dict.keys():
            per_sample_sequence_dict[sample][0] += 1
        else:
            starting_p_list = []
            starting_f_list = []
            for p in list_of_pathogens:
                starting_p_list.append(0)
            for f in list_of_fecal_pathogens:
                starting_f_list.append(0)
            per_sample_sequence_dict[sample] = [1,0,0,starting_p_list, starting_f_list]

pathogen_dict = {}
for line in open(pathogen_info):
    pathogen, GCA = line.rstrip().split(',')
    GCF = GCA.replace('GCA', 'GCF')
    pathogen_dict[GCF] =  pathogen
    #list_of_pathogens.append(pathogen)

#print (list_of_pathogens)

#output.writelines('#Sample,Pathogen_name,length_of_hit,percent_id,evalue')


best_hit_dictionary = {}

for line in open(blast_file):
    elements = line.rstrip().split('\t')
    query = elements[0]
    subject = elements[2]
    percent_id = elements[3]
    length_hit = elements[4]
    evalue = elements[9]
    if float(percent_id) >= 99.00 and int(length_hit) > 200:# and float(evalue) < float('1e-20'):
        if query in best_hit_dictionary.keys():
            continue
        else:
            #print (line)
            best_hit_dictionary[query] = [subject, percent_id, length_hit, evalue]

final_pathogen_dict = {}# pathogen:[number_of_seqs,[p_id1,p_id2]

total_pathogen_count = 0

final_sample_pathogen_dict = {}

for key in sorted(best_hit_dictionary.keys()):
    info = best_hit_dictionary[key]
    sample = key.split('_')[0]
    for gcf in pathogen_dict.keys():
        if gcf in info[0]:
            per_sample_sequence_dict[sample][1] += 1
            pathogen = pathogen_dict[gcf]

            #### Track which pathogen it is and add it to samoe dict
            p_count = 0
            for ppp in list_of_pathogens:
                if pathogen == ppp:
                    p_index = p_count
                    #print (per_sample_sequence_dict[sample])
                    per_sample_sequence_dict[sample][3][p_index] += 1
                p_count += 1



            f_count = 0
            for fff in list_of_fecal_pathogens:
                if fff in pathogen:
                    f_index = f_count
                    per_sample_sequence_dict[sample][2] += 1
                    per_sample_sequence_dict[sample][4][f_index] += 1
                f_count += 1





            total_pathogen_count += 1
            p_ident = float(info[1])
            #print (key, pathogen_dict[gcf], info[1], info[2], info[3] )
            if pathogen in final_pathogen_dict.keys():
                final_pathogen_dict[pathogen][0] += 1
                final_pathogen_dict[pathogen][1].append(p_ident)
            else:
                final_pathogen_dict[pathogen] = [1, [p_ident]]



print ('#Group,Pathogen,raw_pathogen_count,total_pathogen_count,total_num_input_seqs,percent_of_pathogens,percent_of_total,mean_p_id')
for p_name,value in final_pathogen_dict.items():
    percent_of_total = str(100*(value[0]/(float(total_sequences))))
    percent_of_pathogen = str(100*(value[0]/(float(total_pathogen_count))))
    print ('#'+group_name + ','+p_name+ ',' + str(value[0]) + ',' + str(total_pathogen_count) +',' +  str(total_sequences) + ',' + percent_of_pathogen + ',' + percent_of_total + ','+str(np.mean(value[1])))


#"Clostridium,Shigella,Salmonella,Escherichia,Campylobacter,Pseduomonas,Helicobacter,Citrobacter,Enterobacter,Klebisella"

print('Sample,num_raw_seqs,num_of_pathogens,num_of_fecal_pathogens,' + ','.join(list_of_pathogens) +',' + ','.join(list_of_fecal_pathogens))
for sample, i in per_sample_sequence_dict.items():
    str_list_p = [str(x) for x in i[3]]
    str_list_f = [str(x) for x in i[4]]
    #print (str_list_p)
    #print (str_list_f)
    print (sample + ',' + str(i[0]) + ','+ str(i[1]) + ',' + str(i[2]) + ',' + ','.join(str_list_p) + ',' + ','.join(str_list_f))





