#!/usr/bin/python3

OUTPUT_FILE_NAME = 'tests/pp_parse_test_data.json'

import json

test_cases = [
    {"filename": "PP_Tutorial_Lesson_05.prproj",
    "TotalFiles": 36,
    "MovieFiles": 12, 
    "ImageFiles": 21,
    "CorrectAnswer": 36},

     {"filename": "OneClip_fcp_xml.xml",
    "TotalFiles": 2,
    "MovieFiles": 2, 
    "ImageFiles": 0,
    "CorrectAnswer": 2},

    {"filename": "Smorg1_fcp_xml.xml",
    "TotalFiles": 2,
    "MovieFiles": 1, 
    "ImageFiles": 1,
    "CorrectAnswer": 2},

    {"filename": "GZone_sequence_2017_1101_fcp.xml",
    "TotalFiles": 1069,
    "MovieFiles": 1069, 
    "ImageFiles": 0,
    "CorrectAnswer": 1069},

    {"filename": "my_GZ_2017_1101_fcp.xml",
    "TotalFiles": 1191,
    "MovieFiles": 1073, 
    "ImageFiles": 117,
    "CorrectAnswer": 1191},

#    {"filename": "my_GZ.prproj",
#    "TotalFiles": 1191,
#     "MovieFiles": 1073, 
#    "ImageFiles": 117,
#    "CorrectAnswer": 1191},
#
#    {"filename": "MB_Intvw.prproj",
#    "TotalFiles": 126,
#    "MovieFiles": 126, 
#    "ImageFiles": 0,
#    "CorrectAnswer": 126},
#
#    {"filename": "GZone_sequence_prproj.xml",
#    "TotalFiles": 1069,
#    "MovieFiles": 1069, 
#    "ImageFiles": 0,
#    "CorrectAnswer": 1069},
#
#    {"filename": "yoavs_GZ.prproj",
#    "TotalFiles": 131,
#    "MovieFiles": 66, 
#    "ImageFiles": 63,
#    "CorrectAnswer": 131},

]

with open(OUTPUT_FILE_NAME, 'w') as outfile:
    json.dump(test_cases, outfile, encoding='utf-8', 
            sort_keys = True, indent = 4, separators=(',', ':'))


# test 
#with open(OUTPUT_FILE_NAME, "r") as infile:
#    list = json.load(infile)
#    a_case = list[0]
#    print(a_case["filename"])
    
