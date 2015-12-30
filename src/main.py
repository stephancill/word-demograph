import praw
import time
import tqdm
import wdbm


def main():
    # content = []
    database_name = "askreddit.db"
    database = wdbm.load(database_name)
    r = praw.Reddit(user_agent=
    'Documenting Reddit vocabulary.by /u/tookieewooper')
    subreddit = r.get_subreddit("askreddit")
    try:
        submissions = subreddit.get_top_from_day(limit=5)
        print "Fetched submissions"
    except Exception as e:
        print "Couldn't fetch posts, waiting 10 seconds before retrying."
        time.sleep(10)

    for submission in submissions:
        submission_ = submission
        print "submission_.replace_more_comments(limit=None, threshold=0)"
        submission_.replace_more_comments(limit=None, threshold=0)
        print "flat_comments = praw.helpers.flatten_tree(submission_.comments)"
        flat_comments = praw.helpers.flatten_tree(submission_.comments)
        # already_done = set()
        # print type(flat_comments)
        # for comment in flat_comments:
        #     if comment.id not in already_done:
        #         print comment[:5]
        #         # database = wdbm.update(wdbm.filtrate(comment), database)
        #         # already_done.add(comment.id)
        # print "Successfully counted words in {}".format(submission)

    # write(database_name, database)


if __name__ == "__main__":
    main()
