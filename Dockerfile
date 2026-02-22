FROM python:3.14-slim

WORKDIR /app

# Copy application files
COPY config.py .
COPY flairtimercomment.py .

# Install dependencies
RUN pip install --no-cache-dir praw 

ENV PYTHONUNBUFFERED=1

# Run the script
CMD ["python", "flairtimercomment.py"]


