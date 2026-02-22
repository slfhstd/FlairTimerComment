username = ""
password = ""
client_id = ""
client_secret = ""
user_agent = "Flair Timer Comment Bot"
 
#Subreddits
subreddit = "" # "INEEEEDIT" "Ofcoursethatsathing" "All"
 
flair_text = "Waiting for OP" # Case Sensitive
 
interval = 30 # How often should the bot scan the subreddit for these posts, in seconds. Higher = slower/less accurate/save resources, lower = faster/more accurate/use more resources.
 
hours = 48 # How many hours must the flair been on the post to send the notification
 
searchlimit = 600 # Max: 1000, this should only be limited to save on resources. The bot sorts by new and if it isn't catching posts that are being changed to the flair simply because they are too old (say the 301st post on the subreddit is changed to the flair) then increase this limit.

# Comment message to post on old posts
comment_message = ""

# Whether the bot should lock the post after posting the comment (True/False)
# Default is False to avoid accidental locking; set to True to enable locking.
lock_post = False

# Whether the distinguished comment should be stickied (True/False)
# Some subreddits may require `True` to keep moderator comments visible.
distinguish_sticky = False
