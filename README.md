# word-demograph
Script that processes comments in threads and creates a database of word usage demographics.

#Requirements:
* Python == 2.7
* virtualenv => 13.1.2

(additional dependencies listed in `requirements.txt`)

#Set up in virtualenv:
1. `git clone https://github.com/stephancill/word-demograph.git` (Clone this repo)
2. `virtualenv word-demograph` (Create a virtualenv in its directory)
3. `source word-demograph/bin/activate` or `word-demograph\Scripts\activate` for
Windows users. (Activate virtual environment. Use `deactivate` to deactivate the
 virtual environment.)
4. `cd word-demograph`
5. `pip install -r requirements.txt` (Install all requirements)
6. `cd src`
7. See usage.

#Usage:
* `python main.py -t [target_subreddit] -n [number_of_posts]`
(e.g. `python main.py -t all` targets /r/all.)
* `python main.py --merge db_[dbname1].db db_[dbname2].db db_[dbnameN].db` to
merge files.
* Output is sent to `db_[target_sub].db` in `word-demograph/databases`
* `python main.py --help` for more usage commands.
* To gather data from the top 100 subreddits autonomously, run
`python main_allsubs.py`

###Please note that all scripts must be run from within the `src/` directory.
