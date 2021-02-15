#!/bin/sh


CHIP_NAME="bovindv02"

# Executando o python createGenFile
# echo "Executando o python createGenFile"
# python3 createGenFile_Minimac.py --map bovindv01old.map --ped pedigree.csv --genotype-folder ./genoma

# echo "Concatenando arquivos genotypes_"
# cat genotypes_* > bovindv01.ped

# echo "copiando arquivo: cp ./$CHIP_NAME.ped ../plink/$CHIP_NAME/raw/$CHIP_NAME.ped"
# cp ./bovindv01.ped ../plink/$CHIP_NAME/raw/$CHIP_NAME.ped

echo "../Minimac/$CHIP_NAME/"
cd ../Minimac/$CHIP_NAME/


# Cromossomos 1-30
# for chr in $(seq 1 30); do
    # echo "Plink"
    # ./plink --file raw/$CHIP_NAME \
    #     --chr $chr --cow \
    #     --recode \
    #     --geno 0.5 \
    #     --out unphased/$CHIP_NAME.chr$chr --noweb;

    # echo "ShapeIt"
    # ./shapeit \
    #     --input-ped unphased/$CHIP_NAME.chr$chr.ped unphased/$CHIP_NAME.chr$chr.map \
    #     -O phased/$CHIP_NAME.chr$chr.phased \
    #     --force \
    #     --duohmm \
    #     --thread 9;

    # ./shapeit -convert --input-haps phased/$CHIP_NAME.chr$chr.phased --output-vcf phased/vcf/$CHIP_NAME.chr$chr.phased.vcf
# done 

# Cromossomo X
# ./plink --file raw/$CHIP_NAME \
#     --chr "X" --cow \
#     --recode \
#     --geno 0.5 \
#     --out unphased/$CHIP_NAME.chrX --noweb;

# ./shapeit \
#     --input-ped unphased/$CHIP_NAME.chrX.ped unphased/$CHIP_NAME.chrX.map \
#     -O phased/$CHIP_NAME.chrX.phased \
#     --force \
#     --duohmm \
#     --thread 9;

# ./shapeit -convert --input-haps phased/$CHIP_NAME.chrX.phased --output-vcf phased/vcf/$CHIP_NAME.chrX.phased.vcf


Cromossomo Y
./plink --file raw/$CHIP_NAME \
    --chr "Y" --cow \
    --recode \
    --geno 0.5 \
    --out unphased/$CHIP_NAME.chrY --noweb;

./shapeit \
    --input-ped unphased/$CHIP_NAME.chrY.ped unphased/$CHIP_NAME.chrY.map \
    -O phased/$CHIP_NAME.chrY.phased \
    --force \
    --duohmm \
    --thread 9;

./shapeit -convert --input-haps phased/$CHIP_NAME.chrY.phased --output-vcf phased/vcf/$CHIP_NAME.chrY.phased.vcf


# Desliga o computador
# shutdown -h 1