lociLabelOutliers <- function(data, stds) {
  # Column 4 should be the MDEF score
  sMDEF <- sd(data[,length(data)])
  out <- data
  out$Outlier <- apply(out, 1, function(row) (row[length(data)] > stds*sMDEF))
  return(out)
}

args <- commandArgs(trailingOnly=TRUE)

if (length(args) < 2) {
  print("Error: Not enough arguments supplied!")
  print("Script requires two arguments; csvfile and number of standard deviations.")
  quit(status=1)
}

filename <- args[1]
n <- as.double(args[2])

if (is.na(n)) {
  print("Number of standard deviations has to be a number!")
  quit(status=1)
}


if (!file.exists(filename)) {
  print(paste("File", filename, "does not exist!"))
  quit(status=1)
}
output.filepath <- gsub("parsed", "labelled", filename)

data <- read.csv(filename, header=FALSE)
output.data <- lociLabelOutliers(data, n)
print(output.data)
print(output.filepath)

if (file.exists(output.filepath)) {
  print(paste("Overwriting", output.filepath))
}
write.csv(output.data, file=output.filepath, row.names=FALSE)
