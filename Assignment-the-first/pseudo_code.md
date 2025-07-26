```
Initialize a dictionary with tuple permutations of all correct indices and all reverse compliments as the keys, and frequency (0) as the values. (in order of Index, Reverse compliment)

Open all files to read and all files to be written in.
    Iterate through all files at the same time for comparisons.
        Load the four lines of each read into memory
            If the avg qscores for both indices are above the threshold
            indices then
                If the the tuple of R2 and R3 is in the dictionary
                    increment the frequency in the index pair dictionary
                    
                    ...and if R3 is the reverse compliment of R2
                        save the forward read in correct forwards
                        save the reverse read in correct reverses
                    otherwise
                        save the forward read in hopped forwards
                        save the reverse read in hopped reverses
                otherwise
                    save the forward read in unknown forwards
                    save the reverse read in the unknown reverses
            otherwise
                save the forward read in unknown forwards
                save the reverse read in the unknown reverses

save the frequency dictionary for future reference

saving reads is its own function which will also modify the headers
```