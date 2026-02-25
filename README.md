
# Flair Timer Comment Bot

This is a Reddit bot that monitors a subreddit for posts with a specific link flair. When a post keeps that flair for a set number of hours, the bot:

1. Saves the submission
2. Optionally locks the post
3. Leaves a configurable comment
4. Can distinguish and/or sticky its own comment

This is useful in communities where flairing a post starts a timer (for example, "Waiting for OP"). After the timer expires, the bot comments as a reminder.

---

## Features

- Configurable subreddit, flair text, and scan interval
- Tracks posts in `config/posts.json` so it survives restarts
- Optional post locking and moderator comment stickiness
- Can run as a Python script or in Docker

---

## Configuration

Configuration is set in a Python file. Edit `config/config.py` or provide another `config.py` on your `PYTHONPATH`. The shim at the repository root will find it.

Required settings:

```python
username = ""          # Reddit account used by the bot
password = ""          # account password
client_id = ""         # API credentials from https://www.reddit.com/prefs/apps
client_secret = ""     #
user_agent = "Flair Timer Comment Bot"

subreddit = ""         # e.g. "INEEEEDIT" or "All"
flair_text = "Waiting for OP"  # flair text to watch for (case sensitive)

comment_message = ""   # text to post when the timer expires
``` 


Optional settings (defaults shown):

```python
interval = 30            # seconds between subreddit scans
hours = 48               # how long the flair must remain on a post
searchlimit = 600        # how many recent posts to examine (max 1000)
lock_post = False        # lock the submission after commenting?
distinguish_sticky = False  # distinguish and/or sticky the bot's comment?
``` 


The bot keeps a simple JSON file at `config/posts.json`. This directory must be writeable.


---

## Manual Installation & Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/slfhstd/FlairTimerComment.git
   cd FlairTimerComment
   ```

2. Create or edit configuration:
   Populate `config/config.py` as shown above.

3. Install dependencies:
   Make sure Python 3.8+ is installed, then run:
   ```bash
   pip install praw
   ```

4. Start the bot:
   ```bash
   python flairtimercomment.py
   ```

   The script will authenticate and begin looping. Logs are printed to stdout.

---

## Running with Docker

### Build and run locally

1. Build the image:
   ```bash
   docker build -t flairtimercomment .
   ```

2. Create a local configuration directory:
   ```bash
   mkdir -p /some/path/flairtimercomment/config
   cp config/config.py /some/path/flairtimercomment/config/
   ```

3. Run the container:
   ```bash
   docker run -d --name flairtimer --restart unless-stopped \
       -v /some/path/flairtimercomment/config:/app/config \
       flairtimercomment
   ```

   The volume mount ensures your `config.py` and `posts.json` persist outside the container.

### Pull a prebuilt image

An image is published to GitHub Container Registry (example tag `ghcr.io/slfhstd/flairtimercomment:latest`). Use that instead of building locally:

```bash
docker pull ghcr.io/slfhstd/flairtimercomment:latest
docker run -d --name flairtimer ... (same volume flags as above) ghcr.io/slfhstd/flairtimercomment:latest
```

---

## Docker Compose

A sample `docker-compose.yml` is provided:

```yaml
services:
  app:
    image: ghcr.io/slfhstd/flairtimercomment:latest
    container_name: FlairTimerBot
    restart: unless-stopped
    volumes:
      - /docker/data/flairtimercomment:/app/config
```

Adjust the `volumes` path to point at a directory on the host containing your `config.py`.

Start the stack with:

```bash
docker compose up -d
```

or, if you are using the old binary name:

```bash
docker-compose up -d
```

The configuration and state files are persisted under the mounted directory.

---

## Notes & Tips

- Run the bot as a dedicated Reddit account with appropriate moderator permissions if you intend to lock posts.
- `searchlimit` may be raised if the subreddit is busy and posts with the target flair frequently appear deep in the new queue.
- Logs are simple `print` statements; consider redirecting stdout to a file or use a process supervisor in production.

---


