#!/usr/bin/env python3

from nose.tools import assert_equal
from argparse import Namespace
import json

import pp_parse

TEST_FILE_PATH = "tests/pp_parse_test_data.json"

global test_file
global test_file_data


def setup():
    global test_file
    global test_file_data
    with open(TEST_FILE_PATH, encoding='utf-8') as test_file:
        test_file_data = json.loads(test_file.read())


def teardown():
    test_file.close()


def test_one_file():
    args = Namespace(count=True)
    file_list = pp_parse.print_media_paths(
                                    "tests/PP_Tutorial_Lesson_05.prproj", args)
    assert_equal(len(file_list), 33)

    args = Namespace()
    file_list = pp_parse.print_media_paths("tests/OneClip.prproj", args)
    assert_equal(len(file_list), 1)


def test_all_files():
    args = Namespace()
    for a_test_case in test_file_data:
        file_list = pp_parse.print_media_paths(a_test_case["filename"], args)
        assert_equal(len(file_list), a_test_case["UniqueFiles"])
