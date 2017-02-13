# pp_parse
## Extract media file names from an Adobe Premiere Pro CC project file. 

## Installation and use:

####If you do not yet have virtualenv installed, install that first:
    $ pip install virtualenv
####You'll want to know where your python3 is installed:
    $ which python3

###Recommended install steps:
    $ git clone git@github.com:fgiraffe/pp_parse.git
    $ cd pp_parse/
    $ virtualenv venv
    $ virtualenv -p _path to your local python 3_ venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    
###Usage:
    $ python3 pp_parse.py anAdobePremiereProProjFile.prproj
    
or

    $ python3 pp_parse.py -h
will display options.
    

