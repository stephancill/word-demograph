# word-demograph
Reddit bot that processes comments in threads and creates a database of word usage demographics.

#Running:
1. `git clone https://github.com/stephancill/word-demograph.git` (Clone this repo)
2. `virtualenv word-demograph` (Create a virtualenv in its directory)
3. `source word-demograph/bin/activate` (Activate virtual environment)
3. `cd word-demograph`
4. `pip install -r requirements.txt` (Install all requirements)
5. `cd src`
6. `python main.py` (Run `main.py` from within script directory to avoid file miscreation)

#Usage
* Change `target_sub` in line 7 of `main.py` to subreddit of choice.
