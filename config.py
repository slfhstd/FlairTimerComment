username = ""
password = ""
client_id = ""
client_secret = ""
 
#Subreddits
subreddit = "" # "INEEEEDIT" "Ofcoursethatsathing" "All"
 
flair_text = "Waiting for OP" # Case Sensitive
 
interval = 30 # How often should the bot scan the subreddit for these posts, in seconds. Higher = slower/less accurate/save resources, lower = faster/more accurate/use more resources.
 
hours = 48 # How many hours must the flair been on the post to send the notification
 
messagetitle = "4 Day Old Post Notification" # Title of the modmail
 
searchlimit = 600 # Max: 1000, this should only be limited to save on resources. The bot sorts by new and if it isn't catching posts that are being changed to the flair simply because they are too old (say the 301st post on the subreddit is changed to the flair) then increase this limit.