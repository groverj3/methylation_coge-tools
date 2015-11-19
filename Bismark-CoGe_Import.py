#!/usr/bin/env python3

__author__ = 'groverj3'

import csv
import os.path
from argparse import ArgumentParser


# Function to determine if you've passed a valid filename

def file_validity(parser, arg):
    if not os.path.exists(arg):
        parser.error('%s is not a valid file path.' % arg)
    else:
        return open(arg, 'r')


# Function to return number from a string, to extract chromosome number from string

def get_num(x):
    return int(''.join(substring for substring in x if substring.isdigit()))


# Parse command line file path, store in variable

parser = ArgumentParser(description='CoGe-ifier for Bismark converts context-specific methylation call files '
                                    'generated by Bismark into .csv format for compatibility with CoGe\'s '
                                    'LoadExperiment Functionality')
parser.add_argument('input_file', help='Input Bismark context-specific methylation calls', metavar='File')
parser.add_argument('-c', '--coverage', type=int,
                    help='Minimum coverage to report in an additional output .csv. Default = 1 (Unfiltered)')
parser.add_argument('-u', '--unfiltered', default='t', choices=['t', 'f'],
                    help='Outputs an unfiltered .csv. Default = t')
min_coverage = parser.parse_args().coverage
unfiltered = parser.parse_args().unfiltered
methyl_path = parser.parse_args().input_file

# Check validity of input/output path

file_validity(parser, methyl_path)

# Save paths for later use

coge_filtered_path = '%s.filtered.coge.csv' % methyl_path
coge_unfilitered_path = '%s.coge.csv' % methyl_path

# Let the user know it's working

print('Calculating % Methylation on a per Cytosine Basis and formatting for CoGe-import from:\n', methyl_path)
if min_coverage:
    print('Saving CoGe-formatted and coverage-filtered file to:\n', coge_filtered_path)
if unfiltered == 't':
    print('Saving CoGe-formatted unfiltered file to:\n', coge_unfilitered_path)

# Open the Bismark Methylation Extractor output file and create an output for CoGe upload

bismark_tsv = open(methyl_path, 'r')
bismark_summary = csv.reader(bismark_tsv, delimiter='\t')

if min_coverage:
    coge_filtered_csv = open(coge_filtered_path, 'w')
    coge_formatted_filtered = csv.writer(coge_filtered_csv)
if unfiltered == 't':
    coge_unfiltered_csv = open(coge_unfilitered_path, 'w')
    coge_formatted_unfiltered = csv.writer(coge_unfiltered_csv)

# Initialize a dictionary that will serve at the primary data structure

bismark_dict = {}

# Iterate over the tsv file rows updating the dictionary as it goes

next(bismark_summary)  # Skip header
for row in bismark_summary:
    chrm = row[2]  # Chromosome number saved to "chrm"
    pos = row[3]  # Position saved to "pos"
    met = row[1]  # methylation status saved to "met"
    if chrm not in bismark_dict:  # Add chromosome number as key if not in dict
        bismark_dict[chrm] = {}  # Make its value an empty dict
    if pos not in bismark_dict[chrm]:  # Add position as key in second level if not already in dict
        bismark_dict[chrm][pos] = {'metc': 0, 'total': 0}  # Make its value the running counts of methyl status
    if met == '+':
        bismark_dict[chrm][pos]['metc'] += 1
        bismark_dict[chrm][pos]['total'] += 1  # Add 1 to total and metc counts if methylated
    else:
        bismark_dict[chrm][pos]['total'] += 1  # Add 1 to total count if unmethylated

# Iterate over the nested dictionary to get percent methylation as decimal and add as new key:value pair

for chrm in bismark_dict:
    for pos in bismark_dict[chrm]:
        bismark_dict[chrm][pos]['dec_met'] = float(bismark_dict[chrm][pos]['metc']) / float(
            bismark_dict[chrm][pos]['total'])  # Calculate methylation as a decimal

# Iterate over the dictionary for file-outputs

for chrm in bismark_dict:
    for pos in bismark_dict[chrm]:  # Nested loop
        chrm_key = get_num(chrm)  # Save chromosome number key, position key, and methylation fraction
        pos_key = pos
        dec_met = bismark_dict[chrm][pos]['dec_met']
        total = bismark_dict[chrm][pos]['total']
        if min_coverage and total >= min_coverage:
            coge_formatted_filtered.writerow(
                [chrm_key, pos_key, pos_key, 1, dec_met, total])  # Output as filtered .csv file
        if unfiltered == 't':
            coge_formatted_unfiltered.writerow(
                [chrm_key, pos_key, pos_key, 1, dec_met, total])  # Output as unfiltered .csv file

# Ultimate victory

print('\nDone!')
