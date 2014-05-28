library(rjson)

getYAxisLabel <- function(datasetId) {
  # Returns the y-axis label  for a dataset ID
  # All axis labels are stored in data_sets/axislabels.json
  #
  # Args:
  #   datasetId: The ID of the dataset to return a y-axis label for.
  #
  # Returns:
  #   A character string with the y-axis label for the dataset ID

  labels <- fromJSON(file="../data_sets/axislabels.json") # HARDCODED!
  yLabel <- "undefined"
  if (datasetId %in% names(labels$yaxis)) {
    yLabel <- labels$yaxis[datasetId]
  }
  return(as.character(yLabel))
}

getXAxisLabel <- function(datasetId) {
  # Returns the x-axis label  for a dataset ID
  # All axis labels are stored in data_sets/axislabels.json
  #
  # Args:
  #   datasetId: The ID of the dataset to return a x-axis label for.
  #
  # Returns:
  #   A character string with the x-axis label for the dataset ID

  labels <- fromJSON(file="../data_sets/axislabels.json") # HARDCODED!
  xLabel <- "Index"
  if (datasetId %in% names(labels$xaxis)) {
    xLabel <- labels$xaxis[datasetId]
  }
  return(as.character(xLabel))
}
