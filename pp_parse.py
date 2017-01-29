#!/usr/bin/env python3
""" pp_parse.py

A simple python module to parse Adobe Premiere Pro CC project files,
and print out all the media paths that the project references.

Example:
        $ python pp_parse.py myAwesomeMovie.prproj.xml
        Current version parses EXPANDED xml files.
        See accompanying shell script ppxmlconvert.sh.
"""

import xml.sax
import sys
import argparse
import os.path

HELP_STRING = 'Reads a Premiere Pro project file and prints \
                    the media path strings.'


class MediaRef:
    def __init__(self, uid):
        self.actualMediFilePath = ""
        # this field is set to all 000s if it is a title card.
        # in this case ActualMediaFilePath is invalid
        self.contentAndMetadataState = ""
        self.objectUID = uid


class MovieHandler(xml.sax.ContentHandler):
    def __init__(self, options):
        self.CurrentData = ""
        self.options = options
        self.path = ""
        self.mediaRefsSet = set()
        self.mediaHashSet = set()

    # Call when an element starts
    def startElement(self, tag, attributes):
        if tag == 'ModificationState':
            hash = attributes["BinaryHash"]
            self.mediaHashSet.add(hash)
        self.CurrentData = tag

    # Call when an elements ends
    def endElement(self, tag):
        if self.CurrentData == "ActualMediaFilePath":
            self.mediaRefsSet.add(self.path)
        self.CurrentData = ""
        self.path = ""

    # Call when a character is read
    def characters(self, content):
        if self.CurrentData == "ActualMediaFilePath":
            self.path += content


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

    if options.count is True:
        print("Media file count: ", len(medRefsSet))
    else:
        for a_ref in sorted_list:
            if options.brief is True:
                head, tail = os.path.split(a_ref)
                print(tail)
            else:
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

    print_media_paths(args.projectfile, args)
