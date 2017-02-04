#!/usr/bin/env python3
""" pp_parse.py

A simple python module to parse Adobe Premiere Pro CC project files,
and print out all the media paths that the project references.
Tested with Adobe Premiere Pro CC 2015.4

Example:
        $ python pp_parse.py myAwesomeMovie.prproj

Created by Frank Giraffe fgiraffe@gmail.com, January 29, 2017

Copyright (c) 2017 [Frank Giraffe]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
                                  ----
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

    Why does this script exist?

    The Premiere Pro file format is officially undocumented.
    But AFAICT there is no easy way to just extract the files
    that a project references as TEXT. Exporting a "Batch List" is a
    little ugly, and does not offer the full path.
    You can export FCP XML and grep that, but that is an extra step.

    so what is a "good" media chunk inside a Premiere Pro project file?
    To be good it has to:
        - have a ObjectUID attribute. Not sure what the other Media types
            are but they have a ObjectURefs instead.
        - not be a proxy (no <IsProxy> chunk, or set to false)
        - to have a legit looking <ContentAndMetadataState> chunk, namely
            one whose value is not CMS_STATE_NOT_REAL_MEDIA_ID.
            This handles titles, subtitles, slugs, bars and tone,
            solid color mattes, etc.
"""

import xml.sax
import argparse
import os.path
import gzip
import defusedxml.sax

HELP_STRING = 'Reads an un-gzipped Premiere Pro project file and prints \
                    the media path strings.'


CMS_STATE_NOT_REAL_MEDIA_ID = "00000000-0000-0000-0000-000000000000"


class MovieHandler(xml.sax.ContentHandler):
    """
    From https://www.tutorialspoint.com/python/python_xml_processing.htm
    """
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.current_data = ""
        self.path = ""
        self.media_refs_list = []

        self.in_media_chunk = False
        self.is_proxy = False
        self.proxy_value = ""
        self.content_media_state = ""

    # Call when an element starts
    def startElement(self, tag, attributes):
        if tag == "Media":
            if "ObjectUID" in attributes:
                # if Media tag has a ObjectUID we are interested in it.
                self.in_media_chunk = True
                # self.objID = attributes["ObjectUID"]
            else:
                # this skips the bogus Media tags with ObjectURefs attached
                pass
        self.current_data = tag

    # Call when an elements ends
    def endElement(self, name):
        if self.current_data == "IsProxy":
            if self.proxy_value == "true":
                self.is_proxy = True
            else:
                self.is_proxy = False

        if name == "Media" and self.in_media_chunk:
            if self.is_proxy is False and \
               self.content_media_state != CMS_STATE_NOT_REAL_MEDIA_ID:
                self.media_refs_list.append(self.path)
            self.content_media_state = ""
            self.in_media_chunk = False
            self.is_proxy = False
            self.proxy_value = ""
            self.path = ""
        self.current_data = ""

    # Call when a character is read
    def characters(self, content):
        if self.current_data == "ActualMediaFilePath":
            # paths might contain escaped ampersands.
            # so accumulate the path name in case it comes
            # in multiple chunks
            self.path += content

        if self.current_data == "ContentAndMetadataState":
            self.content_media_state += content

        if self.current_data == "IsProxy":
            self.proxy_value += content


def print_media_paths(file_name, only_count=False,
                      leaf_pathnames=False,
                      verify_val=False,
                      show_duplicate_files=False):
    """ prints all media paths in the given file

    Args:
        file_name (string): string containing a path to a PPro project file.
        options (namespace): options to control parse output.
    Returns:
        set: set containing all the pathnames
    """

    if only_count is True and (leaf_pathnames is True or verify_val is True):
        # this is for error reporting when writing tests.
        # the parameter parsing code at the main level should
        # prevent this getting called in regular use.
        print("## Error, count conflicts with other options")
        return set()

    # create an XMLReader
    xml_parser = defusedxml.sax.make_parser()
    # turn off namepsaces
    xml_parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # override the default ContextHandler
    handler = MovieHandler()
    xml_parser.setContentHandler(handler)

    gz_file = gzip.open(file_name, 'r')
    xml_parser.parse(gz_file)

    # collect ALL filenames including dupes
    # now filter the collection based on options passed in

    if show_duplicate_files is False:
        temp_set = set(handler.media_refs_list)
        media_files = list(temp_set)
    else:
        media_files = handler.media_refs_list

    sorted_list = sorted(media_files)

    if only_count is True:
        print("Media file count: ", len(sorted_list))
    elif leaf_pathnames is True:
        sorted_short_filenames = []
        short_filenames = []
        for media_ref in sorted_list:
            _, tail = os.path.split(media_ref)
            short_filenames.append(tail)
        sorted_short_filenames = sorted(short_filenames)
        for media_ref in sorted_short_filenames:
            print(media_ref)
    else:
        for media_ref in sorted_list:
            print(media_ref)

    return sorted_list


def main_func():
    """ Main extry point from the command line.
    """
    args_parser = argparse.ArgumentParser(description=HELP_STRING)
    args_parser.add_argument("projectfile")
    args_parser.add_argument('-d', '--showDupes',
                             help='Show ALL path names, including duplicates.',
                             required=False, action="store_true")

    exclusive_options = args_parser.add_mutually_exclusive_group()
    exclusive_options.add_argument('-c', '--count',
                                   help='Count mode: only prints file count.',
                                   required=False, action="store_true")
    exclusive_options.add_argument('-b', '--brief',
                                   help='Brief mode: only print \
                                   the media file name, not the entire path.',
                                   required=False, action="store_true")
    cmd_line_args = args_parser.parse_args()

    if os.path.isfile(cmd_line_args.projectfile):
        _, file_extension = os.path.splitext(cmd_line_args.projectfile)
        if file_extension == ".prproj":
            print_media_paths(cmd_line_args.projectfile,
                              only_count=cmd_line_args.count,
                              leaf_pathnames=cmd_line_args.brief,
                              show_duplicate_files=cmd_line_args.showDupes,
                              verify_val=False)
        else:
            print("## Error: File: ")
            print("## ", cmd_line_args.projectfile)
            print("## is not a Premiere Pro project file (.prproj).")
    else:
        print("## Error: File: ")
        print("## ", cmd_line_args.projectfile)
        print("## does not exist or is not a readable file.")


if __name__ == "__main__":
    main_func()
