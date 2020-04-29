#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__    = 'William Hanlon'
__copyright__ = ''
__credits__   = ''
__license__   = ''
__version__   = '2.0.0'
__maintainer  = 'William Hanlon'
__email__     = 'whanlon@cosmic.utah.edu'
__status__    = 'Production'

from collections import Counter
import operator
import csv
import re
import sys

class ta_auth:
    """Base class for TA author data formatting classes."""
    def __init__(self, authInFileName, ackInFileName,
            outFileName = None):
        self.author_data = []
        # institutional_ordinal is a dictionary of institution code
        self.institution_ordinal = {}
        self.outFileName = outFileName
        self.authInFileName = authInFileName
        self.ackInFileName = ackInFileName

        # stats
        self.number_of_authors = 0
        self.number_of_institutions = 0
        self.number_of_countries = 0
        self.institution_counter = Counter()
        self.authors_in_country_counter = Counter()
        self.institutions_in_country_counter = Counter()

    def dumpPreamble(self):
        pass

    def dumpAcknowledge(self):
        if self.outFileName is not None:
            origStdout = sys.stdout
            sys.stdout = open(self.outFileName, 'a')

        with(open(self.ackInFileName, 'rb')) as fin:
            for line in fin:
                print(line.decode('utf8').strip())

        if self.outFileName is not None:
            sys.stdout.close()
            sys.stdout = origStdout

    def dumpFoot(self):
        if self.outFileName is not None:
            origStdout = sys.stdout
            sys.stdout = open(self.outFileName, 'a')

        print("\\end{document}")

        if self.outFileName is not None:
            sys.stdout.close()
            sys.stdout = origStdout

    def dumpAuthor(self):
        """Prints the unordered list in simple block format. Use one of the
        derived classes to print a sorted formated list."""

        if self.outFileName is not None:
            origStdout = sys.stdout
            sys.stdout = open(self.outFileName, 'w')

        for sort_key, surname, initials, orcid, _, institution, status in \
                self.author_data:
            name = initials + ' ' + surname
            print(name, '\t', orcid, '\t', institution, '\t', status)

        if self.outFileName is not None:
            sys.stdout.close()
            sys.stdout = origStdout

    def dump(self):
        self.dumpPreamble()
        self.dumpAuthor()
        self.dumpAcknowledge()
        self.dumpFoot()

    def get_author_institution_numbers(self, institution, inst_dict):
        """Given the string of institutions (each enclosed in {}), lookup the
        corresponding institution number from the dictionary of unique
        institution entries. Returns a sorted list of those institution
        numbers."""

        # institutions this author belongs to.
        insts = []
        for m in re.split('\} *\{', institution):
            insts.append(m.strip('{}'))
	# get the institution numbers from the dictionary
        inst_num = []
        for j in insts:
            inst_num.append(inst_dict[j])

        return sorted(inst_num)

    def readAuthor(self):
        """Reads in the CSV file created from the master spreadsheet.
        Import the file using "File..., Download As.., .csv", then provide the
        csv file as authInFileName to this method.

        The first row is the file header. Columns are ordered as
        1) Surname
        2) Given Name
        3) Initials
        4) ORCID
        5) Institution Code
        6) Institution
        7) Status (e.g., deceased)"""

        with open(self.authInFileName, 'rt', encoding='utf8') as authInFile:
            reader = csv.reader(authInFile)
            # the first line is a header (it should be)
            next(reader) # skip the first line
            for row in reader:
                surname      = row[0].strip()
                initials     = row[2].strip()
                orcid        = row[3].strip()
                institution_code = row[4].strip()
                institutions = row[5].strip()
                status       = row[6].strip()
                # the author order is sorted according to 'last name, initials'
                sort_key     = surname + ',' + initials

                name = initials + ' ' + surname

                self.author_data.append((sort_key, surname, initials, orcid,
                    institution_code, institutions, status))

        # ensure the list is sorted. this also effects institution numbers
        # when they are determined in a later function call. sorting a list
        # of tuples automatically sorts by the first element of each
        # tuple.
        self.author_data.sort()

        self.number_of_authors = len(self.author_data)
        self.sort_and_number_institutions()

    def sort_and_number_institutions(self):
        """Generate a unique list of institutions ordered by author name. key
        is the institution name, value is the ordinal number. authorList must
        already be sorted by author name."""

        # list of institutions as they appear in the authorList (with repeated
        # entries.
        institutions = []
        institution_codes = []
        for entry in self.author_data:
            l = []
            for m in re.split('\} *\{', entry[5]):
                l.append(m.strip('{}'))
            for inst in sorted(l):
                institutions.append(inst)
            
            l = []
            for m in re.split(',', entry[4]):
                l.append(m.strip())
            for inst in sorted(l):
                institution_codes.append(inst)

        # get a count of the number of authors from each institution
        self.institution_counter = Counter(institution_codes)

        # generate a unique list of institutions ordered by author
        # name. key is the institution name, value is the ordinal number
        unique_count = 0
        self.institutional_ordinal = {}
        for j in institutions:
            if j not in self.institutional_ordinal:
                unique_count += 1
                self.institutional_ordinal[j] = unique_count

    def stats_by_institution(self):
        if len(self.institution_counter) == 0:
            self.sort_and_number_institutions()

        #for k,v in sorted(self.institution_counter.items(),
        #        key=operator.itemgetter(1), reverse = True):
        #    print(k, v)

        for k,v in self.institution_counter.most_common():
            print(k, v)

        print('')
        print('# of institutions: ', len(self.institution_counter))
        print('# of authors: ', len(self.author_data))
