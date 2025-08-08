#!/usr/bin/env python

# checking hamming distance for the indices

from matplotlib import pyplot as plt

path = '/projects/bgmp/shared/2017_sequencing/indexes.txt'

indices = []

with open(path, 'r') as f:
    for i, line in enumerate(f):
        if i != 0:
            line = line.strip()
            # get the entries in the row
            row = line.split()
            sequence = row[4]
            indices.append(sequence)
            # print(sequence)

index_pairs = {}

for i1 in indices:
    for i2 in indices:
        # we don't want it to compare against itself later
        if i1 != i2:
            # let's not have duplicate pairs either for this, since we are just checking hamming distance all combinations, not caring about order
            if (i2, i1) not in index_pairs:
                index_pairs[(i1,i2)] = 0

# print(index_pairs)
# print(len(index_pairs))

# check how many of the bases are different for each index
for pair in index_pairs:
    i1 = pair[0]
    i2 = pair[1]
    for n, base in enumerate(i1):
        # is index 1's base equal to index 2's base in this position
        if base != i2[n]:
            index_pairs[pair] += 1

# print(index_pairs)
# print(len(index_pairs))

# print(index_pairs.values())
# hist was plotting weirdly so making our own frequency counts so we can use bar..
hamm_dist_frequencies = {}
for n in index_pairs.values():
    if n in hamm_dist_frequencies:
        hamm_dist_frequencies[n] += 1
    else:
        hamm_dist_frequencies[n] = 1

distances = []
counts = []
for i, distance in enumerate(hamm_dist_frequencies):
    distances.append(distance)
    counts.append(hamm_dist_frequencies[distance])

plt.bar(distances, counts, align='center')
plt.ylabel('Count')
plt.xlim((2,9))
plt.xlabel('Hamming distance for index pair')
plt.title('Hamming distances of index combinations')
plt.savefig('Assignment-the-first/hamming_hist.png')
