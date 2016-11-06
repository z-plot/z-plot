#! /bin/csh -f

# first, extract all docs from zplot.py 
./make-docs-single.py > /tmp/docs.out

# now, make each of the pages, including headers and such
set outfile = overview
m4 -DDEF_TITLE="Overview" header.html > ${outfile}.html
m4 -DDEF_ACTIVE_OVERVIEW='<li class="active"' -DDEF_ACTIVE_INDEX='<li' -DDEF_ACTIVE_DOCS='<li' -DDEF_ACTIVE_EXAMPLES='<li' body-start.html >> ${outfile}.html
cat in.${outfile}.html >> ${outfile}.html
cat body-end.html >> ${outfile}.html

set outfile = docs
m4 -DDEF_TITLE="Docs" header.html > ${outfile}.html
m4 -DDEF_ACTIVE_OVERVIEW='<li' -DDEF_ACTIVE_INDEX='<li' -DDEF_ACTIVE_DOCS='<li class="active"' -DDEF_ACTIVE_EXAMPLES='<li' body-start.html >> ${outfile}.html
cat in.${outfile}.html >> ${outfile}.html
cat body-end.html >> ${outfile}.html

set outfile = index
m4 -DDEF_TITLE="Zplot" header.html > ${outfile}.html
m4 -DDEF_ACTIVE_OVERVIEW='<li' -DDEF_ACTIVE_INDEX='<li class="active"' -DDEF_ACTIVE_DOCS='<li' -DDEF_ACTIVE_EXAMPLES='<li' body-start.html >> ${outfile}.html
cat in.${outfile}.html >> ${outfile}.html
cat body-end.html >> ${outfile}.html







