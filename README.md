# TASOFT

## Dark

## ShiftAnal

## Author

### gen_all.py
Author: Mathew Potts

A wrapper for ```ta_author_list.py``` that generates all format types of the author list in a dated directory saved your local machine in the same directory as this program. You must provide the program with the date of the most recent author list,```-authdate```, and the date of the most recent acknowledgements document, ```-ackdate```. There is an optional command line flag, ```-post```, that allow you to post the tadserv author list files automatically and edit the [tadserv author list wiki page](http://tadserv.physics.utah.edu/TA-ICRC-09/index.php/TA_author_list_and_acknowledgements). This is done by utilizing the requests and Beautiful soup python libraries to parse API GET requests from tadserv, modify the tadserv page, and then upload the generated files to tadserv. In order to use this feature a text file, ```tadserv_ids.txt```, must be generated in the same directory as the ```gen_all.py``` program by the user BEFORE using the post flag. The ```tadserv_ids.txt``` files should be formatted in the following way:
```
<tadserv login username>
<tadserv login password>
<user's tadserv username>
<user's tadserv password>
```
This means that all editing on the tadserv will be tied to your user account on tadserv. 

Below is the ```--help``` output of the script:
```
usage: gen_all.py [-h] -authdate YYYYMMDD -ackdate YYYYMMDD [-post]
                  [-authpath path/to/authfile.csv] [-ackpath path/to/ackfile.txt]

This is a wrapper for Bill Hanlon's TA author list program that will generate all the files need to
updated the tadserv author page. (http://tadserv.physics.utah.edu/TA-
ICRC-09/index.php/TA_author_list_and_acknowledgements) The files are generated within a dated
directory in the same directory as this program, except for the .png file. As of right now you need
to save it manually. This program can then post those generated files to the tadserv author page
using the python requests library and Beautiful Soup HTML parser.

optional arguments:
  -h, --help            show this help message and exit
  -authdate YYYYMMDD    Enter the date of the most recent author list in the following format:
                        YYYYMMDD. (Typically this is the current date)
  -ackdate YYYYMMDD     Enter the date of the most recent acknowledgement list in the following
                        format: YYYYMMDD.
  -post                 POST files to the tadserv wiki.
  -authpath path/to/authfile.csv
                        Specify a path to the Authorlist.csv file and moves it to the database for
                        processing. (default: uses csv file $PWD/{authdate}/src/ta_authorlist.csv)
  -ackpath path/to/ackfile.txt
                        Specify a path to the Acknowledgements.txt file and moves it to the
                        database for processing. (default: uses text file
                        $PWD/{authdate}/src/ta_acknowledgements.txt)
```

### ta_author_list.py
Author: Bill Hanlon

Prints out the TA authorlist and acknowledgements using a
formatted CSV file of authors and a plain text file (containing LaTeX
formated text) as input. The columns of the author csv file are expected to be:
1. surname (last name)
2. given name (full first name and middle name if desired)
3. initials
4. orcid
5. institution short code (not used here)
6. institution (delimited by {})
7. status (i.e., "deceased", "not at XYZ University") (appears as a
       footnote)

an institution may actually consist of multiple institutions, with each
individual institution contained in {}.

Multiple output formats are intended to be supported to alleviate the chance of
making mistakes when transcribing the author list to multiple TeX formats.

If attempting to read the spreedsheet directly in the cloud using the google
api, the first attempt will require human intervention to grab credentials that
authorize you to read the sheet. See
https://developers.google.com/sheets/api/quickstart/python for an example on how
to do this.

The CSV author spreadsheet ID and the plain text acknowledgements ID of the
documents storage on Google Drive are not stored in the source code. They 
are read from ta_author_id.txt and ta_acknowledgements_id.txt. Contact me
for the IDs if you wish to read from the cloud. Cloud access is not needed
to run this program. One can always go directly to the spreadsheet and doc,
export to your local drive as CSV and text files,
then provide those files as input using --csvfile and --ackfile.

```
usage: ta_author_list.py [-h] [--auth_host_name AUTH_HOST_NAME] [--noauth_local_webserver] [--auth_host_port [AUTH_HOST_PORT [AUTH_HOST_PORT ...]]] [--logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                         [--csvfile CSVFILE] [--ackfile ACKFILE] [--format {plainLatex,plainText,authblk,aastex,arxiv,revtex}] [--stub-only] [--stats] [--output OUTPUT] [--pdf PDF] [--include-ack]
                         [--ack-only] [--savecsv] [--saveack]

Sort the TA Author list in alphabetical order and affiliations in numerical order and output a working LaTeX skeleton file. If file is not provided, attempt to read the master authorlist spreadsheet
from the cloud. (For reading from the cloud author spreadsheet ID must be provided in a file named 'ta_author_id.txt' and acknowledgements doc ID must be provided in a file named
ta_acknowledgements_id.txt.)

optional arguments:
  -h, --help            show this help message and exit
  --auth_host_name AUTH_HOST_NAME
                        Hostname when running a local web server.
  --noauth_local_webserver
                        Do not run a local web server.
  --auth_host_port [AUTH_HOST_PORT [AUTH_HOST_PORT ...]]
                        Port web server should listen on.
  --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set the logging level of detail.
  --csvfile CSVFILE     TA Author list input file name in CSV format
  --ackfile ACKFILE     TA acknowledgements input file name in plain text format
  --format {plainLatex,plainText,authblk,aastex,arxiv,revtex}
                        select the output format
  --stub-only           do not try to create a full LaTeX document, only output the relevant parts (author and/or acknowledgements)
  --stats               dump counts of institutions and generate plot
  --output OUTPUT       select the file to write to. if not provided, output is directed to STDOUT
  --pdf PDF             generate a PDF version of the authorlist and acknowledgements from the authblk template.
  --include-ack         include acknowledments in output latex and pdf.
  --ack-only            only include acknowledments in output latex and pdf (authors are removed).
  --savecsv             save downloaded csv to ta_author.csv when reading from the cloud
  --saveack             save downloaded acknowledgements to ta_acknowledgements.txt when reading from the cloud
```

#### Formats
These are the different format modules used by ```ta_author_list.py```:
- Plain LaTeX
- Authblk
- AASTeX
- arXiv
- REVTeX

#### Post
Contains the ```POST_AUTHORLIST``` class that manages all GET/POST requests made to post the author list files to the tadserv author list wiki page.
