#!/usr/bin/env python
"""
This module lists all data sets that have reported outliers.
No input is required.
"""
import os
import re

DIR = "../results/"
NUM_DATASETS = 0

def get_outliers(file_name):
  """
  Returns the number of outliers for a data set
  given its file name.
  """
  path = DIR + file_name
  file_handle = open(path, "r")
  outliers = 0

  for line in file_handle:
    if line.startswith("Original"):
      stats = re.search(r"\s(\w+\.\w+)\s\\\\", line)
      if stats:
        outliers = float(stats.group(1))
        return outliers


def get_datasets_with_outliers():
  """
  Returns a list containing all data sets with outliers.
  Each entry in the list i a tuple containing the dataset ID and
  the number of outliers.
  """
  all_files = os.listdir(DIR)
  datasets = []
  global NUM_DATASETS

  for file_name in all_files:
    if file_name.endswith("descStatistics.tex"):
      NUM_DATASETS = NUM_DATASETS + 1
      outliers = get_outliers(file_name)
      if outliers > 0:
        datasets.append((file_name.replace("-descStatistics.tex", ""), outliers))

  return sorted(datasets)


if __name__ == "__main__":
  datasets = get_datasets_with_outliers()
  print("OUTLIERS\tDATA SET")
  for dataset, outliers in datasets:
    print(str(outliers) + "\t" + dataset)
  print("\nFound %d/%d data sets with outliers." % (len(datasets), NUM_DATASETS))
