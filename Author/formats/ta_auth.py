#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__  = "William Hanlon"
__email__   = "whanlon@cosmic.utah.edu"
__version__ = "1.1.0"

import csv
import re
import sys

class ta_auth:
    """Base class for TA author data formatting classes."""
    def __init__(self):
        self.author_data = []

    def dump(self, fileName = None):
        """Prints the unordered list in simple block format. Use one of the
        derived classes to print a sorted formated list."""

        if fileName is not None:
            origStdout = sys.stdout
            sys.stdout = open(fileName, 'w')

        for sort_key, surname, initials, orcid, institution, status in self.author_data:
            name = initials + ' ' + surname
            print name, '\t', orcid, '\t', institution, '\t', status

        if fileName is not None:
            sys.stdout.close()
            sys.stdout = origStdout

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

    def read(self, file_name):
        """Reads in the CSV file created from the master spreadsheet.
        Import the file using "File..., Download As.., .csv", then provide the
        csv file as file_name to this method.

        The first row is the file header. Columns are ordered as
        1) Surname
        2) Given Name
        3) Initials
        4) ORCID
        5) Institution Code
        6) Institution
        7) Status (e.g., deceased)"""
        with open(file_name, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            # the first line is a header (it should be)
            reader.next() # skip the first line
            for row in reader:
                surname      = row[0].strip()
                initials     = row[2].strip()
                orcid        = row[3].strip()
                institutions = row[5].strip()
                status       = row[6].strip()
                # the author order is sorted according to 'last name, initials'
                sort_key     = surname + ',' + initials

                name = initials + ' ' + surname

                self.author_data.append((sort_key, surname, initials, orcid,
                    institutions, status))

    def sort_and_number_institutions(self):
		"""Generate a unique list of institutions ordered by author name. key
		is the institution name, value is the ordinal number. authorList must
		already be sorted by author name."""

		# list of institutions as they appear in the authorList (with repeated
		# entries.
		institutions = []
		for entry in self.author_data:
			l = []
			for m in re.split('\} *\{', entry[4]):
				l.append(m.strip('{}'))
			for inst in sorted(l):
				institutions.append(inst)

		# generate a unique list of institutions ordered by author name. key is the
		# institution name, value is the ordinal number
		unique_count = 0
		inst_dict = {}
		for j in institutions:
			if j not in inst_dict:
				unique_count += 1
				inst_dict[j] = unique_count

		return inst_dict
