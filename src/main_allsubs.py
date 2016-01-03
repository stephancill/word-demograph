import wdbm
import main

def main():
    """Recursively run reddit comment parser for top 1000 posts of all time on
    every subreddit in subreddits.txt"""
    subs = []
    with open("subreddits.txt", "r") as f:
        for line in f:
            subs.append("".join(wdbm.filtrate(line))[1:])

    for subreddit in subs:
        mgr = main.RedditWDBMS(subreddit, 1000)
        mgr.main()

if __name__ == "__main__":
    main()
