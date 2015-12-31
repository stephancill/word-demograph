import praw
import time
import wdbm


def main():
    target_sub = "askreddit"
    database_name = "{}.db".format(target_sub)
    database = {}
    submissions_scanned_f = "submissions_scanned.txt"
    database, submissions_scanned = wdbm.load(database_name, submissions_scanned_f)
    r = praw.Reddit(user_agent=
    'Documenting Reddit vocabulary.by /u/tookieewooper')
    subreddit = r.get_subreddit(target_sub)
    try:
        submissions = subreddit.get_top_from_day(limit=5)
        print "Fetched submissions."
    except Exception as e:
        print "Couldn't fetch submissions."

    for submission in submissions:
        if submission.id not in submissions_scanned:
            flat_comments = praw.helpers.flatten_tree(submission.comments)
            print "Flattened comments."
            already_done = set()
            for comment in flat_comments:
                if comment.id not in already_done:
                    if "praw.objects.Comment" in str(type(comment)) and str(comment) != None:
                        database = wdbm.update(wdbm.filtrate(str(comment)), database)
                        already_done.add(comment.id)
            submissions_scanned.append(submission.id)
            print "SECCESSFULLY COUNTED: '{}– {}'".format(submission.id, str(submission)[7:27])
        else:
            print "ALREADY COUNTED: '{}– {}'".format(submission.id, str(submission)[7:27])

    wdbm.write(database, database_name, submissions_scanned_f, submissions_scanned)


if __name__ == "__main__":
    main()
