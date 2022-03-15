#!/usr/bin/env python3

############################################################################################################
# Purpose: Generate all TA author files and transfer the TA Author files to tadserv                        #
# Author: Mathew Potts                                                                                     #
# Created: 2022-03-13                                                                                      #
############################################################################################################
## IMPORT LIBS

import argparse
import os
import sys
import re
from post import post
from config import TADSERV_ID_FILE

######################################################################################################

## FUNCTIONS
    
def parse_stats(stats):
    # Parse the information from stats
    nums = re.findall(r"#.*\s\d+",stats) # ['# of institutions:  32', '# of authors:  138', '# of countries:  7']
    numofauth   = nums[1].split(' ')[-1]
    numofinstit = nums[0].split(' ')[-1]
    numofcount  = nums[2].split(' ')[-1]

    # Parse table information
    tabs = re.findall(r"(?<=\n)(\w+\s\d+|\w+\s\w+\s\d+)(?=\n)",stats)
    inst = tabs[:[i for i,s in enumerate(tabs) if 'USA' in s][0]]
    bycount = tabs[[i for i,s in enumerate(tabs) if 'USA' in s][0]:]
    countauth = [([' '.join(i.split(' ')[:2]),i.split(' ')[2]] if 'Czech' in i else i.split(' ')) for i in bycount[:int(numofcount)]]
    countinst = [([' '.join(i.split(' ')[:2]),i.split(' ')[2]] if 'Czech' in i else i.split(' ')) for i in bycount[int(numofcount):]]
    countinstauth = [[i[0],j[1],i[1]] for i in countauth for j in countinst if i[0] == j[0]] # [['ICRR', '11', '20'],['University of Utah', '2', '30']]
    top5        = [i.split(' ') for i in inst][:5]# [['ICRR', '20'],['University of Utah', '30']]
    
    return numofauth,numofinstit,numofcount,countinstauth,top5

def gen_all(new_dates,auth_path=None,ack_path=None):
    # Defining environmental variables
    os.environ['DATE'] = new_dates[0]
    os.environ['SRC']  = '{0}/{1}/src'.format(os.environ['PWD'],new_dates[0])

    # Generate all the author files and store them in a dated file system
    os.system('''
    mkdir -p $SRC;
    echo "LaTex";
    $PWD/ta_author_list.py --csvfile $SRC/ta_authorlist.csv --ackfile $SRC/ta_acknowledgements.txt --output $PWD/$DATE/TA-author-$DATE.tex --format plainLatex;
    echo "Authblk";
    $PWD/ta_author_list.py --csvfile $SRC/ta_authorlist.csv --ackfile $SRC/ta_acknowledgements.txt --output $PWD/$DATE/TA-author-$DATE-authblk.tex --format authblk;
    echo "AASTex";
    $PWD/ta_author_list.py --csvfile $SRC/ta_authorlist.csv --ackfile $SRC/ta_acknowledgements.txt --output $PWD/$DATE/TA-author-$DATE-aastex.tex --format aastex;
    echo "arXiv";
    $PWD/ta_author_list.py --csvfile $SRC/ta_authorlist.csv --ackfile $SRC/ta_acknowledgements.txt --output $PWD/$DATE/TA-author-$DATE-arxivSubmit.txt --format arxiv;
    echo "REVTex";
    $PWD/ta_author_list.py --csvfile $SRC/ta_authorlist.csv --ackfile $SRC/ta_acknowledgements.txt --output $PWD/$DATE/TA-author-$DATE-revtex.tex --format revtex;
    echo "PDF";
    $PWD/ta_author_list.py --csvfile $SRC/ta_authorlist.csv --ackfile $SRC/ta_acknowledgements.txt --format arxiv --pdf $PWD/$DATE/TA-author-$DATE.pdf --include-ack > /dev/null;
    echo "Acknowledgements";
    $PWD/ta_author_list.py --csvfile $SRC/ta_authorlist.csv --ackfile $SRC/ta_acknowledgements.txt --format plainLatex --output $PWD/$DATE/TAacknowledgements-$DATE.tex --ack-only > /dev/null;
    echo;
    wait;
    ''')
    
    # Grab the stat infromation
    stats = os.popen('''
    $PWD/ta_author_list.py --csvfile $SRC/ta_authorlist.csv --ackfile $SRC/ta_acknowledgements.txt --stats;
    ''').read()

    return parse_stats(stats)

def grab_creds(path):
    if os.path.isfile(path):
        f = open(path,'r')
        lines = f.readlines()
        return [l[:-1] for l in lines]

def main():
    parser = argparse.ArgumentParser(description = "This is a wrapper for Bill Hanlon's TA author list program that will generate all the files need to updated the tadserv author page. (http://tadserv.physics.utah.edu/TA-ICRC-09/index.php/TA_author_list_and_acknowledgements) The files are generated within a dated directory in the same directory as this program, except for the .png file. As of right now you need to save it manually. This program can then post those generated files to the tadserv author page using the python requests library and Beautiful Soup HTML parser.")
    parser.add_argument('-authdate',metavar='YYYYMMDD', type=str,help='Enter the date of the most recent author list in the following format: YYYYMMDD. (Typically this is the current date)')
    parser.add_argument('-ackdate',metavar='YYYYMMDD', type=str,help='Enter the date of the most recent acknowledgement list in the following format: YYYYMMDD.')
    parser.add_argument('-post', default=False, action='store_true', help='POST files to the tadserv wiki.')
    args  = parser.parse_args()

    # Create a list of the 'new dates' of the authorlist and acknowledgements
    new_dates = [args.authdate,args.ackdate]

    # Check to make sure the directory exists and if not exit program
    print('Generating all TA author list types:')
    if os.path.isdir(new_dates[0]):
        info  = gen_all(new_dates)
    else:
        print("\n{0} doesn't exist. Please create a new dated directory with the appropriate structure. (YYYYMMDD/src)".format(new_dates[0] + '/'))
        sys.exit(1)

    # Get a list of the files generated
    files = [os.path.join(new_dates[0], f) for f in os.listdir(new_dates[0]) if os.path.isfile(os.path.join(new_dates[0],f))]
    
    if args.post:
        print('Initializing POST class...')
        tadserv_info = grab_creds(TADSERV_ID_FILE)
        auth = post.POST_AUTHORLIST(*tadserv_info)
        print('Constructing Content.')
        txt = auth.construct_content(new_dates,*info)
        print('Posting Content to tadserv.')
        auth.post_authorlist_content(txt)
        print('Uploading local files to tadserv.')
        auth.post_authorlist_files(files)

#######################################################################################################
## PROGRAM

if __name__ == "__main__":
    main()
    