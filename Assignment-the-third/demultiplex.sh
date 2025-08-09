#!/bin/bash
#SBATCH --account=bgmp                    #REQUIRED: which account to use
#SBATCH --partition=bgmp                  #REQUIRED: which partition to use
#SBATCH --cpus-per-task=1                 #optional: number of cpus, default is 1
#SBATCH --mem=8GB                         #optional: amount of memory, default is 4GB per cpu
#SBATCH --mail-user=sbergan@uoregon.edu   #optional: if you'd like email
#SBATCH --mail-type=ALL                   #optional: must set email first, what type of email you want
#SBATCH --job-name=demultiplex                   #optional: job name
#SBATCH --output=demultiplex_%j.out              #optional: file to store stdout from job, %j adds the assigned jobID
#SBATCH --error=demultiplex_%j.err               #optional: file to store stderr from job, %j adds the assigned jobID

mamba activate demultiplex

/usr/bin/time -v /projects/bgmp/sbergan/bioinfo/Bi622/Demultiplex/Assignment-the-third/demultiplex.py \
    -i /projects/bgmp/shared/2017_sequencing/indexes.txt \
    -r1 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz \
    -r2 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz \
    -r3 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz \
    -r4 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz \
    -o /projects/bgmp/sbergan/bioinfo/Bi622/Demultiplex/Assignment-the-third/final_output

