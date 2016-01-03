import wdbm
import main as m

def main():
    """Recursively run reddit comment parser for top 1000 posts of all time on
    every subreddit in subreddits.txt"""
    subs = []
    with open("subreddits.txt", "r") as f:
        for sub in f:
            subs.append(sub[:-1])

    for subreddit in subs:
        print subreddit
        mgr = m.RedditWDBM(subreddit, 1000)
        mgr.main()

if __name__ == "__main__":
    main()
