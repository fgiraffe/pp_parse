#!/usr/bin/env python3

from nose.tools import assert_equal
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
        yield check_results_nodupes, a_test_case["filename"],\
                                     a_test_case["UniqueFiles"]

    for a_test_case in test_file_data:
        yield check_results_dupes, a_test_case["filename"],\
                                     a_test_case["FileCountFCPWithDupes"]


def check_results_nodupes(file_name, correct_results):
    file_list = pp_parse.print_media_paths(file_name,
                                           only_count=False,
                                           leaf_pathnames=False,
                                           show_duplicate_files=False)
    assert_equal(len(file_list), correct_results)


def check_results_dupes(file_name, correct_results):
    file_list = pp_parse.print_media_paths(file_name,
                                           only_count=False,
                                           leaf_pathnames=False,
                                           show_duplicate_files=True)
    assert_equal(len(file_list), correct_results)
