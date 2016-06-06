import argparse
import logging
import praw
import sys
import time
import wdbm
from tqdm import tqdm

class RedditWDBM(object):
    """
    ---------------------------------------------------------------------------
    Processes comments in reddit threads and creates a database of word usage
    demographics.
    ---------------------------------------------------------------------------
    """

    def __init__(self, target, merge, post_count=5):
        self.target_sub = target
        self.post_count = post_count
        self.mergefiles = merge


    def main(self):
        """
        Start processing.
        """
        logging.basicConfig(format="%(levelname)s:%(message)s",
                            filename="{}.log".format(__name__),
                            level=logging.DEBUG)

        if self.target_sub:
            database_name = "db_{}.db".format(self.target_sub)
            scanned_f = "ss_{}.txt".format(self.target_sub)
            tmp_database = {}
            tmp_scanned = []
            tmp_database, tmp_scanned = wdbm.load(database_name, scanned_f)

            r = praw.Reddit(user_agent='''Documenting Reddit vocabulary.
                                        by /u/tookieewooper''')
            subreddit = r.get_subreddit(self.target_sub)
            try:
                submissions = subreddit.get_top_from_month(limit=self.post_count+1)
                logging.info("Fetched {0} submissions from {1}.".format(self.post_count,
                                                                      self.target_sub))
            except praw.errors.InvalidSubreddit as e:
                sys.exit("Couldn't fetch submissions from {}.".format(self.target_sub))

            for submission in tqdm(submissions):
                if submission.id not in tmp_scanned:
                    flat_comments = praw.helpers.flatten_tree(submission.comments)
                    already_done = set()
                    for comment in flat_comments:
                        if comment.id not in already_done:
                            if "praw.objects.Comment" in str(type(comment)):
                                if str(comment) is not None:
                                    database = wdbm.update(wdbm.filtrate(str(comment)),
                                                           tmp_database)
                                    already_done.add(comment.id)

                    tmp_scanned.append(submission.id)
                    print "SECCESSFULLY COUNTED: {0}- '{1}'".format(submission.id,
                                                                  str(submission)[:40])
                else:
                    print "ALREADY COUNTED: {0}- '{1}'".format(submission.id,
                                                             str(submission)[:40])

            wdbm.write(
                       tmp_database,
                       database_name,
                       scanned_f,
                       tmp_scanned
                      )

        if self.mergefiles is not None:
            wdbm.merge(self.mergefiles)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target",
                        help="targeted subreddit")
    parser.add_argument("-n", "--posts",
                        help="number of posts to fetch",
                        default=5, type=int)
    parser.add_argument("--merge", help="merge a list of files",
                        nargs="+")
    args = parser.parse_args()

    if not (args.target or args.merge):
        parser.error("No action requested, add --target or --merge")

    manager = RedditWDBM(args.target, args.merge, args.posts)
    manager.main()
