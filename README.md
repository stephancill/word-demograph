# word-demograph
Script that processes comments in threads and creates a database of word usage demographics.

#Requirements:
* Python == 2.7
* virtualenv => 13.1.2

(additional dependencies listed in `requirements.txt`)

#Set up in virtualenv:
1. `git clone https://github.com/stephancill/word-demograph.git` (Clone this repo)
2. `virtualenv word-demograph` (Create a virtualenv in its directory)
3. `source word-demograph/bin/activate` or `word-demograph\Scripts\activate` for Windows users. (Activate virtual environment. Use `deactivate` to deactivate the virtual environment.)
4. `cd word-demograph`
5. `pip install -r requirements.txt` (Install all requirements)
6. `cd src`
7. See usage.

#Usage:
* `python main.py -t [target_subreddit] -n [number_of_posts]`
(e.g. `python main.py all` targets /r/all.)
* Output is sent to `db_[target_sub].db` in `word-demograph/databases`
* `python main.py --help` for more usage commands.

###Please note that `main.py` must be run from within the `src/` directory.
