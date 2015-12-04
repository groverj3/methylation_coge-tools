#!/usr/bin/env python3

import re

__author__ = 'groverj3'

# Module to strip nonsense from chromosome IDs


def fix_chromosome_id(chromosome):
    replacements = [('lcl\|', ''),
                    ('gi\|', ''),
                    ('chromosome', ''),
                    ('^chr', ''),
                    ('^_+', ''),
                    ('\s+', ''),
                    ('^\s', ''),
                    ('\s$', ''),
                    ('\/', '_'),
                    ('\|$', ''),
                    ('\|', '_'),
                    ('\(', '_'),
                    ('\)', '_'),
                    ('_+', '')]  # Regex and substitutions from list of tuples, add cases as needed

    for rep_tuple in replacements:  # Compile as regex objects, substitute regex as specified in the tuple list
        regex_pattern = re.compile(rep_tuple[0], re.IGNORECASE)
        rep = rep_tuple[1]
        chromosome = regex_pattern.sub(rep, chromosome)

    if re.search(r'^0+$', chromosome):  # Set chr IDs composed only of arbitrary number of zeroes to "0"
        chromosome = 0
    elif chromosome != 0:  # Or attempt to strip leading arbitrary number of leading zeroes
        chromosome = re.sub(r'^0+', '', chromosome)

    if chromosome == 'chloroplast':  # Set chloroplast ID to "C"
        chromosome = 'C'
        return chromosome
    elif chromosome == 'mitochondria':  # Set mitochondria ID to "M"
        chromosome = 'M'
        return chromosome
    else:
        return chromosome
