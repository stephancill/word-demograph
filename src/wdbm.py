#Word Database Manager
"""Usage:
1. Load database into dictionary with load()
2a. Filter through input text and isolate words with filtrate()
2b. Update dictionary values with update()
3. Finally write the dictionary back to database file with write()
"""
import string

__author__ = "Stephan Cilliers <stephanus.cilliers@gmail.com> "
default_db_name = "database.db"

def load(dbname=default_db_name):
    """
    ---------------------------------------------------------------------------
    Load database text file into dictionary. (returns: dictionary)
    *arguments: (1) File dbname
    ---------------------------------------------------------------------------
    """
    try:
        with open(dbname,"r") as f:
            tmp_db = {}
            try:
                for line in f:
                    (w, c) = line.split()
                    tmp_db[w] = int(c)
            except Exception as e:
                print "Database empty, loading anyway."
    except Exception as e:
        print "Database file not found, creating '{}'.".format(dbname)
        with open(dbname,"w") as f:
            tmp_db = {}
            pass

        return tmp_db

def write(db, dbname=default_db_name):
    """
    -----------------------------------------------------------------------
    Write dictionary to database text file. (returns: Confirmation)
    *arguments: (2) File dbname, Dictionary db
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
        return "Completed write with {} errors.".format(errors) #confirmation

def update(words, db):
    """
    ---------------------------------------------------------------------------
    Update dictionary values. (returns: updated dictionary)
    *arguments: (2) List words, Dictionary db
    ---------------------------------------------------------------------------
    """
    local_db = db
    for word in words:
        try:
            local_db[word] += 1
            # return "'{}' found, count updated.".format(word)
        except Exception as e:
            local_db[word] = 1
            # return "'{}' not found, added.".format(word)

    return local_db

def filtrate(text):
    """
    ---------------------------------------------------------------------------
    Remove punctuation, digits and newlines from input string. (returns: list)
    *arguments: (1) String text
    ---------------------------------------------------------------------------
    """
    exclude = ["\n", string.digits, string.punctuation]
    for exclusion_set in exclude:
        filtered = "".join(ch.lower() for ch in text if ch not in exclusion_set)

    return filtered.split()

def main():
    content = []
    database_name = "database.db"
    inputfile_name = "input.txt"
    with open(inputfile_name, "r") as inputf:
        for line in inputf:
            content.append(line)
    content = filtrate(" ".join(content))
    database = load(database_name)
    database = update(content, database)
    write(database_name, database)

if __name__ == "__main__":
    main()
