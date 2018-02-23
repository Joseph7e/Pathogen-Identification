cat accessions.txt | while read line
do
   fna_link=""
   gff_link=""
   acc=$line

   web="https://www.ncbi.nlm.nih.gov/genome/?term="$acc
   gff_link="$(wget -q -O- $web | grep -o -P ".faa.gz.*?ftp.*?gff.gz" | grep -o -P "ftp.*?gff.gz")"

   cd gffs
   #wget $gff_link
   fna_link="$(wget -q -O- $web | grep gff | grep -o -P "ftp.*fna.gz")"
   cd ../genomes
   #wget $fna_link
   cd ../
   echo $acc $gff_link $fna_link

done
