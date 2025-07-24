#!/usr/bin/env python

import gzip
import os
from matplotlib import pyplot as plt
import bioinfo
from tqdm import tqdm


# for testing
fq_paths_lengths = [
    ('test_R1.fq.gz', 12),
    ('test_R2.fq.gz', 12),
    ('test_R3.fq.gz', 12),
    ('test_R4.fq.gz', 12)
]

# # for real data
# data = ''


def main():
    for read_num, (file, length) in enumerate(fq_paths_lengths):

        # progress bar initialization
        milestone = length // 10
        print(f'Reading {file}')
        with gzip.open(file,'rt') as f:
            for i, line in tqdm(enumerate(f)):
                # print(f.read())
                # print(type(line))
                if i % 4 == 3:
                    line = line.strip()
                    # print(line)
                    # print(line)
                    # initialize the list
                    if i == 3:
                        num_chars = len(line)
                        means = [0.0 for i in range(num_chars)]
                    for j, char in enumerate(line):
                        # print(f'j: {j}')
                        # print(f'char: {char}')
                        means[j] += bioinfo.convert_phred(char)/12
        # plot the thing here
        plt.bar(range(0,num_chars), means)
        plt.title("Mean Quality Score by Base Pair Index")
        plt.xlabel("# Base Pair")
        plt.ylabel("Mean Quality Score")
        plt.savefig(f'R{read_num}.png')
        plt.cla()
        

main()