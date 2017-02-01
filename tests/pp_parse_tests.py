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


def test_file_from_list():
    # from http://nose.readthedocs.io/en/latest/writing_tests.html
     for a_test_case in test_file_data:
        yield check_results, a_test_case["filename"], a_test_case["UniqueFiles"]


def check_results(file_name, correct_results):
    args = Namespace()
    file_list = pp_parse.print_media_paths(file_name, args)
    assert_equal(len(file_list), correct_results)
