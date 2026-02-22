FROM python:3.14-slim

# Copy application files
WORKDIR /config
COPY scripts ./scripts
COPY config.py .
COPY flairtimercomment.py .

# Add execute permissions to the scripts
RUN chmod +x /config/scripts/start_bot.sh
RUN chmod +x /config/scripts/autorun.sh 
RUN chmod +x /config/scripts/copy.sh

# Create App directory
RUN mkdir /app
# Install dependencies
RUN pip install --no-cache-dir praw 

ENV PYTHONUNBUFFERED=1

# Run the script
CMD ["sh", "/config/scripts/autorun.sh"]


