#! /bin/csh -f

@ count = 1
foreach dir ( * )
    if (-d $dir) then
	cd $dir
	foreach type ( $* )
	    foreach py ( *.py )
		echo "$count ${dir}/${py} $type"
		@ count += 1
		./${py} $type
	    end
	end
	cd ..
    endif
end


