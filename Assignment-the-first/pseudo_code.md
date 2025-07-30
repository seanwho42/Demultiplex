### pseudo-code:
```
Initialize a dictionary with tuple permutations of all correct indices and all reverse compliments as the keys, and frequency (0) as the values. (in order of Index, Reverse compliment)

initialize variables as 0 for 
 - the number of read-pairs with properly matched indexes (per index-pair),
 - the number of read pairs with index-hopping observed, and
 - the number of read-pairs with unknown index(es).

Open all files to read and all files to be written in.
    Iterate through all files at the same time for comparisons.
        Load the four lines of each read into memory with
            If the avg qscores for both indices are above the threshold
            indices then
                If the the tuple of R2 and R3 is in the dictionary
                    increment the frequency in the index pair dictionary
                    
                    ...and if R3 is the reverse compliment of R2
                        save the forward read in correct forwards
                        save the reverse read in correct reverses
                        increment 
                    otherwise
                        save the forward read in hopped forwards
                        save the reverse read in hopped reverses
                otherwise
                    increment unknown
                    save the forward read in unknown forwards
                    save the reverse read in the unknown reverses
            otherwise
                increment unknown
                save the forward read in unknown forwards
                save the reverse read in the unknown reverses

write two tsvs: one for matched index pair frequencies, one for hopped frequencies
write summary file which shows
 - the number of read-pairs with properly matched indexes (per index-pair),
 - the number of read pairs with index-hopping observed, and
 - the number of read-pairs with unknown index(es).

```

### high level functions:
```python
def main(paths: list):
    '''
    main function which takes a list of file paths, reads through all four files and
    saves fastq files (fwd and rev) for matched indices, hopped indices, and unknown

    also saves summary data to a separate file indicies_summary.txt (total matched, total unmatched),
    and tsvs of frequencies for each index pair occurance
    '''
```

writing reads to files:
```python
## don't know if this is the right way to annotate file object types but here we are
def save_read( : list, file: _io.TextIOWrapper, index_pair : tuple = NULL, ):
    '''
    takes a read from a fastq file as a list, a file object, and an (optional) index pair tuple and writes
    the lines in the read, with the header modified by the index_pair tuple (if provided)
    '''
```


```python
def get_reads(files: tuple) -> tuple:
    '''
    takes files as a tuple and returns a tuple of four lines (a read) as a list
    '''
# example:
r1, r2, r3, r4 = get_reads((f1, f2, f3, f4))
```

```python
def populate_dict(file_path : string) -> dict:
    '''
    takes the file path for the file on talapas which has all the indices, parses through it, and populates
    a dictionary with all the index pairs as a tuple (Read 2 index, Read 3 index (reverse compliment)) as
    keys and frequencies as a value
    '''
```