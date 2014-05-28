#!/usr/bin/env python
"""
This script prints the sample size of
all data sets available in the "results" folder.
"""
import sys
import os

DIR = "../results/"
ORIGINAL = "original"
LABELLED = "labelled"

def get_all_datasets(set_type):
  """
  Returns file names for all datasets of type set_type.
  """
  all_files = os.listdir(DIR)
  datasets = []

  for file_name in all_files:
    if file_name.endswith(set_type+".csv"):
      datasets.append(file_name)

  return sorted(datasets)

def get_metadata(datasets):
  """
  Returns a list with data set objects inlcuding their meta data.
  """
  metadata = []
  for dataset in datasets:
    # Fetch the sample size of the original data
    file_handle = open(DIR+dataset, "r")
    lines = file_handle.readlines()
    file_handle.close()
    reference = dataset.split("-")[0]
    name = dataset.split("-")[1:-1]
    name = " ".join(name)
    name = name.replace("_", " ")
    # Add information to our collection
    metadata.append({
      "name": name,
      "reference": reference,
      "sampleSize": len(lines),
      "hasOutliers": False
    })
  return metadata

def get_metadata_labelled(datasets):
    """
    Returns a list with data set objects inlcuding their meta data.
    """
    metadata = []
    for dataset in datasets:
      # Fetch the sample size of the labelled data
      file_handle = open(DIR+dataset, "r")
      outliers = 0
      samples = -1
      has_outliers = False
      for line in file_handle:
        samples = samples + 1
        if "TRUE" in line:
          has_outliers = True
          outliers = outliers + 1
      file_handle.close()
      reference = dataset.split("-")[0]
      name = dataset.split("-")[1:-1]
      name = " ".join(name)
      name = name.replace("_", " ")
      # Add information to our collection
      metadata.append({
        "name": name,
        "reference": reference,
        "sampleSize": samples-outliers,
        "hasOutliers": has_outliers
      })
    return metadata

def get_latex_output():
  datasets = get_all_datasets(ORIGINAL)
  metadata = get_metadata(datasets)
  output = ""
  output = output + """
\\begin{longtable}{lll}
\t\\caption{Sample sizes for the original data sets used in this study} \\\\
\t\\hline
\t\\textbf{Data set name} & \\textbf{Reference} & \\textbf{Sample size}\\\\ \\hline \\endhead
\t\\label{tab:samplesizes}\n"""
  for dataset in metadata:
    output = output + "\t" + dataset["name"] + " & " + "\\citet{"+dataset["reference"]+"}" + " & " + str(dataset["sampleSize"]) + " \\\\ \hline" + "\n"
  output = output + "\\end{longtable}"
  return output

def get_latex_output_labelled():
  datasets = get_all_datasets(LABELLED)
  metadata = get_metadata_labelled(datasets)
  output = ""
  output = output + """
\\begin{longtable}{lll}
\t\\caption{Sample sizes for the data sets from which outliers were removed.} \\\\
\t\\hline
\t\\textbf{Data set name} & \\textbf{Reference} & \\textbf{Sample size}\\\\ \\hline \\endhead
\t\\label{tab:samplesizes-modified}\n"""
  for dataset in metadata:
    if dataset["hasOutliers"]:
      output = output + "\t" + dataset["name"] + " & " + "\\citet{"+dataset["reference"]+"}" + " & " + str(dataset["sampleSize"]) + " \\\\ \hline" + "\n"
  output = output + "\\end{longtable}"
  return output

if __name__ == "__main__":
  if len(sys.argv) > 1:
    if sys.argv[1] == "--latex":
      print get_latex_output()
      sys.exit(0)
    if sys.argv[1] == "--latex-labelled":
      print get_latex_output_labelled()
      sys.exit(0)

  datasets = get_all_datasets(ORIGINAL)
  metadata = get_metadata(datasets)

  output = "Data set name" + "\t" + "Reference" + "\t" + "Sample size" + "\n"
  for dataset in metadata:
    output = output + dataset["name"] + "\t" + dataset["reference"] + "\t"+ str(dataset["sampleSize"]) + "\n"

  sizes = map(lambda dataset: dataset["sampleSize"], metadata)
  mean = float(sum(sizes)/len(sizes)) if len(sizes) > 0 else float('nan')
  output = output + "\nAverage sample size: %f" % mean

  print output
