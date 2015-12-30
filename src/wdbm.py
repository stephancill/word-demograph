#Word Database Manager
"""Usage:
1. Load database into dictionary with load()
2a. Filter through input text and isolate words with filtrate()
2b. Update dictionary values with update()
3. Finally write the dictionary back to database file with write()
"""
import string

default_db_name = "default.db"

__author__ = "Stephan Cilliers <stephanus.cilliers@gmail.com> "


def load(dbname=default_db_name, submissions_scanned_f=None):
    """
    ---------------------------------------------------------------------------
    Load database text file into dictionary. (returns: dictionary)
    *arguments: (2) File dbname, File submissions_scanned_f
    ---------------------------------------------------------------------------
    """
    try:
        with open(dbname,"r") as f:
            tmp_db = {}
            try:
                for line in f:
                    (w, c) = line.split()
                    tmp_db[w] = int(c)
                print "Database {} sucessfully loaded.".format(dbname)
            except Exception as e:
                print "Database empty, loading anyway."
    except Exception as e:
        print "Database file not found, creating '{}'.".format(dbname)
        with open(dbname,"w") as f:
            tmp_db = {}
            pass
    if submissions_scanned_f == None:
        return tmp_db
    else:
        scanned = []
        try:
            with open(submissions_scanned_f, "r") as f:
                tmp = f.read()
                scanned = tmp.split()
            print "Sucessfully loaded list of previously scanned threads."
            print scanned
        except Exception as e:
            print "Failed to load list of previously scanned threads."
            scanned = []

        return tmp_db, scanned

def write(db, dbname=default_db_name, submissions_scanned_f=None,
    submissions_scanned=None):
    """
    -----------------------------------------------------------------------
    Write dictionary to database text file. (returns: Confirmation)
    *arguments: (4) File dbname, Dictionary db, File submissions_scanned_f
                    List submissions_scanned
    -----------------------------------------------------------------------
    """
    data_to_write = db
    sorted_values = sorted(data_to_write)
    with open(dbname,"w") as f:
        errors = 0
        for i in sorted_values:
            try:
                f.write("{} {}\n".format(i, data_to_write[i]))
            except Exception as e:
                print "Failed to write {}, {}.\n".format(i, type(i))
                errors += 1
        print "Wrote {} words with {} errors.".format(len(data_to_write), errors) #confirmation

    if submissions_scanned_f != None and submissions_scanned != None:
        with open(submissions_scanned_f, "w") as f:
            for i in submissions_scanned:
                try:
                    f.write("{}\n".format(i))

                except Exception as e:
                    print "Failed to write already scanned ID: {}.".format(i)
                    raise

def update(words, db):
    """
    ---------------------------------------------------------------------------
    Update dictionary values. (returns: updated dictionary)
    *arguments: (2) List words, Dictionary db
    ---------------------------------------------------------------------------
    """
    local_db = {}
    local_db = db
    for word in words:
        try:
            local_db[str(word)] += 1 #Update entry
        except Exception as e:
            local_db[str(word)] = 1 #Create entry

    return local_db

def filtrate(text):
    """
    ---------------------------------------------------------------------------
    Remove punctuation, digits and newlines from input string. (returns: list)
    *arguments: (1) String text
    ---------------------------------------------------------------------------
    """
    exclude = ["\n", string.digits, string.punctuation]
    filtered = text
    for exclusion_set in exclude:
        filtered = "".join(
        ch.lower() for ch in filtered if ch not in exclusion_set)

    filtered = filtered.split()

    return filtered

def main():
    pass

if __name__ == "__main__":
    main()
