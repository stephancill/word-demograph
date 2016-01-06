"""Word Database Manager
A module that is designed for the extraction of words from text sources and
constructing databases that contain word frequency data.
"""

import logging
import operator
import os
import string
import datetime

__author__ = "Stephan Cilliers <stephanus.cilliers@gmail.com> "

default_db_dir = "databases"

logging.basicConfig(format="%(levelname)s:%(message)s",
                    filename="{}.log".format(__name__),
                    level=logging.DEBUG)

def load(dbname, scanned_f=None):
    """
    ---------------------------------------------------------------------------
    Load database file into dictionary. (returns: [dictionary, list] OR
    dictionary)
    *arguments: (2) File dbname, File scanned_f
    ---------------------------------------------------------------------------
    """
    info = {"func": "LOAD"}
    try:
        os.chdir("../{}".format(default_db_dir))
        logging.debug("SUCCESS: Database directory found.", extra=info)
    except OSError as e:
        os.makedirs("../{}".format(default_db_dir))
        os.chdir("../{}".format(default_db_dir))
        logging.debug("Database directory not found, creating.", extra=info)
    try:
        with open(dbname, "r") as f:
            tmp_db = {}
            try:
                for line in f:
                    (w, c) = line.split()
                    tmp_db[w] = int(c)
                logging.info("SUCCESS: Database {} loaded.".format(dbname),
                             extra=info)
            except Exception as e:
                logging.debug("Database empty, loading anyway.", extra=info)
    except IOError as e:
        logging.debug("Database file not found, creating '{}'.".format(dbname),
                      extra=info)
        with open(dbname, "w") as f:
            tmp_db = {}

    if scanned_f is None:
        return tmp_db
    else:
        scanned = []
        try:
            with open(scanned_f, "r") as f:
                tmp = f.read()
                scanned = tmp.split()
            logging.info("SUCCESS: Loaded list of previously scanned threads.",
                         extra=info)
        except IOError as e:
            logging.warning("FAIL: to load list of previously scanned threads.",
                            extra=info)
            scanned = []

        return tmp_db, scanned


def write(db, dbname, scanned_f=None, scanned=None):
    """
    ---------------------------------------------------------------------------
    Write dictionary to database file. (returns: None)
    *arguments: (4) Dictionary db, File dbname, File scanned_f
                    List scanned
    ---------------------------------------------------------------------------
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
                logging.error("Failed to write {0}, {1}.\n".format(i, type(i)),
                              extra=info)
                errors += 1
        logging.info("WRITE: Wrote {0} words to {1} with {2} errors.".format(
                                                        len(data_to_write),
                                                        dbname,
                                                        errors), extra=info)

    if scanned_f is not None and scanned is not None:
        with open(scanned_f, "w") as f:
            for i in scanned:
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

    for word in words:
        try:
            local_db[str(word)] += 1    # Update entry
        except KeyError as e:
            local_db[str(word)] = 1     # Create entry

    return local_db


def filtrate(text):
    """
    ---------------------------------------------------------------------------
    Remove punctuation, digits and newlines from input string. (returns: list)
    *arguments: (1) String text
    ---------------------------------------------------------------------------
    """
    info = {"func": "FILTRATE"}
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

def merge(files, f="merged"):
    """
    ---------------------------------------------------------------------------
    Merge a list of .db files into a single .db file. (returns: None)
    *arguments: (2) List files, String filename
    ---------------------------------------------------------------------------
    """
    info = {"func": "MERGE"}
    timestamp = str(datetime.datetime.now().time()).replace(":", ".")
    final_filename = "{0}{1}.db".format(timestamp, f)

    if os.getcwd()[-len(default_db_dir):] is not default_db_dir:
        os.chdir("../{}".format(default_db_dir))
        logging.debug("Changed directory to {}".format(default_db_dir),
                      extra=info)

    merged_count = 0
    for filename in files:
        master_database = load(final_filename)
        tmp_database = load(filename)
        for word in tmp_database.items():
            try:
                master_database[word[0]] += word[1]
            except KeyError as e:
                master_database[word[0]] = word[1]

        write(master_database, final_filename)
        merged_count += 1
        logging.debug("SUCCESS: Wrote {0} to {1}".format(filename,
                                                         final_filename))

    logging.debug("SUCCESS: Merged {} files".format(merged_count), extra=info)


def main():
    print """Usage of Word Database Manager:
    1. Load database into dictionary with load()
    2a. Filter through input text and isolate words with filtrate()
    2b. Update dictionary values with update()
    3. Finally write the dictionary back to database file with write()
    """


if __name__ == "__main__":
    main()
