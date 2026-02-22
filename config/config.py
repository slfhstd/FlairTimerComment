username = ""
password = ""
client_id = ""
client_secret = ""
 
#Subreddits
subreddit = "" # "INEEEEDIT" "Ofcoursethatsathing" "All"
 
flair_text = "Waiting for OP" # Case Sensitive
 
interval = 30 # How often should the bot scan the subreddit for these posts, in seconds. Higher = slower/less accurate/save resources, lower = faster/more accurate/use more resources.
 
hours = 48 # How many hours must the flair been on the post to send the notification
 
searchlimit = 600 # Max: 1000, this should only be limited to save on resources. The bot sorts by new and if it isn't catching posts that are being changed to the flair simply because they are too old (say the 301st post on the subreddit is changed to the flair) then increase this limit.

# Comment message to post on old posts
comment_message = "Hello OP! It has been at least __2 days__ since you last replied to your post. \n\n Please update your post in one of the following ways; \n\n * Reply to any relevant comments you haven't replied to yet. \n * [Mark your post solved](https://www.reddit.com/r/MinecraftHelp/wiki/rules/#wiki_7._points_sytem_rules), if your issue is fixed.\n\n \n __If you do not update your post within *7 days* you may receive a short ban.__ \n\n _Please note: Deleting this post, without marking it solved, is against [our rules](https://www.reddit.com/r/MinecraftHelp/wiki/rules/#wiki_7._points_sytem_rules)._ \n"

# Whether the bot should distinguish the posted comment (True/False)
distinguish_comment = True
