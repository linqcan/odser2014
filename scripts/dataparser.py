#!/usr/bin/env python
"""
This module removes strings from a result file generated by ELKI.
The module takes a CSV file and an output path as arguments.
"""
import sys
import csv

def main(args):
  """
  args[0] : data file (csv)
  args[1] : output file path
  """
  if len(args) < 1:
    print 'An input file needs to be provided!'
    return
  if len(args) < 2:
    print("An output path needs to be provided!")
    return

  filename = args[0]
  outputfilename = args[1]
  csvfile = open(filename, 'rb')
  outputfile = open(outputfilename, 'w')
  csvrows = csv.reader(csvfile, delimiter=' ')
  for row in csvrows:
    newrow = list()
    for col in row:
      if 'ID' in col:
        # Skip the ID column
        continue
      if 'radius' in col:
        # Skip radius score for LOCI
        continue
      if '=' in col:
        col = col.split('=')[1]
      newrow.append(col)
    rowstr = ','.join(map(str, newrow)) + '\n'
    # print rowstr # DEBUG
    outputfile.write(rowstr)
  csvfile.close()
  outputfile.close()

def parseResultFile(file_path, output_file_path):
  main([file_path, output_file_path])

if __name__ == '__main__':
  main(sys.argv[1:])
