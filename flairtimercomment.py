
import praw
import os
import os.path
import json
import time


# Helper to get env var or default
def env_or_default(var, default):
    return os.environ.get(var, default)

# Create config/config.py from environment if missing or empty
default_config_path = os.path.join('config', 'config.py')
def write_config_from_env():
    os.makedirs('config', exist_ok=True)
    with open(default_config_path, 'w') as f:
        f.write(
            f'username = "{env_or_default("USERNAME", "")}"\n'
            f'password = "{env_or_default("PASSWORD", "")}"\n'
            f'client_id = "{env_or_default("CLIENT_ID", "")}"\n'
            f'client_secret = "{env_or_default("CLIENT_SECRET", "")}"\n'
            f'user_agent = "{env_or_default("USER_AGENT", "Flair Timer Comment Bot")}"\n'
            '\n'
            f'subreddit = "{env_or_default("SUBREDDIT", "")}"\n'
            f'flair_text = "{env_or_default("FLAIR_TEXT", "Waiting for OP")}"\n'
            f'interval = {env_or_default("INTERVAL", "30")}\n'
            f'hours = {env_or_default("HOURS", "48")}\n'
            f'searchlimit = {env_or_default("SEARCHLIMIT", "600")}\n'
            f'comment_message = "{env_or_default("COMMENT_MESSAGE", "")}"\n'
            f'lock_post = {env_or_default("LOCK_POST", "False")}\n'
            f'distinguish_sticky = {env_or_default("DISTINGUISH_STICKY", "False")}\n'
        )
    print(f"Configuration file auto-populated from environment variables at {default_config_path}.")

# Check if config file exists and is non-empty, else generate from env
def config_needs_populating():
    if not os.path.exists(default_config_path):
        return True
    try:
        with open(default_config_path, 'r') as f:
            content = f.read().strip()
            return len(content) == 0
    except Exception:
        return True
    
if config_needs_populating():
    write_config_from_env()
    # Optionally exit after populating, or continue to run

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
