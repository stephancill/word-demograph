import argparse
import praw
import sys
import time
import wdbm


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target",
                        help="targeted subreddit",
                        default="all")
    parser.add_argument("-n", "--posts",
                        help="number of posts to fetch",
                        default=5, type=int)
    args = parser.parse_args()

    target_sub = args.target
    submission_count = args.posts

    database_name = "db_{}.db".format(target_sub)
    database = {}
    submissions_scanned_f = "submissions_scanned.txt"
    database, submissions_scanned = wdbm.load(database_name,
                                              submissions_scanned_f)

    r = praw.Reddit(user_agent='''Documenting Reddit vocabulary.
                                by /u/tookieewooper''')
    subreddit = r.get_subreddit(target_sub)
    try:
        submissions = subreddit.get_top_from_day(limit=submission_count)
        print "Fetched {} submissions from {}.".format(submission_count,
                                                       target_sub)
    except Exception as e:
        print "Couldn't fetch submissions from {}.".format(target_sub)

    for submission in submissions:
        if submission.id not in submissions_scanned:
            flat_comments = praw.helpers.flatten_tree(submission.comments)
            already_done = set()
            for comment in flat_comments:
                if comment.id not in already_done:
                    if "praw.objects.Comment" in str(type(comment)):
                        if str(comment) != None:
                            database = wdbm.update(wdbm.filtrate(str(comment)),
                                                   database)
                            already_done.add(comment.id)
            submissions_scanned.append(submission.id)
            print "SECCESSFULLY COUNTED: {}- '{}'".format(submission.id,
                                                          str(submission)[:40])
        else:
            print "ALREADY COUNTED: {}- '{}'".format(submission.id,
                                                     str(submission)[:40])

    wdbm.write(database, database_name,
               submissions_scanned_f, submissions_scanned)

if __name__ == "__main__":
    main()
