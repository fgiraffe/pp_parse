#!/usr/bin/python3

#!/usr/bin/env python3

import xml.sax
import sys
import argparse
import os.path
import urllib
import re

HELP_STRING = 'Reads an Final Cut Pro xml file and prints \
                the media path strings.'


class MovieHandler(xml.sax.ContentHandler):
    """
    From https://www.tutorialspoint.com/python/python_xml_processing.htm
    """
    def __init__(self, options):
        self.CurrentData = ""
        self.options = options
        self.path = ""
        self.mediaRefsSet = set()
        self.mediaRefsList = []

    # Call when an element starts
    def startElement(self, tag, attributes):
        self.CurrentData = tag

    # Call when an elements ends
    def endElement(self, name):
        if name == "pathurl":
            # swap back the %20 type encoding FCP added 
            # e.g. "mute%20cat" -> "mute cat"
            u8str = urllib.parse.unquote(self.path)
            # now strip off the prefix
            searchStr = "file://localhost"
            u8str = re.sub(searchStr, "", u8str)
            self.mediaRefsSet.add(u8str)
            self.mediaRefsList.append(u8str)
            self.path = ""
        self.CurrentData = ""

    # Call when a character is read
    def characters(self, content):
        if self.CurrentData == "pathurl":
            # paths might contain escaped ampersands.
            # so accumulate the path name in case it comes
            # in multiple chunks
            self.path += content


def print_media_paths(file_name, options):
    """ prints all media paths in the given file

    Args:
        file_name (string): string containing a path to a Final Cut Pro xml file.
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

    if options.showdupes is True:
        sorted_list = sorted(handler.mediaRefsList)
    else:
        sorted_list = sorted(handler.mediaRefsSet)

    if "count" in options and options.count is True:
        print("Media file count: ", len(sorted_list))
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
    parser.add_argument("--showdupes", 
                        help='Show Dupes: if a file is referenced twice, print/count it twice.',
                        required=False, action="store_true")
    
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
