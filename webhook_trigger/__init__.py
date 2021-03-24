import os
import time
import praw
import json
import pprint
import sqlite3
import markdown
import requests

# Import the framework
from flask import Flask
from pets_db import init_db, query_db
from logging.config import dictConfig

# Create a logging configuration for all logs
dictConfig({
  'version': 1,
  'formatters': {'default': {
    'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
  }},
  'handlers': {'wsgi': {
    'class': 'logging.StreamHandler',
    'stream': 'ext://flask.logging.wsgi_errors_stream',
    'formatter': 'default'
  }},
  'root': {
    'level': 'INFO',
    'handlers': ['wsgi']
  }
})

# Create an instance of Flask
app = Flask(__name__)

env_vars = "lostboyz"
community = "VictoriaBC"

reddit = praw.Reddit(env_vars)
subreddit = reddit.subreddit(community)

seen = []

init_db()

@app.route("/")
def index():
  """Render some documentation as a smoke test that we are up and running"""
  
  # Open the README file
  with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:
    
    # Read the content of the file
    content = markdown_file.read()

    # Convert to HTML
    return markdown.markdown(content)

def payload_factory(a_post):
  payload_dict = {
    "id": a_post.id,
    "locked": a_post.locked,
    "is_self": a_post.is_self,
    "post_hint": a_post.post_hint,
    "submission_name": a_post.name,
    "link_flair_text": a_post.link_flair_text,
    "submission_author_name": a_post.author.name,
    "url": a_post.url,
    "title": a_post.title,
    "preview": a_post.preview
  }
  return payload_dict 

def trigger_webhook():
  with app.app_context():
    for item in query_db('select * from lost_pets_submissions'):
      if item is not None:
        seen.append(item['submission_id'])

    for submission in subreddit.new(limit=None):
      payload = {}
      """
        Skip submissions without a post_hint they tend not to have a preview
      """
      keys = dir(submission)
      if submission.link_flair_text == "Lost & Found" and "post_hint" in keys:

        print("=============>>>>>>>>>>>> DEBUG 1")
        print(os.environ)
        print(os.environ['WEBHOOK_SRV_URL'])
        pprint.pprint(vars(payload_factory(submission)))
        print("<<<<<<<<<<<<<<============ DEBUG 1")

        pprint.pprint(vars(submission))
        r = requests.post(os.environ['WEBHOOK_SRV_URL'], json = payload_factory(submission))
        if r.status_code != requests.codes.created:
          r.raise_for_status()
        else:
          seen.append(submission.id)
          inserted = False
          query_db('INSERT INTO lost_pets_submissions (submission_id) VALUES (?)', [submission.id], one=True)
          for entry in query_db('select * from lost_pets_submissions'):
            if entry['submission_id'] == submission.id:
              inserted = True
              print (submission.id + ' was saved')      
          if inserted is not True:
            app.logger.info('submission id: %s was not saved', submission.id)

while True:
  trigger_webhook()
  time.sleep(60) # Run trigger webhook once per minute