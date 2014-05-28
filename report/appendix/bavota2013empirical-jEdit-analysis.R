# Script for further analysis of "An Empirical Study on the Developers’ Perception of Software Coupling"
# Recreation of table three in Bavota et al.(2013)
#
#References
#Gabriele Bavota, Bogdan Dit, Rocco Oliveto, Massimiliano Di Penta, Denys
#Poshyvanyk, and Andrea De Lucia. An empirical study on the developers’
#perception of software coupling. In Proceedings of the 2013 International
#Conference on Software Engineering, pages 692–701. IEEE Press, 2013.
###########################

# Input, in *.modified outliers are removed 
`semanticLow.labelled` <- read.csv("../../results/bavota2013empirical-jEdit-semanticLow-labelled.csv")
semanticLow.modified= semanticLow.labelled$Data[semanticLow.labelled$Outlier == "FALSE"]
semanticLow.orginal= semanticLow.labelled$Data

`structuralLow.labelled` <- read.csv("../../results/bavota2013empirical-jEdit-structuralLow-labelled.csv")
structuralLow.modified= structuralLow.labelled$Data[structuralLow.labelled$Outlier == "FALSE"]
structuralLow.orginal= structuralLow.labelled$Data


`dynamicLow.labelled` <- read.csv("../../results/bavota2013empirical-jEdit-dynamicLow-labelled.csv")
dynamicLow.modified= dynamicLow.labelled$Data[dynamicLow.labelled$Outlier == "FALSE"]
dynamicLow.orginal= dynamicLow.labelled$Data

`logicalLow.labelled` <- read.csv("../../results/bavota2013empirical-jEdit-logicalLow-labelled.csv")
logicalLow.modified= logicalLow.labelled$Data[logicalLow.labelled$Outlier == "FALSE"]
logicalLow.orginal= logicalLow.labelled$Data

# Wilcoxon test also known as Wilcoxon rank-sum test
#P1
p1.modified <- 	round((wilcox.test(semanticLow.modified,structuralLow.modified))$p.value,4)
p1.orginal <- round((wilcox.test(semanticLow.orginal,structuralLow.orginal))$p.value,4)

#T2
p2.modified <- round((wilcox.test(semanticLow.modified,dynamicLow.modified))$p.value,4)
p2.orginal <- round((wilcox.test(semanticLow.orginal,dynamicLow.orginal))$p.value,4)

#T3
p3.modified <- round((wilcox.test(semanticLow.modified,logicalLow.modified))$p.value,4)
p3.orginal <- round((wilcox.test(semanticLow.orginal,logicalLow.orginal))$p.value,4)

#T4
p4.modified <- round((wilcox.test(structuralLow.modified,dynamicLow.modified))$p.value,4)
p4.orginal <- round((wilcox.test(structuralLow.orginal,dynamicLow.orginal))$p.value,4)

#T5
p5.modified <- round((wilcox.test(structuralLow.modified,logicalLow.modified))$p.value,4)
p5.orginal <-  round((wilcox.test(structuralLow.orginal,logicalLow.orginal))$p.value,4)

#T6
p6.modified <- round((wilcox.test(dynamicLow.modified,logicalLow.modified))$p.value,4)
p6.orginal <- round((wilcox.test(dynamicLow.orginal,logicalLow.orginal))$p.value,4)

a <- c("Comparison", "semanticLow-structuralLow","semanticLow-dynamicLow","semanticLow-logicalLow","structuralLow-dynamicLow","structuralLow-logicalLow","dynamicLow-logicalLow")
b <- c("Modified", p1.modified, p2.modified, p3.modified, p4.modified, p5.modified, p6.modified)
c <- c("Orginal", p1.orginal, p2.orginal, p3.orginal, p4.orginal, p5.orginal, p6.orginal)
df = data.frame(a,b,c)
write.table(df)
""