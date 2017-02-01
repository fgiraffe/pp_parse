#!/usr/bin/env python3

from nose.tools import *
from argparse import Namespace
import json

import pp_parse

TEST_FILE_DATA = "tests/pp_parse_test_data.json"

def setup():
    print ("SETUP!")

def teardown():
    print ("TEAR DOWN!")

def test_basic():
    print ("I RAN!")

def test_one_file():
    args = Namespace(count=True)
    file_list = pp_parse.print_media_paths("tests/PP_Tutorial_Lesson_05.prproj", args)
    assert_equal(len(file_list), 33)

    args = Namespace()
    file_list = pp_parse.print_media_paths("tests/OneClip.prproj", args)
    assert_equal(len(file_list), 1)

def test_all_files():
    args = Namespace()

    with open(TEST_FILE_DATA, encoding='utf-8') as json_fp:
        data = json.loads(json_fp.read())

    for a_test_case in data:
        file_list = pp_parse.print_media_paths(a_test_case["filename"], args)
        assert_equal(len(file_list), a_test_case["UniqueFiles"])
