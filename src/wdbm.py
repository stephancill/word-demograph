"""Word Database Manager
A module that is designed for the extraction of words from text sources and
constructing databases that contain word frequency data.
"""

import logging
import operator
import os
import string

__author__ = "Stephan Cilliers <stephanus.cilliers@gmail.com> "

default_db_name = "default.db"
logging.basicConfig(format="%(levelname)s:%(message)s",
                    filename="{}.log".format(__name__),
                    level=logging.DEBUG)

def load(dbname=default_db_name, submissions_scanned_f=None):
    """
    ---------------------------------------------------------------------------
    Load database file into dictionary. (returns: dictionary)
    *arguments: (2) File dbname, File submissions_scanned_f
    ---------------------------------------------------------------------------
    """
    info = {"func": "LOAD"}
    try:
        os.chdir("../databases")
        logging.debug("Database directory found.", extra=info)
    except OSError as e:
        os.makedirs("../databases")
        os.chdir("../databases")
        logging.debug("Database directory not found, creating.", extra=info)
    try:
        with open(dbname, "r") as f:
            tmp_db = {}
            try:
                for line in f:
                    (w, c) = line.split()
                    tmp_db[w] = int(c)
                logging.info("Database {} sucessfully loaded.".format(dbname),
                             extra=info)
            except Exception as e:
                logging.debug("Database empty, loading anyway.", extra=info)
    except IOError as e:
        logging.debug("Database file not found, creating '{}'.".format(dbname),
                      extra=info)
        with open(dbname, "w") as f:
            tmp_db = {}

    if submissions_scanned_f is None:
        return tmp_db
    else:
        scanned = []
        try:
            with open(submissions_scanned_f, "r") as f:
                tmp = f.read()
                scanned = tmp.split()
            logging.info("Sucessfully loaded list of previously scanned threads.",
                         extra=info)
        except IOError as e:
            logging.warning("Failed to load list of previously scanned threads.",
                            extra=info)
            scanned = []

        return tmp_db, scanned


def write(db, dbname=default_db_name, submissions_scanned_f=None,
          submissions_scanned=None):
    """
    -----------------------------------------------------------------------
    Write dictionary to database file. (returns: None)
    *arguments: (4) File dbname, Dictionary db, File submissions_scanned_f
                    List submissions_scanned
    -----------------------------------------------------------------------
    """
    info = {"func": "WRITE"}
    data_to_write = db
    sorted_values = sorted(data_to_write.items(),
                           key=operator.itemgetter(1),
                           reverse=True)
    with open(dbname, "w") as f:
        errors = 0
        for i in sorted_values:
            try:
                f.write("{0} {1}\n".format(i[0], i[1]))
            except IOError as e:
                logging.error("WRITE: Failed to write {0}, {1}.\n".format(i, type(i)))
                errors += 1
        logging.info("WRITE: Wrote {0} words to {1} with {2} errors.".format(len(data_to_write),
                                                       dbname,
                                                       errors), extra=info)

    if submissions_scanned_f is not None and submissions_scanned is not None:
        with open(submissions_scanned_f, "w") as f:
            for i in submissions_scanned:
                try:
                    f.write("{}\n".format(i))
                except IOError as e:
                    logging.error("Failed to write already scanned ID: {}.".format(i),
                                  extra=info)


def update(words, db):
    """
    ---------------------------------------------------------------------------
    Update dictionary values. (returns: updated dictionary)
    *arguments: (2) List words, Dictionary db
    ---------------------------------------------------------------------------
    """
    info = {"func": "UPDATE"}
    local_db = {}
    local_db = db
    existing = 0
    new = 0
    for word in words:
        try:
            local_db[str(word)] += 1    # Update entry
            existing += 1
        except Exception as e:
            local_db[str(word)] = 1     # Create entry
            new += 1
    logging.debug("UPDATE: {0} new, {1}, existing added.".format(new, existing),
                  extra=info)

    return local_db


def filtrate(text):
    info = {"func": "FILTRATE"}
    """
    ---------------------------------------------------------------------------
    Remove punctuation, digits and newlines from input string. (returns: list)
    *arguments: (1) String text
    ---------------------------------------------------------------------------
    """
    exclude = ["\n", string.digits, string.punctuation]
    exclude_substrings = ["http"]
    filtered = text
    for exclusion_set in exclude:
        filtered = "".join(ch.lower()
                           for ch in filtered
                           if ch not in exclusion_set)

    filtered = filtered.split()

    for substring in exclude_substrings:
        tmp_filtered = []
        for word in filtered:
            index = word.find(substring)
            if index != -1:
                tmp_word = word[index:]
            else:
                tmp_filtered.append(word)
        filtered = tmp_filtered
    logging.debug("Filtered.")

    return filtered


def main():
    print """Usage of Word Database Manager:
    1. Load database into dictionary with load()
    2a. Filter through input text and isolate words with filtrate()
    2b. Update dictionary values with update()
    3. Finally write the dictionary back to database file with write()
    """

if __name__ == "__main__":
    main()
