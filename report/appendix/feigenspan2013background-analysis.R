# This script requires the library "effsize"
library(effsize)

# Load data for RH1 and RH2
`s1color` <- read.table("../../results/feigenspan2013background-s1color-original.csv", quote="\"")
s1color = s1color$V1
`s1ifdef.labelled` <- read.csv("../../results/feigenspan2013background-s1ifdef-labelled.csv")
s1ifdef.modified= s1ifdef.labelled$Data[s1ifdef.labelled$Outlier == "FALSE"]

`m1color` <- read.table("../../results/feigenspan2013background-m1color-original.csv", quote="\"")
m1color = m1color$V1
`m1ifdef.labelled` <- read.csv("../../results/feigenspan2013background-m1ifdef-labelled.csv")
m1ifdef.modified = m1ifdef.labelled$Data[m1ifdef.labelled$Outlier=="FALSE"]

`m2color` <- read.table("../../results/feigenspan2013background-m2color-original.csv", quote="\"")
m2color = m2color$V1
`m2ifdef.labelled` <- read.csv("../../results/feigenspan2013background-m2ifdef-labelled.csv")
m2ifdef.modified = m2ifdef.labelled$Data[m2ifdef.labelled$Outlier=="FALSE"]

# Normality test, significance test and effect size calculation
shapiro.test(s1color)
shapiro.test(s1ifdef.modified)
wilcox.test(s1color, s1ifdef.modified)
cliff.delta(s1color, s1ifdef.modified)

shapiro.test(m1color)
shapiro.test(m1ifdef.modified)
t.test(m1color, m1ifdef.modified)
cliff.delta(m1color, m1ifdef.modified)

shapiro.test(m2color)
shapiro.test(m2ifdef.modified)
wilcox.test(m2color, m2ifdef.modified)
cliff.delta(m2color, m2ifdef.modified)


# Load data for RH4
`m1color.performance.original` <- read.table("../../results/feigenspan2013background-m1color-performance-original.csv", quote="\"")
m1color.performance.original = m1color.performance.original$V1
m1ifdef.performance.labelled <- read.csv("../../results/feigenspan2013background-m1ifdef-performance-labelled.csv")
m1ifdef.performance.modified = m1ifdef.performance.labelled$Data[m1ifdef.performance.labelled$Outlier == "FALSE"]

`m2color.performance.original` <- read.table("../../results/feigenspan2013background-m2color-performance-original.csv", quote="\"")
m2color.performance.original = m2color.performance.original$V1
`m2ifdef.performance.labelled` <- read.csv("../../results/feigenspan2013background-m2ifdef-performance-labelled.csv")
m2ifdef.performance.modified = m2ifdef.performance.labelled$Data[m2ifdef.performance.labelled$Outlier == "FALSE"]

`m3color.performance.original` <- read.table("../../results/feigenspan2013background-m3color-performance-original.csv", quote="\"")
m3color.performance.original = m3color.performance.original$V1
`m3ifdef.performance.labelled` <- read.csv("../../results/feigenspan2013background-m3ifdef-performance-labelled.csv")
m3ifdef.performance.modified = m3ifdef.performance.labelled$Data[m3ifdef.performance.labelled$Outlier == "FALSE"]

# Normality and significance test
shapiro.test(m1color.performance.original)
shapiro.test(m1ifdef.performance.modified)
wilcox.test(m1color.performance.original, m1ifdef.performance.modified)

shapiro.test(m2color.performance.original)
shapiro.test(m2ifdef.performance.modified)
wilcox.test(m2color.performance.original, m2ifdef.performance.modified)

shapiro.test(m3color.performance.original)
shapiro.test(m3ifdef.performance.modified)
wilcox.test(m3color.performance.original, m3ifdef.performance.modified)
