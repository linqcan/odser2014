library("xtable")
source("getCaptions.R")
source("getAxisLabels.R")

plotOneDimOutliers <- function(data,pathNoExt){
  # Creates and stores a plot of the data set.
  #

  inlierPCH <- 20
  outlierPCH <- 3
  if (is.data.frame(data)){
    # Remove NA from data set
    data <- na.omit(data)

    # creates an empty list
    pch.list <- rep(0, length(data[,1]))
    
    # sets the values in pch.list to x for outlier or o for inliner
    pch.list[data[,3] == "TRUE"]  <- outlierPCH
    pch.list[data[,3] == "FALSE"] <- inlierPCH
    
    # Modifying the filename
    pathNoExt <- gsub("labelled", "plotOutliers", pathNoExt)
    datasetId <- gsub("-plotOutliers", "", basename(pathNoExt))
    pdfFileName <- paste(pathNoExt, ".pdf", sep="")
    pdf(file=pdfFileName) 
    
    # Plot your graph  
    plot(data[,1], pch=pch.list, ylab=getYAxisLabel(datasetId), xlab=getXAxisLabel(datasetId))
    abline(a=mean(data[,1]) , b=0)
    tempFrame <- subset.matrix(data, data[,3] == FALSE)
    abline(a=mean(tempFrame[,1]), b=0, lty=2)

    # Write the file  
    dev.off()

    # Create figure Tex for plot
    createOutlierPlotTex(pathNoExt)

    print(paste("[plotOneDimOutliers] Output:", pdfFileName))
  }
  else {
    print("[plotOneDimOutliers] The data is not a data.frame object!")
  }
}

descriptiveStatistics <- function(data, pathNoExt){
  # Generating descriptive statistics
  # 

  # Filters the the outliers
  inliers  <- subset.matrix(data, data[,3] == FALSE)
  outliers <- subset(data, data[, 3] == TRUE)

  nrOutliers <- dim(outliers)[1]

  #Calculates the values for the table
  #Rounds the values with 3 decimals
  originalMean <- round(mean(data[,1], na.rm = TRUE),3)
  originalMedian <- round(median(data[,1], na.rm = TRUE),3)
  originalSTD <- round(sd(data[,1], na.rm = TRUE),3)

  modifiedMean <- round(mean(inliers[,1], na.rm = TRUE),3)
  modifiedMedian <- round(median(inliers[,1], na.rm = TRUE),3)
  modifiedSTD <- round(sd(inliers[,1], na.rm = TRUE),3)

  Set <- c( "Original" , "Modified")
  Mean <- c(originalMean, modifiedMean)
  Median <- c(originalMedian, modifiedMedian)
  StandardDeviation <- c(originalSTD, modifiedSTD)
  NumberOfOutliers <- c(nrOutliers, 0)

  dataFrame = data.frame(Set,Mean, Median, StandardDeviation, NumberOfOutliers)
  pathNoExt <- gsub("labelled", "descStatistics", pathNoExt)
 
  # Retrieve the table caption
  datasetId <- gsub("-descStatistics", "", basename(pathNoExt))
  tableCaption <- getTableCaption(datasetId)
  tableCaption <- paste("Descriptive statistics for dataset", tableCaption)

  # Write statistics to Latex
  tableName <- paste(pathNoExt, ".tex", sep="" )
  print(xtable(dataFrame, caption=tableCaption), label=paste("tab:", datasetId), type="latex", file=tableName, include.rownames=FALSE)

  # Write statistics to HTML
  tableName <- paste(pathNoExt, ".html", sep="" )
  print(xtable(dataFrame, caption=tableCaption), type="html", file=tableName, include.rownames=FALSE)
}

createOutlierPlotTex <- function(pathNoExt){
  # Creates the tex file for including the outlier plot
  #
  datasetId <- gsub("-plotOutliers", "", basename(pathNoExt))
  caption <- getPlotOutliersCaption(datasetId)
  pathPDF <- paste(pathNoExt, ".pdf", sep="" )
  fileNamePDF <- basename(pathPDF)
  pathTex <- paste(pathNoExt, ".tex", sep="" )
  sink(pathTex)
  cat("\\begin{figure}[H]")
  cat("\n")
  cat("\\centering")
  cat("\n")
  cat("\\includegraphics[width=0.7\\textwidth]{../results/") # HARDCODED result path!
  cat(fileNamePDF)
  cat("}")
  cat("\n")
  cat("\\caption{Figure showing dataset ")
  cat(caption)
  cat(", outliers are marked with a cross}")
  cat("\n")
  cat("\\end{figure}")
  sink()
}
  

# The script
#

args <- commandArgs(trailingOnly=TRUE)
hasHeader <- TRUE
n <- 0

if (length(args) != 1) {
  print("Error: Not enough arguments supplied!")
  print("Script requires one arguments; csvfile")
  quit(status=1)
} 

filePath <- args[1]

if (!file.exists(filePath)) {
  print(paste("File", FilePath, "does not exist!"))
  quit(status=1)
}

pathNoExt <- gsub(".csv", "", filePath) # Assuming .csv file

data <- read.csv(filePath, header=hasHeader)
plotOneDimOutliers(data, pathNoExt) 
descriptiveStatistics(data, pathNoExt)
