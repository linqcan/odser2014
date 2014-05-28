library(rjson)

getTableCaption <- function(datasetId) {
  # Returns a table caption for a dataset ID
  # All captions are stored in data_sets/captions.json
  #
  # Args:
  #   datasetId: The ID of the dataset to return a caption for.
  #
  # Returns:
  #   A character string with a caption for the dataset ID

  captions <- fromJSON(file="../data_sets/captions.json") # HARDCODED!
  tableCaption <- paste("\\emph{No caption found for}", datasetId)
  if (datasetId %in% names(captions$tableCaptions)) {
    tableCaption <- captions$tableCaptions[datasetId]
  }
  return(as.character(tableCaption))
}

getPlotOutliersCaption <- function(datasetId) {
  # Returns a caption for the plotOutliers figure for a dataset ID
  # All captions are stored in data_sets/captions.json
  #
  # Args:
  #   datasetId: The ID of the dataset to return a caption for.
  #
  # Returns:
  #   A character string with a caption for the dataset ID

  captions <- fromJSON(file="../data_sets/captions.json") # HARDCODED!
  plotOutliersCaption <- paste("\\emph{No caption found for}", datasetId)
  if (datasetId %in% names(captions$plotOutliersCaptions)) {
    plotOutliersCaption <- captions$plotOutliersCaptions[datasetId]
  }
  return(as.character(plotOutliersCaption))
}
