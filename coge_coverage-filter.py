#!/usr/bin/env python3

import csv
import os.path
from argparse import ArgumentParser

__author__ = 'groverj3'

# Function to determine if you've passed a valid filename


def file_validity(parser, arg):
    if not os.path.exists(arg):
        parser.error('%s is not a valid file path.' % arg)
    else:
        pass

# Parse command line file path and coverage, store in variables

parser = ArgumentParser(description='This script is exactly what you think it is. It filters csv files formatted for '
                                    'CoGe\'s LoadExperiment function based on read coverage')

parser.add_argument('input_file',
                    help='Input Bismark context-specific methylation calls',
                    metavar='File')

parser.add_argument('-c', '--coverage',
                    type=int,
                    required=True,
                    help='Minimum coverage to report in output csv')

coge_path = parser.parse_args().input_file
coverage = parser.parse_args().coverage

# Check validity of input filename

file_validity(parser, coge_path)

# Output file is input_file_path.coge.csv

filtered_coge_path = '%s.filtered.coge.csv' % coge_path

print('Filtering out cytosines with read coverage <', coverage, 'from:\n',
      coge_path,
      '\nSaving filtered file to:\n',
      filtered_coge_path)

# Iterate through rows in csv and send that row to output file only if read coverage is above the specified value

with open(coge_path, 'r') as unfiltered_csv, open(filtered_coge_path, 'w') as filtered_csv:
    coge_methyl_summary = csv.reader(unfiltered_csv)
    filtered_methyl_summary = csv.writer(filtered_csv)

    for row in coge_methyl_summary:
        total_reads = int(row[5])
        if total_reads >= coverage:
            filtered_methyl_summary.writerow(row)

print('\nDone!')
