#! /bin/csh -f

set script_dir=`dirname $0`
set zplot_dir=`cd $script_dir/../zplot && pwd`
if (! $?PYTHONPATH) then
    setenv PYTHONPATH $zplot_dir
else
    setenv PYTHONPATH $zplot_dir\:$PYTHONPATH
endif

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


