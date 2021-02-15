for chr in $(seq 1 30); do
     ./plink --file bovindv02 \
           --chr $chr --cow \
           --recode \
           --exclude duplicates \
           --geno 0.5 \
           --out output/bovindv02.chr$chr --noweb;
done 

./plink --file bovindv02 \
   --chr "X" --cow  \
           --recode \
           --geno 0.5 \
           --exclude duplicates \
           --out output/bovindv02.chrX --noweb;

./plink --file bovindv02 \
           --chr "Y" --cow  \
           --recode \
           --geno 0.5 \
           --exclude duplicates \
           --out output/bovindv02.chrY --noweb;


# for chr in $(seq 27 30); do
#      ./shapeit --input-ped bovindv02.chr$chr.ped bovindv02.chr$chr.map -O output/bovindiv02.chr$chr.phased --force --thread 8
# done 

# ./plink --file bovindv02 \
#    --chr 27 \
#            --recode \
#            --geno 0.5 \
#            --exclude duplicates \
#            --out output/bovindv02.chr27 --noweb;