#!/bin/bash
# ./ppxmlconvert.sh PPXMLTest.prproj
# Adobe Premiere Pro CC stores project files as gzipped xml
# This script copies, unpacks and renames a given project file
# so it can be easily read with a text editor.


#if something fails, abort
set -e
#set -x

if [ $# -ne 1 ]; then
    echo
	echo $0: usage: ppxmlconvert.sh premProProjectFile.prproj
	echo "# takes a native format Premier Pro project file and"
	echo "# unpacks it into an xml text file."
    exit 1
fi

function main {
	file_full_pathname=$1
	file_leaf=`echo "$file_full_pathname" | awk '{sub(/.*\//,x)}1'`
	file_path=`dirname "$file_full_pathname"`

	cp -i -p "$file_full_pathname" /tmp
	# add .gz suffix, or gunzip complains
	mv /tmp/"$file_leaf"  /tmp/"$file_leaf".gz
	gunzip /tmp/"$file_leaf".gz

	# file is unzipped, but has original name. 
	# add .xml suffix to be clear what it is 
	mv  /tmp/"$file_leaf" /tmp/"$file_leaf".xml
	
	# copy it back to wherever we started from and clean up
	cp -i -p  /tmp/"$file_leaf".xml "$file_path"/
	echo "#Created  "$file_path"/"$file_leaf".xml"
	rm  /tmp/"$file_leaf".xml 

}

if [ -r "$1" ]; then
	main "$1"
else
   echo "The file '$1' does not exist or is not readable"
fi
