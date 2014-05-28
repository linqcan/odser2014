#!/usr/bin/env python
"""
This is the data analysis pipeline.
It performs one-dimensional or
multi-dimensional outlier detection on a data set.
The data set should be in a CSV file and contain no headers.

Returns result files in the folder "../results".

Takes a CSV file or a folder with CSV files as an argument.
If a folder is given it will be traversed recursively.
Note! Headers in CSV files are not supported!

Usage: pipeline.py FILE|FOLDER
"""
import os.path
import shutil
import subprocess
import sys

import locirmax
import dataparser
import configmanager as cm

DEBUG = False # Default is False
OUTPUT_PATH = "../results/"
FILES_ANALYZED = 0

def print_msg(msg):
  print "[pipeline] " + msg

def log(msg):
  if DEBUG:
    print_msg("Debug: " + msg)

def main(args):
  """

  if multi-dim => LOCI & ABOD
  else => MZS

  FILE  data set in CSV format
  """

  if len(args) < 1:
    print_msg("No file argument supplied")
    sys.exit(1)

  file_path = args[0]

  if not ".csv" in file_path:
    # A certain file extension is required to
    # make path manipulation easier.
    print_msg("Input file must have file extension .csv!")
    print_msg("File: "+file_path)
    sys.exit(1)

  if not os.path.isfile(file_path):
    print_msg("File not found! "+file_path)
    sys.exit(1)

  #Parse the data set's ID
  dataset_id = file_path.split("/")
  if len(dataset_id) > 0:
    dataset_id = dataset_id[-1]
  else:
    dataset_id = file_path
  dataset_id = dataset_id.split("-")[0]

  print_msg("Analyzing "+file_path)

  # Figure out the number of dimensions of the data set
  file_handle = open(file_path, "r")
  line = file_handle.readline()
  file_handle.close()
  dims = len(line.split(","))
  print_msg(str(dims) + " dimension(s)")

  output_path = OUTPUT_PATH
  output_path = os.path.abspath(output_path) + "/"

  if dims > 1:
    # Make sure data set contains at least 20 rows
    file_handle = open(file_path, "r")
    rows = sum(1 for i in file_handle)
    file_handle.close()
    if rows < 20:
      print_msg("Number of data points has to be >20!")
      print_msg("Aborting!")
      sys.exit(1)

    # Configure output path for ELKI
    output_path = output_path+dataset_id+"/"

    # LOCI, ABOD
    loci_file_name = "loci-mdef-outlier_order.txt"
    loci_parsed_file_path = output_path+"parsed-"+loci_file_name
    abod_file_name = "abod-outlier_order.txt"
    abod_parsed_file_path = output_path+"parsed-"+abod_file_name

    # LOCI parameters
    loci_alpha = cm.get("loci", "alpha")
    loci_nmin = cm.get("loci", "nmin")
    loci_std = cm.get("loci", "std")

    # Calculate rmax for LOCI
    loci_rmax_args = []
    loci_rmax_args.append(file_path)
    loci_rmax_args.append(loci_alpha)
    loci_rmax = locirmax.main(loci_rmax_args)

    # Run LOCI
    run_elki(
        file_path,
        output_path,
        "loci",
        {
          "loci.alpha": loci_alpha,
          "loci.rmax": loci_rmax,
          "loci.nmin": loci_nmin
        }
    )

    # Run ABOD
    run_elki(
        file_path,
        output_path,
        "abod",
        None
    )

    # Remove description strings and ID columns
    print_msg("Removing string clutter from result files")
    dataparser.parseResultFile(output_path+loci_file_name, loci_parsed_file_path)
    dataparser.parseResultFile(output_path+abod_file_name, abod_parsed_file_path)

    # Label outliers detected by LOCI
    label_args = ["lociLabelOutliers.R"]
    label_args.append(loci_parsed_file_path)
    label_args.append(str(loci_std))
    label_command = ["Rscript"]
    label_command.extend(label_args)
    print_msg("Running LOCI labelling: "+str(label_command))

    try:
      subprocess.check_output(label_command)
    except subprocess.CalledProcessError as ex:
      print_msg("")
      print_msg("Process failed!")
      print_msg("Process command "+str(ex.cmd))
      print_msg("Process output "+ex.output)
      return

  else:
    # MZS
    mzs_std = cm.get("mzs", "std")

    # Copy data to results directory, create dir if not exists
    file_name = file_path.split("/")[-1]
    mzs_file_path = output_path+file_name
    mzs_file_path = mzs_file_path.replace(".csv", "-original.csv")

    if not os.path.exists(output_path):
          os.makedirs(output_path)
    shutil.copyfile(file_path, mzs_file_path)

    # Run MZS
    mzs_command = ["Rscript"]
    mzs_args = ["modifiedZScore.R"]
    mzs_args.append(mzs_file_path)
    mzs_args.append(str(mzs_std))
    mzs_command.extend(mzs_args)
    print_msg("Running MZS: "+str(mzs_command))

    try:
      subprocess.check_output(mzs_command)
    except subprocess.CalledProcessError as ex:
      print_msg("")
      print_msg("Process failed!")
      print_msg("Process command "+str(ex.cmd))
      print_msg("Process output "+ex.output)
      return

    # Create plots
    plot_command = ["Rscript"]
    plot_args = ["plotOneDimOutliers.R"]
    plot_args.append(mzs_file_path.replace("original", "labelled"))
    plot_command.extend(plot_args)
    print_msg("Plotting: " + str(plot_command))

    try:
      subprocess.check_output(plot_command)
    except subprocess.CalledProcessError as ex:
      print_msg("")
      print_msg("Process failed!")
      print_msg("Process command "+str(ex.cmd))
      print_msg("Process output "+ex.output)
      return

    # Run significance tests
    sig_command = ["Rscript"]
    sig_args = ["sigTest.R"]
    sig_args.append(mzs_file_path.replace("original", "labelled"))
    sig_command.extend(sig_args)
    print_msg("Running significance tests: "+str(sig_command))

    try:
      subprocess.check_output(sig_command)
    except subprocess.CalledProcessError as ex:
      print_msg("")
      print_msg("Process failed!")
      print_msg("Process command "+str(ex.cmd))
      print_msg("Process output "+ex.output)
      return

  print_msg("All analysis have been conducted.")
  print_msg("Check "+output_path+" for the results!")
  print_msg("\n")


