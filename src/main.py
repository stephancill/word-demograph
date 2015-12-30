import praw
import time
# import tqdm
import wdbm


def main():
    # content = []
    database_name = "askreddit.db"
    database = {}
    database = wdbm.load(database_name)
    r = praw.Reddit(user_agent=
    'Documenting Reddit vocabulary.by /u/tookieewooper')
    subreddit = r.get_subreddit("askreddit")
    try:
        submissions = subreddit.get_top_from_day(limit=5)
        print "Fetched submissions."
    except Exception as e:
        print "Couldn't fetch posts, waiting 10 seconds before retrying."
        time.sleep(10)
        submissions = subreddit.get_top_from_day(limit=5)

    for submission in submissions:
        flat_comments = praw.helpers.flatten_tree(submission.comments)
        print "Flattened comments."
        already_done = set()
        for comment in flat_comments:
            if comment.id not in already_done:
                if "praw.objects.Comment" in str(type(comment)) and str(comment) != None:
                    # print type(comment)
                    database = wdbm.update(wdbm.filtrate(str(comment)), database)
                    already_done.add(comment.id)
        print "Successfully counted words in {}".format(submission)

    wdbm.write(database, database_name)


if __name__ == "__main__":
    main()
