import praw
import config
import os.path
import json
import time
 
def authentication():
    print ("Authenticating...")
    reddit = praw.Reddit(username = config.username,
            password = config.password,
            client_id = config.client_id,
            client_secret = config.client_secret,
            user_agent = "Waiting For OP Flair Timer Running On MinecraftHelpModTeam")
    print ("Authenticated as {}.".format(reddit.user.me()))
    return reddit
 
def main(reddit, posts: dict):
    while True:
        for submission in reddit.subreddit(config.subreddit).new(limit=config.searchlimit):
            if not submission.saved:
                if submission.id not in posts.keys() and submission.link_flair_text == config.flair_text:
                    posts[submission.id] = time.time()
                    print(f"Post {submission} has been flaired {config.flair_text}")
                if submission.id in posts.keys() and submission.link_flair_text != config.flair_text:
                    posts.pop(submission.id)
                    print(f"Post {submission} has been unflaired {config.flair_text}")
 
        for submission in posts:
            if time.time() > posts[submission] + (config.hours * 60 * 60):
                posts.pop(submission)
                reddit.submission(submission).save()
                reddit.submission(submission).reply(body="Hello OP! It has been at least __2 days__ since you last replied to your post. \n\n Please update your post in one of the following ways; \n\n * Reply to any relevant comments you haven't replied to yet. \n * [Mark your post solved](https://www.reddit.com/r/MinecraftHelp/wiki/rules/#wiki_7._points_sytem_rules), if your issue is fixed.\n\n \n __If you do not update your post within *7 days* you may receive a short ban.__ \n\n _Please note: Deleting this post, without marking it solved, is against [our rules](https://www.reddit.com/r/MinecraftHelp/wiki/rules/#wiki_7._points_sytem_rules)._ \n").mod.distinguish(how="yes")
                print(f"Post {submission} has been flaired {config.flair_text} for {config.hours} hours, posted comment")
                break
 
        save_posts(posts)
        time.sleep(config.interval)
 
def load_posts():
    if not os.path.exists("posts.json"):
        with open("posts.json", "w+") as file:
            json.dump({}, file)
    with open("posts.json", "r+") as file:
        data = json.load(file)
        return data
 
def save_posts(data):
    with open('posts.json', 'w+') as file:
        json.dump(data, file)
 
 
while True:
    try:
        posts = load_posts()
        main(reddit = authentication(), posts = posts)
    except Exception as e:
        print(e)
