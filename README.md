# word-demograph
Reddit bot that processes comments in threads and creates a database of word usage demographics.

#Set up:
1. `git clone https://github.com/stephancill/word-demograph.git` (Clone this repo)
2. `virtualenv word-demograph` (Create a virtualenv in its directory)
3. `source word-demograph/bin/activate` (Activate virtual environment)
3. `cd word-demograph`
4. `pip install -r requirements.txt` (Install all requirements)
5. `cd src`
6. See usage.

#Usage
* `python main.py [target_subreddit]` (e.g. `python main.py all` targets /r/all.)
* Output is sent to `[target_sub].db` in `src/`

##Please note that `main.py` must be run from within the `src/` directory.
