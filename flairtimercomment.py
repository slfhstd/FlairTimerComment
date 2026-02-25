import praw

import praw
import os
import os.path
import json
import time

# Create default config/config.py if it doesn't exist
default_config_path = os.path.join('config', 'config.py')
if not os.path.exists(default_config_path):
    os.makedirs('config', exist_ok=True)
    with open(default_config_path, 'w') as f:
        f.write(
            'username = ""\n'
            'password = ""\n'
            'client_id = ""\n'
            'client_secret = ""\n'
            'user_agent = "Flair Timer Comment Bot"\n'
            '\n'
            '# Subreddits\n'
            'subreddit = ""\n'
            'flair_text = "Waiting for OP"\n'
            'interval = 30\n'
            'hours = 48\n'
            'searchlimit = 600\n'
            'comment_message = ""\n'
            'lock_post = False\n'
            'distinguish_sticky = False\n'
        )

import config
def authentication():
    print ("Authenticating...")
    reddit = praw.Reddit(username = config.username,
            password = config.password,
            client_id = config.client_id,
            client_secret = config.client_secret,
            user_agent = config.user_agent)
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
                # Optionally lock the post if configured
                if getattr(config, 'lock_post', False):
                    try:
                        reddit.submission(submission).mod.lock()
                    except Exception as e:
                        print(f"Could not lock submission: {e}")

                comment = reddit.submission(submission).reply(body=config.comment_message)
                try:
                    sticky = getattr(config, 'distinguish_sticky', False)
                    if sticky:
                        comment.mod.distinguish(how="yes", sticky=True)
                    else:
                        comment.mod.distinguish(how="yes")
                    print(f"Distinguished comment (sticky={sticky})")
                except Exception as e:
                    print(f"Could not distinguish comment: {e}")
                print(f"Post {submission} has been flaired {config.flair_text} for {config.hours} hours, posted comment")
                break
 
        save_posts(posts)
        time.sleep(config.interval)
 
def load_posts():
    if not os.path.exists("config/posts.json"):
        with open("config/posts.json", "w+") as file:
            json.dump({}, file)
    with open("config/posts.json", "r+") as file:
        data = json.load(file)
        return data
 
def save_posts(data):
    with open('config/posts.json', 'w+') as file:
        json.dump(data, file)
 
 
while True:
    try:
        posts = load_posts()
        main(reddit = authentication(), posts = posts)
    except Exception as e:
        print(e)
