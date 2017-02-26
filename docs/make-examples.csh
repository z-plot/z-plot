#! /bin/csh -f

echo "<h1> Examples </h1>"

echo ""
echo "<p> Below are a number of examples provided with zplot. If you add new and interesting types of graphs, please add them (via github). For each graph, there is usually a script that generates the graph, a data file (sometimes a few), and a resulting EPS or SVG file that shows the output (or both).</p>"
echo ""

set nonomatch

foreach d ( ../examples/* )
    if (-d $d) then
	cd $d
	set currd = `echo $d | awk '{n=split($1,x,"/"); print x[n]}'`

	echo "<h2>$currd</h2>"
	echo "<p><ul>"
	foreach f ( *.py )
	    set base = `echo $f | awk '{n=split($1,x,"."); print x[1]}'`
	    # echo "b" $base

	    set target_base = "../examples/${currd}/${base}"
	    # echo "tb" $target_base
	    # echo -n "stuff " 
	    # echo ../${target_base}*.data
	    # echo ""

	    echo -n " <li> ${base}:"

	    if (-e ../${target_base}.py) then
		echo -n "<a href=../examples/${currd}/${base}.py> script</a>"
	    endif 
	    foreach dfile (../${target_base}*data) 
		# this is an ugly hack to peel off the first '../' of each dfile
		set dfile2 = `echo $dfile | awk '{print substr($0,4,length($0));}'`
		echo -n "<a href=$dfile2> data</a>"
	    end
	    echo " &nbsp; &nbsp; output:"
	    if (-e ../${target_base}.eps) then
		echo -n "<a href=../examples/${currd}/${base}.eps> eps</a>"
	    endif 
	    if (-e ../${target_base}.pdf) then
		echo -n "<a href=../examples/${currd}/${base}.pdf> pdf</a>"
	    endif 
	    if (-e ../${target_base}.svg) then
		echo -n "<a href=../examples/${currd}/${base}.svg> svg</a>"
	    endif 
	    echo " </li>"
    
	end
	echo "</ul></p>"
	cd ..
    endif

end


