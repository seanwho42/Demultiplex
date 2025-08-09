#!/usr/bin/env python
import os
import gzip
import argparse


# Assignment-the-third/demultiplex.py -i test_indexes.txt -r1 TEST-input_FASTQ/test_R1.fq.gz -r2 TEST-input_FASTQ/test_R2.fq.gz -r3 TEST-input_FASTQ/test_R3.fq.gz -r4 TEST-input_FASTQ/test_R4.fq.gz -o test_output

def get_args():
    parser = argparse.ArgumentParser(description="")
    # TODO: include the file formatting info for the index file
    parser.add_argument("-i", "--indices", help="Index file containing all indices (mention something)", required = True)
    parser.add_argument("-r1", "--read1", help="Input fastq file for read 1", required=True)
    parser.add_argument("-r2", "--read2", help="Input fastq file for read 2", required=True)
    parser.add_argument("-r3", "--read3", help="Input fastq file for read 3", required=True)
    parser.add_argument("-r4", "--read4", help="Input fastq file for read 4", required=True)
    parser.add_argument("-o", "--out", help="output directory path", required=True)
    return parser.parse_args()

args = get_args()

# make sure that the output directory is standardized to not have the slash at the end
if args.out[-1] == '/':
    args.out = args.out[:-1]

compliments = {
    'A' : 'T',
    'T' : 'A',
    'C' : 'G',
    'G' : 'C',
    'N' : 'N'
}

def main():
    # TODO: say what types of fastq files in the docstring
    '''
    Main function to read the fastq files and demultiplex them, creating new fastq files
    '''

    hopped_pairs, matched_pairs = get_index_pairs()
    unknown_pairs_count = 0

    outfile_dict = open_outfiles(matched_pairs)

    with gzip.open(args.read1, 'rt') as r1, gzip.open(args.read2, 'rt') as r2, gzip.open(args.read3, 'rt') as r3, gzip.open(args.read4, 'rt') as r4:
        # while loop to read through all of the read files
        while True:
            r1_lines, r2_lines, r3_lines, r4_lines = get_reads(r1, r2, r3, r4)

            # check indices to see if they are part of mismatches:
            index_pair = (r2_lines[1], r3_lines[1])
            if index_pair in matched_pairs:
                # write to matched pair files
                matched_pairs[index_pair]['count'] += 1
                # faster to get INDEX-INDEX string this way than to generate it every time
                index_string = matched_pairs[index_pair]['index_string']

                write_read(read = r1_lines, index_string = index_string, outfile = outfile_dict[f'{index_string}_R1'])
                write_read(read = r4_lines, index_string = index_string, outfile = outfile_dict[f'{index_string}_R2'])


            elif index_pair in hopped_pairs:
                # write to hopped pair files
                hopped_pairs[index_pair]['count'] += 1
                # faster to get INDEX-INDEX string this way than to generate it every time
                index_string = hopped_pairs[index_pair]['index_string']

                write_read(read = r1_lines, index_string = index_string, outfile = outfile_dict['hopped_R1'])
                write_read(read = r4_lines, index_string = index_string, outfile = outfile_dict['hopped_R2'])

            else:
                # breaks loop if there is nothing being read
                if not r1_lines[0]:
                    close_outfiles(outfile_dict)
                    break

                # write to unknown index files
                unknown_pairs_count += 1
                index_string = f'{index_pair[0]}-{reverse_compliment(index_pair[1])}'

                write_read(read = r1_lines, index_string = index_string, outfile = outfile_dict['unknown_R1'])
                write_read(read = r4_lines, index_string = index_string, outfile = outfile_dict['unknown_R2'])

    # generate summary info files
    write_summary(matched_pairs, hopped_pairs, unknown_pairs_count)


            


def open_outfiles(matched_pairs):
    # TODO: write docstring
    # make sure the needed directories exist
    os.makedirs(f'{args.out}/matched', exist_ok = True)
    os.makedirs(f'{args.out}/summary', exist_ok = True)
    
    outfile_dict = {}
    # R1 is forward, R2 is reverse
    for direction in ('R1', 'R2'):
        for pair_dict in matched_pairs.values():
            matched_index_name = pair_dict['index_string']
            # open file object as value in dictionary
            outfile_dict[f'{matched_index_name}_{direction}'] = open(f'{args.out}/matched/{matched_index_name}_{direction}.fq', 'w')
        outfile_dict[f'hopped_{direction}'] = open(f'{args.out}/hopped_{direction}.fq', 'w')
        outfile_dict[f'unknown_{direction}'] = open(f'{args.out}/unknown_{direction}.fq', 'w')
    # print('OUTFILE DICT:')
    # print(outfile_dict)
    return outfile_dict

def close_outfiles(outfile_dict):
    '''
    Closes each output file that was created
    '''
    for file_object in outfile_dict.values():
        file_object.close()


