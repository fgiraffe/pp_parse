#!/bin/bash



testfiles=(
"tests/GZone_sequence_2017_1101_fcp.xml"
"tests/GZone_sequence_fcp.xml"
"tests/MB_Intvw_fcp.xml"
"tests/OneClip_fcp_xml.xml"
"tests/PP_Tutorial_Lesson_05_fcp.xml"
"tests/Smorg1_2017_1101_fcp.xml"
"tests/Smorg1_fcp_xml.xml"
"tests/my_GZ_2017_1101_fcp.xml"
"tests/my_GZ_fcp.xml"
"tests/yoavs_GZ_fcp.xml"
)

for i in "${testfiles[@]}"
do
	echo
	echo "-------------------------------------------------------"
	echo "Testing (dupes allowed): " "$i" 
#	python3 fcp_parse.py --showdupes "$i"
	python3 fcp_parse.py --showdupes --count "$i"
#	echo "-------------------------"
#	echo "Testing (NO dupes allowed): " "$i" 
#	python3 fcp_parse.py "$i"
#	python3 fcp_parse.py  --count "$i"
#	echo "-------------------------"
#	echo "Testing (brief mode): " "$i" 
#	python3 fcp_parse.py --brief "$i"
done
