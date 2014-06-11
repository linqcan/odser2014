# Unsupervised Outlier Detection in Software Engineering
This is a companion repository to the master thesis "Unsupervised Outlier Detection in Software Engineering" by Henrik Larsson and Erik Lindqvist.

After cloning this repository it is possible to re-run the analysis and compile the report.

## Requirements
The following software requirements must be fulfilled in order to run the analysis and compile the report.

* Linux or OS X (with bash)
* Python 2.7
* R 2.15.1 or greater (required packages are listed below)
  * xtables
  * rjson
* TEX Live 2013 (required packages are listed below)
  * caption
  * float
  * graphicx
  * hyperref
  * longtable
  * natbib
  * pdflscape
  * subcaption
  * tabu
  * tikz
* ELKI 0.6.0 (for multi-dimensional data sets)
  * OpenJDK 7

ELKI 0.6.0 needs to be downloaded from the authors [web site](http://elki.dbs.ifi.lmu.de/wiki/Releases) and the *executeable archive*/jar-file put in the folder *bin/*. This can be done manually or by issuing `bash scripts/installELKI.sh` from the top folder.

## Usage
### First run
* Clone this repository to your local drive
* Run the init script to check if the dependencies are met by issuing the command `./init`
* When all dependencies are met, to perform the analysis and compile the report issue the command `./generate all`
* Results can be found in the *results/* folder.

### Browsing the results
To browse the results more easily, open the file *results/index.html* in your web browser. This will give you an index from which you can browse the results of all data sets containing outliers.

### Changing parameters for the outlier detection
The parameters for Modified Z Score (MZS) and LOCI can be changed by editing the file *config.json*. Refer to the algorithms original documentation for help with the different parameters.

### Using the pipeline with your own data set
Data sets handled by the pipeline must be in the CSV format and must **not** contain any headers. Furthermore, the naming convention for datasets is:

*study_identifier-optional_set_identifier*.csv

For example, *foo2014bar-effort*.csv

The easiest way to add your own data set is to create a folder in *data_sets* with your study identifier as a name and the put all of your data sets in this folder (named according to the convention above). Then run `./generate analysis` in the repository's top folder.

The pipeline can be run without invoking the generate script. The expected arguments for the pipeline is either a data set or a folder containing data sets. The folder is scanned recursively. To invoke the pipeline, move to the *scripts* folder and execute the following:

`./pipeline.py /home/foo/foo2014bar-effort.csv`

or

`./pipeline.py /home/foo/my_data_sets`

**Note** that the pipeline needs to be run from the folder *scripts*!

Again, we like to remind you to name your data sets according to the convetion presented previously!

## Result files generated
The pipeline produces numerous result files. Each file has the *study_identifier* and *set_identifier* in the file name before the result file suffix is added. Below is a short description of each.

**-descStatistics.html** Descriptive statistics for the data set in HTML format.

**-descStatistics.tex** Descriptive statistics for the data set in LateX format.

**-labelled.csv** Data set with outliers labelled after MZS has been applied.

**-normPlotsNoOutliers.pdf** Normality plot for data set without outliers.

**-normPlotsOutliers.pdf** Normality plot for data set with outliers.

**-original.csv** The original data set.

**-plotOutliers.pdf** Plot with outliers marked out.

**-plotOutliers.tex** LateX code for including the outlier plot in a LateX document.

**-studentStat.html** Statistics from a Students t-test (Welch's t-test) comparing the data set before and after outliers were removed. HTML format.

**-studentStat.tex** Statistics from a Students t-test (Welch's t-test) comparing the data set before and after outliers were removed. LateX format.

**-swStatNoOutlier.html** Shapiro-Wilks statistics for the data set after outliers were removed. HTML format.

**-swStatNoOutlier.tex** Shapiro-Wilks statistics for the data set after outliers were removed. LateX format.

**-swStatOutlier.html** Shapiro-Wilks statistics for the data set before outliers were removed. HTML format.

**-swStatOutlier.tex** Shapiro-Wilks statistics for the data set after outliers were removed. LateX format.

**-wilcoxonStat.html** Statistics from a Wilcoxon test (Mann-Whitney U) comparing the data set before and after outliers were removed. HTML format.

**-wilcoxonStat.tex** Statistics from a Wilcoxon test (Mann-Whitney U) comparing the data set before and after outliers were removed. LateX format.

## Reference for tests used in R

* `t.test` for parametric significance testing
* `wilcox.test` for non-parametric significance testing
* `shapiro.test` for normality testing

## Data sets used
The data sets used in this study can be found in the folder *data_sets*. The data sets are credited as follows:

**arcuri2013parameter** - Andrea Arcuri and Gordon Fraser. Parameter tuning or default values? an empirical investigation in search-based software engineering. *Empirical Software Engineering, 18(3):594–623, 2013.*

**bavota2013empirical** - Gabriele Bavota, Bogdan Dit, Rocco Oliveto, Massimiliano Di Penta, Denys Poshyvanyk, and Andrea De Lucia. An empirical study on the developers’ perception of software coupling. In *Proceedings of the 2013 International Conference on Software Engineering*, pages 692–701. IEEE Press, 2013.

**feigenspan2013background** - Janet Feigenspan, Christian K ̈astner, Sven Apel, Jörg Liebig, Michael Schulze, Raimund Dachselt, Maria Papendieck, Thomas Leich, and Gunter Saake. Do background colors improve program comprehension in the# ifdef hell? *Empirical Software Engineering*, 18(4):699–745, 2013.

**herbold2013training** - Steffen Herbold. Training data selection for cross-project defect prediction. In *Proceedings of the 9th International Conference on Predictive Models in Software Engineering*, page 6. ACM, 2013.

**itkonen2013test** - Juha Itkonen and Mika V Mäntylä. Are test cases needed? replicated comparison between exploratory and test-case-based software testing. *Empirical Software Engineering*, pages 1–40, 2013.

**lee2013drag** - Yun Young Lee, Nicholas Chen, and Ralph E Johnson. Drag-and-drop refactoring: intuitive and efficient program transformation. In *Proceedings of the 2013 International Conference on Software Engineering*, pages 23–32. IEEE Press, 2013.

**nam2013transfer** - Jaechang Nam, Sinno Jialin Pan, and Sunghun Kim. Transfer defect learning. In *Proceedings of the 2013 International Conference on Software Engineering*, pages 382–391. IEEE Press, 2013.

**parnin2013adoption** - Chris Parnin, Christian Bird, and Emerson Murphy-Hill. Adoption and use of java generics. *Empirical Software Engineering*, 18(6):1047–1089, 2013.

**sawadsky2013reverb** - Nicholas Sawadsky, Gail C Murphy, and Rahul Jiresal. Reverb: recommending code-related web pages. In *Proceedings of the 2013 International Conference on Software Engineering*, pages 812–821. IEEE Press, 2013.

**shar2013mining** - Lwin Khin Shar, Hee Beng Kuan Tan, and Lionel C Briand. Mining sql injection and cross site scripting vulnerabilities using hybrid program analysis. In *Proceedings of the 2013 International Conference on Software Engineering*, pages 642–651. IEEE Press, 2013.

**wang2013improving** - Jinshui Wang, Xin Peng, Zhenchang Xing, and Wenyun Zhao. Improving feature location practice with multi-faceted interactive exploration. In *Proceedings of the 2013 International Conference on Software Engineering*, pages 762–771. IEEE Press, 2013.

### Data sets not available
Due to missing consent from the authors the data sets from the following papers are not available:

**minku2013analysis** - Leandro L Minku and Xin Yao. An analysis of multi-objective evolutionary algorithms for training ensemble models based on different performance measures in software effort estimation. In *Proceedings of the 9th International Conference on Predictive Models in Software Engineering*, page 8. ACM, 2013.

**song2013impact** - Liyan Song, Leandro L Minku, and Xin Yao. The impact of parameter tuning on software effort estimation using learning machines. In *Proceedings of the 9th International Conference on Predictive Models in Software Engineering*, page 9. ACM, 2013.
