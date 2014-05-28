
#
# R-script to check  and install dependencies for dependencies 
#


# xtable Used by pipeline and 



# repo used for downloading R packages
# More repos available at http://cran.r-project.org/mirrors.html
# xtable used by pipeline
cran_repo = "http://cran.us.r-project.org"
con <- file("stdin")
packages <- c('xtable', 'rjson', 'effsize')
for (i in packages){
    if(!is.element(i, installed.packages()[,1])) {
        cat(sprintf("[Init Pipeline] Do you wish to install %s? (y/n)", i))
        answer <- readLines(con,1)
        if(answer == "y" || answer == "Y"){
            cat(sprintf("[Init Pipeline] Installing %s \n" , i))
            install.packages(i, repos=cran_repo)
        }else {cat(sprintf( "[Init Pipeline] Aborting installation of %s \n" , i))}
    }else {cat(sprintf("[Init Pipeline] R package %s: OK \n", i))}
}

close(con)