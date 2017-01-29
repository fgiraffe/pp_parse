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

g_file_hash_set = set()

HELP_STRING = 'Reads a Premiere Pro project file and prints \
                    the media path strings.'
# ModificationState Encoding="base64"
# BinaryHash="9d36d822-4d36-2654-9415-492500000054


class MovieHandler(xml.sax.ContentHandler):
    def __init__(self, options):
        self.CurrentData = ""
        self.path = ""
        self.isProxy = False
        self.options = options

    # Call when an element starts
    def startElement(self, tag, attributes):
        global g_file_hash_set
        if tag == "ModificationState":
            hash = attributes["BinaryHash"]
            g_file_hash_set.add(hash)
        self.CurrentData = tag

    # Call when an elements ends
    def endElement(self, tag):
        if self.CurrentData == "ActualMediaFilePath":
            if self.isProxy is False and self.options.quiet is False:
                print(self.path)
            else:
                # proxy, skip it
                self.isProxy = False
        elif self.CurrentData == "IsProxy":
            self.isProxy = True
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
    """

    # create an XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # override the default ContextHandler
    handler = MovieHandler(options)
    parser.setContentHandler(handler)

    parser.parse(file_name)

    if options.quiet is True:
        print("Media file count: ", len(g_file_hash_set))


if (__name__ == "__main__"):
    parser = argparse.ArgumentParser(description=HELP_STRING)
    parser.add_argument("projectfile")
    parser.add_argument('-q', '--quiet',
                        help='Quiet mode: only prints file count',
                        required=False, action="store_true")
    args = parser.parse_args()

    print_media_paths(args.projectfile, args)