def run_elki(file_path, output_path, algorithm, params):
  """
  Runs ABOD or LOCI in ELKI.

  params  Dictionary with parameters needed for an algorithm.

  Returns 0 if successful, 1 otherwise.
  """
  elki_path = "../bin/elki.jar"

  print_msg("Running "+algorithm+" using "+file_path+" with parameters: "+str(params))
  if not os.path.isfile(file_path):
    print_msg("File not found!")
    print_msg(file_path)
    return 1

  if not os.path.isfile(elki_path):
    print_msg("ELKI binary not found!")
    return 1

  command = ["/usr/bin/env"]
  args = ["java"]

  args.append("-jar")
  args.append(elki_path)
  args.append("KDDCLIApplication")
  args.append("-dbc.in")
  args.append(file_path)

  if algorithm == "abod":
    args.append("-algorithm")
    args.append("outlier.ABOD")
  elif algorithm == "loci":
    args.append("-algorithm")
    args.append("outlier.lof.LOCI")
    args.append("-loci.rmax")
    args.append(str(params["loci.rmax"]))
    args.append("-loci.nmin")
    args.append(str(params["loci.nmin"]))
    args.append("-loci.alpha")
    args.append(str(params["loci.alpha"]))
  else:
    print_msg("Unknown algorithm!")
    return 1

  args.append("-resulthandler")
  args.append("ResultWriter")
  args.append("-out")
  args.append(output_path)
  command.extend(args)

  try:
    subprocess.check_output(command)
  except subprocess.CalledProcessError as ex:
    print_msg("Command "+str(command)+" returned a non-zero exit code!")
    print_msg("Process command "+str(ex.cmd))
    print_msg("Process output: "+ex.output)
  return 0

def walk_dir(path):
  """
  Recursively walk through a directory and its subdirectories
  and run the analyze on all .csv files found
  """
  contents = os.listdir(path)
  files = []
  dirs = []

  for item in contents:
    if os.path.isfile(os.path.join(path, item)):
      if item.endswith(".csv"):
        files.append(item)
      continue
    if os.path.isdir(os.path.join(path, item)):
      dirs.append(item)
      continue

  for sub_dir in dirs:
    walk_dir(os.path.join(path, sub_dir))
  analyze_files(path, files)

def analyze_files(path, files):
  """
  Runs the analyze on all files in the supplied list.
  """
  for data_file in files:
    file_path = os.path.join(path, data_file)
    main([file_path])
    global FILES_ANALYZED
    FILES_ANALYZED = FILES_ANALYZED + 1

def clean_results():
  path = os.path.abspath(OUTPUT_PATH)
  if os.path.exists(path):
    print_msg("Removing all results in '"+path+"'")
    shutil.rmtree(path)
  else:
    print_msg("Results folder does not exist. Aborting.")

if __name__ == "__main__":

  if len(sys.argv) < 2:
    print_msg("No arguments supplied!")
    sys.exit(1)

  if sys.argv[1] == "clean":
    clean_results()
    sys.exit(0)

  path = sys.argv[1]
  if os.path.isdir(path):
    # A directory, run all csv files in it
    walk_dir(path)
    print_msg("Done. Analyzed %s files " % str(FILES_ANALYZED))
  else:
    # Just a file, run it
    main(sys.argv[1:])
