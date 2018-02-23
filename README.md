# Potential-Pathogen-Identification


### Construct database of potential human pathogens
Species names of potential pathogens were dentified from X paper.
538_potential_pathogenic_bacteria.csv - contains the complete list of potential pathogens.
https://github.com/Joseph7e/Pathogen-Identification/blob/master/538_potential_pathogenic_bacteria.csv


### Identify species with avaialble data in refseq.
Species with avaialble genomic sequences were identified from NCBIs ftp report file.
pathogen_gca_file.txt - a complete list of all potential pathogen genome accessions available
download_stuff_V2.sh - used to download all gff and fna files for each species


### extract 16S sequences
The all 16S copies from each species genome was than extracted and concatenated into a single FASTA database 
gene_extractor.py - used to extract a given gene from a genomic fasta, given a gff and gene name (in this case 16S rRNA).

all_pathogens_in_database.txt - list of pahtogen species in final database
missing_species.txt - list of potential pathogens that are not in final database


### Sequence BLAST
Query sequences are BLASTed against the final database using the following command.
makeblastdb -in new_database_436_species.fasta -out new_database_436_species -dbtype nt
blastn -query <sequence.fasta> -subject new_database_436_species -outfmt 6 -out <outname>


### Parse BLAST and construct csv of results.
parse_blast_for_pathogens.py - the main script for blast parsing and pathogen identification.
This above script takes three command line arguments. 
1.) Sequence file - input FASTA used for BLAST
2.) BLAST results
3.) group name (i.e. ward 1, ward 2, etc)
Hardcoded are paths to the pathogen_gca_file.txt and enteric_specific_pathogens.csv files above.
The script is stingent on assigning amplicon sequences to potential pathogens, requiring >99% identity, hit length greater than 200 bps, and an e-value less than 1e-20.
