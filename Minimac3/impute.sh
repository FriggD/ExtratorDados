#!/bin/sh

REF="bovindv02"
INPUTE="bovindv01"
PREFIX="Inputação"


for chr in $(seq 23 30); do
    ./Minimac3 --refHaps $REF/phased/vcf/$REF.chr$chr.phased.vcf \
        --haps $INPUTE/phased/vcf/$INPUTE.chr$chr.phased.vcf \
        --prefix Inputed/chr${chr} \
        --MyChromosome $chr
done 

# chr="X"
# ./Minimac3 --refHaps $REF/phased/vcf/$REF.chr$chr.phased.vcf \
#     --haps $INPUTE/phased/vcf/$INPUTE.chr$chr.phased.vcf \
#     --prefix Inputed/chr${chr}

# chr="Y"
# ./Minimac3 --refHaps $REF/phased/vcf/$REF.chr$chr.phased.vcf \
#     --haps $INPUTE/phased/vcf/$INPUTE.chr$chr.phased.vcf \
#     --prefix Inputed/chr${chr}