def get_reads(r1, r2, r3, r4):
    '''
    Takes files as a tuple and returns a tuple of four lists (one list for each input file) with four lines each (a read)
    '''
    # TODO: probably a more efficient way to handle reading these
    r1_lines = []
    r2_lines = []
    r3_lines = []
    r4_lines = []
    for i in range(0,4):
        r1_lines.append(r1.readline())
        # strip the index reads only
        r2_lines.append(r2.readline().strip())
        r3_lines.append(r3.readline().strip())
        r4_lines.append(r4.readline())
    return r1_lines, r2_lines, r3_lines, r4_lines

def get_index_pairs():
    # TODO: add docstring
    '''
    Returns two dictionaries, matched_pairs and hopped_pairs.
    {(index, rc_index) : {index_string, count}}
    '''
    indices = []

    with open(args.indices, 'r') as f:
        for i, line in enumerate(f):
            if i != 0:
                line = line.strip()
                # get the entries in the row
                row = line.split()
                sequence = row[4]
                indices.append(sequence)
                # print(sequence)

        matched_pairs = {}
        hopped_pairs = {}

        for i1 in indices:
            for i2 in indices:
                # check if we've already created it
                if not ((i1, reverse_compliment(i2)) in matched_pairs or (i1, reverse_compliment(i2)) in hopped_pairs):
                    index_string = f'{i1}-{i2}'
                    index_pair_dict = {'index_string': index_string, 'count':0}
                    # if the indices are correctly matched, write to matched_pairs, otherwise write to hopped_pairs
                    if i1 == i2:
                        matched_pairs[(i1, reverse_compliment(i2))] = index_pair_dict
                    else:
                        hopped_pairs[(i1, reverse_compliment(i2))] = index_pair_dict
    # print('MATCHED PAIRS:')
    # print(matched_pairs)

    return hopped_pairs, matched_pairs

def reverse_compliment(seq):
    # TODO: make a docstring here
    '''
    returns reverse compliment
    '''
    rc = ''
    for base in seq.upper()[::-1]:
        rc += compliments[base]
    return rc

def write_read(read, index_string, outfile):
    '''
    Write reads to outfile given:
     read: a list of lines from the read we need to modify
     index_string: string showing the two indices in 'INDEX-INDEX' format to be added to the header
     outfile: an outfile object
    '''
    outfile.write(f'{read[0].strip()} {index_string}\n')
    for n in range(1,4):
        outfile.write(read[n])


def write_summary(matched_pairs, hopped_pairs, unknown_pairs_count):
    # TODO: write a docstring here
    '''
    
    '''
    # print(matched_pairs.items())
    matched_read_count = 0
    hopped_read_count = 0
    for values_dict in matched_pairs.values():
        matched_read_count += values_dict['count']
    
    for values_dict in hopped_pairs.values():
        hopped_read_count += values_dict['count']
    
    sorted_matched = sorted(matched_pairs.items(), key = lambda item: item[1]['count'], reverse = True)
    sorted_hopped = sorted(hopped_pairs.items(), key = lambda item: item[1]['count'], reverse = True)

    total_read_count = matched_read_count + hopped_read_count + unknown_pairs_count

    with open(f'{args.out}/summary/hopped.tsv', 'w') as hopped_tsv, \
        open(f'{args.out}/summary/matched.tsv', 'w') as matched_tsv, \
        open(f'{args.out}/summary/overview.txt', 'w') as overview:

        matched_tsv.write('index_pair\tnum_matches\tpercentage_of_matched_reads\tpercentage_of_total_reads\n')
        for key, values_dict in sorted_matched:
            matched_tsv.write(f'{values_dict['index_string']}\t{values_dict['count']}\t{100*(values_dict['count']/matched_read_count)}\t{100*(values_dict['count']/total_read_count)}\n')
        
        hopped_tsv.write('index_pair\tnum_matches\tpercentage_of_hopped_reads\tpercentage_of_total_reads\n')
        for key, values_dict in sorted_hopped:
            hopped_tsv.write(f'{values_dict['index_string']}\t{values_dict['count']}\t{100*(values_dict['count']/hopped_read_count)}\t{100*(values_dict['count']/total_read_count)}\n')
         
        overview.write(f'Read Counts\n--------------------\n')
        overview.write(f'matched: {matched_read_count}\n')
        overview.write(f'hopped: {hopped_read_count}\n')
        overview.write(f'unknown: {unknown_pairs_count}\n')
        overview.write(f'total reads: {total_read_count}\n')
        overview.write(f'\nPercentage of reads\n--------------------\n')
        overview.write(f'matched: {100*matched_read_count/total_read_count}\n')
        overview.write(f'hopped: {100*hopped_read_count/total_read_count}\n')
        overview.write(f'unknown: {100*unknown_pairs_count/total_read_count}\n')


        
            

main()