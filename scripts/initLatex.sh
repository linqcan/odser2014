 #!/bin/bash   

declare -a Packages=('caption.sty' 'float.sty' 'hyperref.sty' 'longtable.sty' 'natbib.sty' 'pdflscape.sty' 'subcaption.sty' 'tabu.sty' 'tikz.sty');

for i in "${Packages[@]}"
do
    kpsewhich $i > /dev/null
    status=$?
    if [ $status -ne 0 ]; then
      echo [Init Pipeline] Latex package "$i" missing 
    else
      echo [Init Pipeline] Latex package "$i": OK
    fi
done







