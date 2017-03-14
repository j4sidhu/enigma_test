"""
This module manipulates a csv file according to the guidelines given in part 1 of the enigma data engineering test.
"""

import csv
import re
import datetime as dt

INPUT_FILE = 'test.csv'
OUTPUT_FILE1 = 'solution-string_cleaning.csv'
OUTPUT_FILE2 = 'solution-code_swap.csv'
OUTPUT_FILE3 = 'solution.csv'
STATE_ABBR_FILE = 'state_abbreviations.csv'


def string_cleaning(input_file=INPUT_FILE, output_file=OUTPUT_FILE1):
    """
    The bio field contains text with arbitrary padding, spacing and line breaks.
    This function normalizes these values to a space-delimited string.
    It creates a new csv file with the appropriate bio column

    :param input_file (string): Optional parameter. Name of the csv file that needs to be cleaned up
    :param output_file (string): Optional parameter. Name of the csv file that will be outputted
    :return : None
    """
    with open(output_file, 'wb') as outputfile:
        writer = csv.writer(outputfile)
        with open(input_file, 'r') as inputfile:
            reader = csv.reader(inputfile)
            for index, row in enumerate(reader):
                if index != 0:  # Skip the headers
                    # row[8] = " ".join(row[8].split()).strip()
                    row[8] = " ".join(row[8].split())
                    # Remove spaces from the string
                    # 9th column is the 'bio' column

                writer.writerow(row)


def code_swap(input_file=OUTPUT_FILE1, output_file=OUTPUT_FILE2, state_abbr_file=STATE_ABBR_FILE):
    """
    Converts the state field from its abbreviated name to its full name in accordance with the data dictionary that's
    provided.

    :param input_file (string): Optional parameter. Name of the file in which the state column will be converted to
    its full state name
    :param output_file (string): Optional parameter. Name of the outputted file with the full state names
    :param state_abbr_file (string): Optional parameter. Name of the file that contains the abbreviated states as well
    as the full state names
    :return: None
    """
    states = {}
    # Dictionary where the keys will be the abbreviated version and the values will be the full state names

    with open(state_abbr_file, 'r') as state_file:
        reader = csv.reader(state_file)
        for index, row in enumerate(reader):
            if index != 0:  # Skip the headers
                states[row[0]] = row[1]  # Populate the states dictionary

    with open(output_file, 'wb') as output:
        writer = csv.writer(output)
        with open(input_file, 'r') as f:
            reader = csv.reader(f)
            for index, row in enumerate(reader):
                if index != 0:  # Skip the headers
                    try:
                        row[5] = states[row[5]]  # 5th column is the 'state' column
                    except KeyError:  # The key is not found
                        raise Exception('State {0} not found in the {1} file'.format(row[5], state_abbr_file))
                writer.writerow(row)


def date_offset(input_file=OUTPUT_FILE2, output_file=OUTPUT_FILE3):
    """
    The start_date field in the input file contains data in a variety of formats. These may include
    e.g., "June 23, 1912" or "5/11/1930" (month, day, year), "June 2018", "3/06" (incomplete dates) or even arbitrary
    natural language.

    This functions adds a start_date_description field adjacent to the start_date column to filter invalid date
    values into. It also normalizes all valid date values in start_date to ISO 8601 (i.e., YYYY-MM-DD).

    :param input_file (string): Optional parameter. Name of the file in which the old 'start_date' column is
    :param output_file (string): Optional parameter. Name of the file that will be outputted with the
    proper 'start_date' column with ISO 8601 format and the newly added 'start_date_description' column
    :return: None
    """
    with open(output_file, 'wb') as outputfile:
        writer = csv.writer(outputfile)
        with open(input_file, 'r') as inputfile:
            reader = csv.reader(inputfile)
            for index, row in enumerate(reader):
                if index == 0:  # Header
                    row.append('start_date_description')
                else:
                    # This is little bit of a brute force way of doing it but it gets the job done

                    hash_pattern = r'^[1-9][0-9][0-9][0-9]-[0,1][0-9]-[0-3][0-9]$'
                    # RE for fields such as '1980-12-10'

                    slash_pattern = r'^[0,1][0-9]/[0-3][0-9]/[1-9][0-9][0-9][0-9]$'
                    # RE for fields such as '12/31/1991'

                    abbr_pattern = r'^[0-3][0-9]-[A-Z][a-z][a-z]-[0-9][0-9]$'
                    # RE for fields such as '10-Dec-80'

                    full_pattern = r'^(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|' \
                                            'Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?) [1-9][0-9]?,' \
                                            ' [1-9][0-9][0-9][0-9]$'
                    # RE for fields such as 'December 20, 1980' or 'July 3, 2002'

                    if re.match(hash_pattern, row[10]):  # 10th column is the 'start_date' column
                        pass  # The date is already in the ISO 8601 format
                    elif re.match(slash_pattern, row[10]):
                        row[10] = dt.datetime.strptime(row[10], '%m/%d/%Y').strftime('%Y-%m-%d')
                        # Convert the string into datetime and then back into a string that follows ISO 8601 format
                    elif re.match(abbr_pattern, row[10]):
                        row[10] = dt.datetime.strptime(row[10], '%d-%b-%y').strftime('%Y-%m-%d')
                        # Convert the string into datetime and then back into a string that follows ISO 8601 format
                    elif re.match(full_pattern, row[10]):
                        row[10] = dt.datetime.strptime(row[10], '%B %d, %Y').strftime('%Y-%m-%d')
                        # Convert the string into datetime and then back into a string that follows ISO 8601 format
                    else:
                        row.append(row[10])
                        row[10] = ''

                writer.writerow(row)


if __name__ == "__main__":
    string_cleaning()
    code_swap()
    date_offset()
