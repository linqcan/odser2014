#!/usr/bin/env python
"""
This module contains various functions for creating pieces of Latex
code used for the report.
"""

import listSetsWithOutliers
import statisticsDataSets
import json

def create_plot_outliers_matrix():
  """
  Creates a figure with outlier plots as subfigures
  """
  datasets = listSetsWithOutliers.get_datasets_with_outliers()

  file_path = "../results/outlier-plot-matrix.tex"
  file_handle = open(file_path, "w")

  figures = 1
  subfigures = 0
  end_figure = "\n\\end{figure}\n"

  file_handle.write(create_figure(figures))
  for dataset,outliers in datasets:
    if subfigures != 0 and subfigures % 9 == 0:
      figures = figures + 1
      file_handle.write(end_figure)
      file_handle.write(create_figure(figures))
    tex = create_subfigure(dataset)
    file_handle.write(tex)
    subfigures = subfigures + 1
  file_handle.write(end_figure)
  file_handle.close()
  print("[createLatex] Wrote file "+file_path)

def create_figure(figures):
  begin_figure = "\n\\begin{figure}\n  \\centering"
  figure_caption = "\n  \\caption{Plots displaying outliers for the analyzed papers. Outliers are marked with a cross. The original mean is displayed as a solid horizontal  line whereas the mean after outlier removal is shown as a dotted line.}"
  figure_label = "\n  \\label{fig:outliers-%d}"
  result = begin_figure + figure_caption + (figure_label % figures)
  return result

def create_subfigure(dataset):
  file_path = "../results/"+dataset+"-plotOutliers.pdf"
  paper_id = dataset.split("-")[0]
  scaling = "0.3"
  result = """
  \\subcaptionbox{"""+get_plot_caption(dataset)+""" \\citep{"""+paper_id+"""} \\label{fig:"""+dataset+"""-plotOutliers}}
    {\\includegraphics[width="""+scaling+"""\\textwidth]{"""+file_path+"""}}"""
  return result

def get_plot_caption(dataset):
  """
  Returns the caption for a dataset.
  """
  json_file = open("../data_sets/captions.json", "r")
  json_obj = json.load(json_file)
  captions = json_obj["plotOutliersCaptions"]
  if dataset in captions.keys():
    return captions[dataset]
  else:
    return "\\textsf{"+dataset+"}"

def create_sample_sizes_table():
    """
    Writes the sample sizes table
    """
    output = statisticsDataSets.get_latex_output()
    file_path = "../results/samplesizestable.tex"
    file_handle = open(file_path, "w")
    file_handle.write(output)
    file_handle.close()
    print("[createLatex] Wrote file "+file_path)

def create_sample_sizes_modified_table():
    """
    Writes the sample sizes table
    """
    output = statisticsDataSets.get_latex_output_labelled()
    file_path = "../results/samplesizesmodifiedtable.tex"
    file_handle = open(file_path, "w")
    file_handle.write(output)
    file_handle.close()
    print("[createLatex] Wrote file "+file_path)

if __name__ == "__main__":
  # Functions to run when script is called
  create_plot_outliers_matrix()
  create_sample_sizes_table()
  create_sample_sizes_modified_table()
