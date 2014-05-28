abodLabelOutliers <- function(data, n) {
  # data is a data frame
  # n is the number of outliers we want to label
  out <- data
  i <- 0
  rows <- dim(data)[1]
  outliers <- vector()
  for(j in 1:rows) {
    outlier <- FALSE
    if (i < n) {
      outlier <- TRUE
      i <- i + 1
    }
    outliers <- append(outliers, outlier)
  }
  out$Outlier <- outliers
  return(out)
}

args <- commandArgs(trailingOnly=TRUE)

if (length(args) < 2) {
  print("Error: Not enough arguments supplied!")
  print("Script requires two arguments; csvfile and number of outliers")
  quit(status=1)
}

filename <- args[1]
n <- as.double(args[2])

if (is.na(n)) {
  print("Number of outliers has to be a number!")
  quit(status=1)
}

path <- paste(getwd(), "/", filename, sep="")

if (!file.exists(path)) {
  print(paste("File", path, "does not exist!"))
  quit(status=1)
}

data <- read.csv(path, header=FALSE)

output.data <- abodLabelOutliers(data, n)
output.filepath <- paste(getwd(), "/", "labelled-", filename, sep="")

print(output.data)
print(output.filepath)

if (file.exists(output.filepath)) {
  print(paste("Overwriting", output.filepath))
}
write.csv(output.data, file=output.filepath, row.names=FALSE)
