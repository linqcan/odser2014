#!/usr/bin/env python
"""
This module creates the HTML files needed for browsing the
result files using a web browser.
"""
import os
import re

RESULT_DIR = "../results/"

HTML_HEAD = """
<html>
<head>
<title>%s</title>
</head>
<body>
<h1>%s</h1>
<ul>
"""

HTML_FOOT = """
</ul>
</body>
</html>
"""

def get_all_paper_ids():
  """
  Returns all paper IDs in the result folder.
  """
  ids = []
  file_names = os.listdir(RESULT_DIR)
  for file_name in file_names:
    if "plotOutliers.pdf" in file_name:
      paper_id = file_name.split("-")[0]
      ids.append(paper_id)
  return sorted(list(set(ids)))

def get_all_data_sets_for_paper(paper_id):
  """
  Returns the full name for all data sets for a given paper.
  """
  data_sets = []
  file_names = os.listdir(RESULT_DIR)
  for file_name in file_names:
    match = re.search(paper_id+"-(.*)-plotOutliers.pdf", file_name)
    if match:
      set_name = match.group(1)
      data_sets.append(paper_id+"-"+set_name)
  return sorted(data_sets)


def create_index_for_paper(paper_id, data_sets):
  """
  Creates the index page for a paper.
  """
  title = get_title(paper_id)
  meta = get_meta(paper_id)
  output = HTML_HEAD % (title, title)
  output = output + "<p>"+meta["authors"]+". "+meta["year"]+".</p>"

  for data_set in data_sets:
    output = output + "\n<h2>%s</h2>\n" % data_set
    output = output + "<li><a href=\"%s-descStatistics.html\">Descriptive statisitcs</a></li>\n" % data_set
    output = output + "<li><a href=\"%s-plotOutliers.pdf\">Outlier plot</a></li>\n" % data_set
    output = output + "<li><a href=\"%s-normPlotsOutliers.pdf\">Normality plot with outliers</a></li>" % data_set
    output = output + "<li><a href=\"%s-normPlotsNoOutliers.pdf\">Normality plot without outliers</a></li>" % data_set
    output = output + "<li><a href=\"%s-swStatOutlier.html\">Result from a Shapiro-Wilks test (with outliers)</a></li>\n" % data_set
    output = output + "<li><a href=\"%s-swStatNoOutlier.html\">Result from a Shapiro-Wilks test (without outliers)</a></li>\n" % data_set
    output = output + "<li><a href=\"%s-wilcoxonStat.html\">Result from a Mann-Whitney U test</a></li>\n" % data_set
    output = output + "<li><a href=\"%s-studentStat.html\">Result from a Welch's t-test </a></li>\n" % data_set
  output = output + HTML_FOOT
  file_handle = open(RESULT_DIR+paper_id+"-index.html", "w")
  file_handle.write(output)
  file_handle.close()
  return output

def create_main_index(paper_ids):
  """
  Creates the main index.
  """
  main_title = "Index for results"
  output = HTML_HEAD % (main_title, main_title)
  for paper_id in paper_ids:
    title = get_title(paper_id)
    output = output + "<li><a href=\"%s-index.html\">%s</a></li>" % (paper_id, title)
  output = output + HTML_FOOT
  file_handle = open(RESULT_DIR+"index.html", "w")
  file_handle.write(output)
  file_handle.close()
  return output

def get_title(paper_id):
  """
  Returns the title for a paper id.
  """
  file_handle = open("../report/references.bib", "r")
  found_paper = False
  title = paper_id
  for line in file_handle:
    if paper_id in line:
      found_paper = True
      continue
    if found_paper and ("title" in line):
      match = re.search("title\s*=\s*{(.*)}", line)
      if match:
        title = match.group(1)
      break
  file_handle.close()
  return title

def get_meta(paper_id):
  """
  Returns the author and year for a paper id as a dictionary.
  """
  file_handle = open("../report/references.bib", "r")
  found_paper = False
  found_author = False
  found_year = False
  authors = "N/A"
  year = "N/A"
  for line in file_handle:
    if paper_id in line:
      found_paper = True
    if found_paper and ("author" in line):
      match = re.search("author\s*=\s*{(.*)}", line)
      if match:
        authors = match.group(1)
        found_author = True
    if found_paper and ("year" in line):
      match = re.search("year\s*=\s*{(.*)}", line)
      if match:
        year = match.group(1)
        found_year = True
    if found_paper and found_author and found_year:
      break
  file_handle.close()
  return {"authors":authors, "year":year}

def main():
  """
  The module's main function.
  """
  paper_ids = get_all_paper_ids()
  for paper_id in paper_ids:
    data_sets = get_all_data_sets_for_paper(paper_id)
    create_index_for_paper(paper_id, data_sets)
  create_main_index(paper_ids)
  print "[createHtmlDocs] Generated HTML docs"

if __name__ == "__main__":
  main()
