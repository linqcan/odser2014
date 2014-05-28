# Performs a significance test on a labelled data set
sigTest <- function(dataLabelled, pathNoExt){

  dataWithOutliers    <- dataLabelled[,1]
  dataWithoutOutliers <- subset.matrix(dataLabelled, dataLabelled[,3] == FALSE)[,1]

  # Perform SW on both data sets
  dataWithOutliers.sw    <- shapiro.test(dataWithOutliers)
  dataWithoutOutliers.sw <- shapiro.test(dataWithoutOutliers)

  # Prepare stat for printing to file
  outlierStatDf   <- data.frame(unlist(dataWithOutliers.sw))
  noOutlierStatDf <- data.frame(unlist(dataWithoutOutliers.sw))

  # Create paths
  outlierPath   <- gsub("labelled", "swStatOutlier", pathNoExt)
  noOutlierPath <- gsub("labelled", "swStatNoOutlier", pathNoExt)
  outlierPath <- paste(outlierPath, ".tex", sep="")
  noOutlierPath <- paste(noOutlierPath, ".tex", sep="")

  # Create latex tables
  print(xtable(outlierStatDf), type="latex", file=outlierPath)
  print(xtable(noOutlierStatDf), type="latex", file=noOutlierPath)

  # Create HTML tables
  print(xtable(outlierStatDf), type="html", file=gsub(".tex", ".html", outlierPath))
  print(xtable(noOutlierStatDf), type="html", file=gsub(".tex", ".html", noOutlierPath))

  # Create a PDF with qqplot, histogram and density
  pdf(paste(gsub("labelled", "normPlotsOutliers", pathNoExt), ".pdf", sep=""))
  hist(dataWithOutliers, prob=TRUE)
  lines(density(dataWithOutliers))
  qqnorm(dataWithOutliers)
  qqline(dataWithOutliers)
  dev.off()

  pdf(paste(gsub("labelled", "normPlotsNoOutliers", pathNoExt), ".pdf", sep=""))
  hist(dataWithoutOutliers, prob=TRUE)
  lines(density(dataWithoutOutliers))
  qqnorm(dataWithoutOutliers)
  qqline(dataWithoutOutliers)
  dev.off()


  # Perform students t-test (pair wise)
  studentStat <- t.test(dataWithOutliers, dataWithoutOutliers, paired=FALSE, na.action=na.omit)

  # Perform Wilcoxon (pair wise)
  wilcoxonStat <- wilcox.test(dataWithOutliers, dataWithoutOutliers, paired=FALSE, na.action=na.omit)

  # Prepare stat for printing to file
  studentDf  <- data.frame(unlist(studentStat))
  wilcoxonDf <- data.frame(unlist(wilcoxonStat))

  # Create paths
  studentPath  <- gsub("swStatOutlier", "studentStat", outlierPath)
  wilcoxonPath <- gsub("swStatOutlier", "wilcoxonStat", outlierPath)

  # Create Latex tables
  print(xtable(studentDf), type="latex", file=studentPath)
  print(xtable(wilcoxonDf), type="latex", file=wilcoxonPath)

  # Create HTML tables
  print(xtable(studentDf), type="html", file=gsub(".tex", ".html", studentPath))
  print(xtable(wilcoxonDf), type="html", file=gsub(".tex", ".html", wilcoxonPath))
}


args <- commandArgs(trailingOnly=TRUE)

if (length(args) != 1) {
  print("Error: Not enough arguments supplied!")
  print("Script requires one arguments; csvfile")
  quit(status=1)
} 

filePath <- args[1]

pathNoExt <- gsub(".csv", "", filePath) # Assuming .csv file

if (!file.exists(filePath)) {
  print(paste("File", filePath, "does not exist!"))
  quit(status=1)
}

library("xtable")
data <- read.csv(filePath, header=TRUE)
sigTest(data,pathNoExt) 
