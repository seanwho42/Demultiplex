#!/usr/bin/env python

import gzip
import os
from matplotlib import pyplot as plt
import bioinfo


# # for testing
# fq_paths_lengths = [
#     ('test_R1.fq.gz', 12),
#     ('test_R2.fq.gz', 12),
#     ('test_R3.fq.gz', 12),
#     ('test_R4.fq.gz', 12)
# ]

# for real data
# list of tuples with (path, number of reads)
fq_paths_n_reads = [
    ('/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz', 363246735),
    ('/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz', 363246735),
    ('/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz', 363246735),
    ('/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz', 363246735)
]


def main():
    for read_num, (file, n_reads) in enumerate(fq_paths_n_reads):

        # progress bar initialization
        print(f'Reading {file}')
        with gzip.open(file,'rt') as f:
            for i, line in enumerate(f):
                if i % 4 == 3:
                    line = line.strip()
                    # initialize the list
                    if i == 3:
                        num_chars = len(line)
                        means = [0.0 for i in range(num_chars)]
                    # add to sum
                    for j, char in enumerate(line):
                        means[j] += bioinfo.convert_phred(char)/n_reads
        # plot the thing here
        plt.bar(range(0,num_chars), means)
        plt.title(f'Mean Quality Score by Base Pair Index (read {read_num + 1})')
        plt.xlabel("# Base Pair")
        plt.ylabel("Mean Quality Score")
        plt.savefig(f'read{read_num+1}.png')
        plt.cla()
        

main()