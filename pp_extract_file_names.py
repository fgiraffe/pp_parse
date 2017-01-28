#!/usr/bin/env python3

import xml.sax
import sys

g_file_hash_set = set()

# ModificationState Encoding="base64" BinaryHash="9d36d822-4d36-2654-9415-492500000054

class MovieHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""
        self.path = ""
        self.isProxy = False

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
            if self.isProxy is False:
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

if ( __name__ == "__main__"):
    
    if len(sys.argv) == 2:

        # create an XMLReader
        parser = xml.sax.make_parser()
        # turn off namepsaces
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)

        # override the default ContextHandler
        Handler = MovieHandler()
        parser.setContentHandler( Handler )
        
        parser.parse(sys.argv[1])

        print("Media files: ", len(g_file_hash_set))
    else:
        print("Usage...")    
    
