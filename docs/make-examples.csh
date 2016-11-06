#! /bin/csh -f

echo "<h1> Examples </h1>"

foreach d ( ../examples/* )
    if (-d $d) then
	cd $d
	set currd = `echo $d | awk '{n=split($1,x,"/"); print x[n]}'`
	echo "<h2>$currd</h2>"
	echo "<p><ul>"
	foreach f ( *.py )
	    echo "  <li><a href=../examples/${currd}/${f}> $f</a>"
	end
	echo "</ul></p>"
	cd ..
    endif

end


