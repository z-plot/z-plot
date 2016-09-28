#! /bin/csh -f

@ count = 1
foreach dir ( * )
    if (-d $dir) then
	cd $dir
	foreach py ( *.py )
	    echo "$count $py"
	    @ count += 1
	    ./${py}
	end
	cd ..
    endif
end


