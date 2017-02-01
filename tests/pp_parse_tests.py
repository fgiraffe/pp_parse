#!/usr/bin/env python3

from nose.tools import *
from argparse import Namespace

import pp_parse

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


