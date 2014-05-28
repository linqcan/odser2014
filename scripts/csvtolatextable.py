#!/usr/bin/env python
"""
This script converts a csv file to a Latex table.
The assumption is that the first row of the csv file contains the header.
"""
import sys
import os.path
import csv

def main(file_path):
  """
  Main function. Returns an exit code.
  """
  if not os.path.exists(file_path):
    print("File %s does not exist!" % file_path)
    return 1
  # Read csv file
  csv_file = open(file_path, "rb")
  csvreader = csv.reader(csv_file, delimiter=",")
  header = csvreader.next() 
  table_spec = ""
  factor =  1.00 / len(header)
  for i in range(0, len(header)):
    table_spec = table_spec + ("|p{%.2f\\textwidth}" % factor)
  begin_tabular = """

  \\begin{table}
    \\caption{CAPTION}
    \\label{tab:LABEL}
    {\\small
    \\begin{tabular}{"""+table_spec+"""|}
    \\hline
  """
  end_tabular = """
    \\end{tabular}
    }
  \\end{table}
  """

  result = begin_tabular + "\n    "
  for column in header:
    result = result + ("\\textbf{%s} &" % column.strip())
  result = result.rstrip("&") + "\\\ \\hline \n"

  for row in csvreader:
    newline = "    "
    for column in row:
      newline = newline + column + " &"
    newline = newline.rstrip("&")
    newline = newline + " \\\ \\hline"
    result = result + newline + "\n"
  
  result = result + end_tabular
  csv_file.close()
  output_file = open("latextable.tex", "w")
  output_file.write(result)
  output_file.close()
  print result



if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Missing argument FILE")
    sys.exit(1)
  exit_code = main(sys.argv[1])
  sys.exit(exit_code)
