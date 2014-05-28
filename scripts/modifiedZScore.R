#########################
# Function declarations
#
# This version of the MZS is implemented as described in (Garcia, 2012) and
# uses the same alternative method as SPSS (2007) to calculate the score if MAD equals zero.
############
# References
# Francisco Augusto Alcaraz Garcia. Tests to identify outliers in data series.
# Pontifical Catholic University of Rio de Janeiro, Industrial Engineering De-
# partment, Rio de Janeiro, Brazil, 2012.
#
# IBM SPSS. IBM SPSS modified z score, 2007. URL http://goo.gl/oikOjr
#
#########################
MZS <- function(indata) {

  data    <- unlist(indata, use.names=FALSE)
  the_mad <- mad(data, na.rm=TRUE)
  the_sd  <- sd(data, na.rm=TRUE)
  the_median <- median(data, na.rm=TRUE)
  result  <- vector()
  alternate <- FALSE
  if (the_mad == 0) {
    alternate <- TRUE
    the_mad <- meanAD(data)
  }

  for (i in 1:length(data)) {
    if (!is.na(data[i])) {
      if (alternate == TRUE) {
        num_med <- (data[i] - the_median) / (1.253314 * the_mad)
      } else {
        num_med <- abs(( 0.6745*(data[i] - the_median)) / the_mad)
      }
      result <- append(result, num_med)
    } else {
      result <- append(result, NA)
    }
  }
  return(result)
}

MZSLabelOutliers <- function(indata, score, sd) {
  resultFrame <- data.frame(indata, score, (sd<score))
  colnames(resultFrame) <- c("Data" , "Score", "Outlier")
  resultFrame <- na.omit(resultFrame)
  return(resultFrame)
}

meanAD <- function(data) {
  print("Using alternative MAD calculation")
  data <- data[!is.na(data)] # Remove NA
  the_mean <- mean(data)
  num <- length(data)
  the_sum <- vector()
  for (i in 0:num) {
    the_sum <- append(the_sum,  abs(data[i]-the_mean))
  }
  return(sum(the_sum) / num)
}

#########################
# The script
args <- commandArgs(trailingOnly=TRUE)

hasHeader <- FALSE
n <- 0

if (length(args) < 1) {
  print("Error: Not enough arguments supplied!")
  print("Script requires one arguments; csvfile")
  quit(status=1)
} else if (length(args) < 2) {
  n <- 3.5
  print("Number of standard deviations was set to 3.5 according to:")
  print("B. Iglewicz; D.C. Hoaglin (1993). How to Detect and Handle Outliers.")
}

if (length(args) > 1) {
  n <- as.double(args[2])
}

if (length(args) > 2) {
  if (args[3] == "FALSE") {
    hasHeader <- FALSE
  } else if (args[3] == "TRUE") {
    hasHeader <- TRUE
  } else {
    print(paste("Unknown header option:", args[3]))
    quit(status=1)
  }
}

print(paste("n:", n))
print(paste("header:", hasHeader))

filename <- args[1]

if (is.na(n)) {
  print("Number of standard deviations has to be an integer!")
  quit(status=1)
}

path <- filename

if (!file.exists(path)) {
  print(paste("File", path, "does not exist!"))
  quit(status=1)
}

data <- read.csv(path, header=hasHeader)
output.data <- MZSLabelOutliers(data, MZS(data), n)
output.filepath <- gsub("original", "labelled", filename)

print(output.data)
print(output.filepath)

if (file.exists(output.filepath)) {
  print(paste("Overwriting", output.filepath))
}
write.csv(output.data, file=output.filepath, row.names = FALSE)
