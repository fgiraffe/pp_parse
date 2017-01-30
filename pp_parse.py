#!/usr/bin/env python3
""" pp_parse.py

A simple python module to parse Adobe Premiere Pro CC project files,
and print out all the media paths that the project references.
Tested with Adobe Premiere Pro CC 2015.4

Example:
        $ python pp_parse.py myAwesomeMovie.prproj.xml
        Current version parses EXPANDED xml files.
        See accompanying shell script ppxmlconvert.sh.

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

    The Premeiere Pro file format is officially undocumented.
    But AFAICT there is no easy way to just extract the files
    that a project references as TEXT. Exporting a batch list is a
    little ugly, and does not offer the full path.
    You can export FCP XML and use that, but that is an extra step.

    so what is a "good" media chunk inside a Premiere Pro project file?
    To be good it has to:
        - have a ObjectUID attribute. Not sure what the other Media types
            are but they have a ObjectURefs instead.
        - not be a proxy (no <IsProxy> chunk, or set to false)
        - to have a legit lookin <ContentAndMetadataState> chunk, namely
            one whose value is not CMS_STATE_NOT_REAL_MEDIA_ID.
            This handles titles, subtitles, slugs, bars and tone,
            solid color mattes, etc.
"""

import xml.sax
import sys
import argparse
import os.path

HELP_STRING = 'Reads an un-gzipped Premiere Pro project file and prints \
                    the media path strings.'


CMS_STATE_NOT_REAL_MEDIA_ID = "00000000-0000-0000-0000-000000000000"


class MovieHandler(xml.sax.ContentHandler):
    """
    From https://www.tutorialspoint.com/python/python_xml_processing.htm
    """
    def __init__(self, options):
        self.CurrentData = ""
        self.options = options
        self.path = ""
        self.mediaRefsSet = set()
        self.mediaHashSet = set()

        self.inMediaChunk = False
        self.isProxy = False
        self.proxyValue = ""
        self.extra = ""

    # Call when an element starts
    def startElement(self, tag, attributes):
        if tag == 'ModificationState':
            hash = attributes["BinaryHash"]
            self.mediaHashSet.add(hash)

        if tag == "Media":
            if "ObjectUID" in attributes:
                # if Media tag has a ObjectUID we are interested in it.
                self.inMediaChunk = True
            else:
                # this skips the bogus Media tags with ObjectURefs attached
                pass

        self.CurrentData = tag

    # Call when an elements ends
    def endElement(self, name):

        if self.CurrentData == "IsProxy":
            if self.proxyValue == "true":
                self.isProxy = True
            else:
                self.isProxy = False

        if name == "Media" and self.inMediaChunk:
            if self.isProxy is False and \
               self.extra != CMS_STATE_NOT_REAL_MEDIA_ID:
                self.mediaRefsSet.add(self.path)
            self.extra = ""
            self.inMediaChunk = False
            self.isProxy = False
            self.proxyValue = ""
            self.path = ""
        self.CurrentData = ""

    # Call when a character is read
    def characters(self, content):
        if self.CurrentData == "ActualMediaFilePath":
            # paths might contain escaped ampersands.
            # so accumulate the path name in case it comes
            # in multiple chunks
            self.path += content

        if self.CurrentData == "ContentAndMetadataState":
            self.extra = content

        if self.CurrentData == "IsProxy":
            self.proxyValue = content


def print_media_paths(file_name, options):
    """ prints all media paths in the given file

    Args:
        file_name (string): string containing a path to a PPro project file.
        options (namespace): options to control parse output.
    Returns:
        set: set containing all the pathnames
    """

    # create an XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # override the default ContextHandler
    handler = MovieHandler(options)
    parser.setContentHandler(handler)

    parser.parse(file_name)
    medRefsSet = handler.mediaRefsSet

#    sorted_list = sorted(medRefsSet, key=lambda medRef:
#                           medRef.actualMediFilePath)
    sorted_list = sorted(medRefsSet)

    if "count" in options and options.count is True:
        print("Media file count: ", len(medRefsSet))
    elif "brief" in options and options.brief is True:
        sorted_short_filenames = []
        short_filenames = []
        for a_ref in sorted_list:
            head, tail = os.path.split(a_ref)
            short_filenames.append(tail)
        sorted_short_filenames = sorted(short_filenames)
        for aRef in sorted_short_filenames:
            print(aRef)
    else:
        for a_ref in sorted_list:
            print(a_ref)

    return sorted_list


if (__name__ == "__main__"):
    parser = argparse.ArgumentParser(description=HELP_STRING)
    parser.add_argument("projectfile")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--count',
                       help='Count mode: only prints file count.',
                       required=False, action="store_true")
    group.add_argument('-b', '--brief',
                       help='Brief mode: only print the media file name\
                       not the entire path.',
                       required=False, action="store_true")
    args = parser.parse_args()

    list_of_files = print_media_paths(args.projectfile, args)
