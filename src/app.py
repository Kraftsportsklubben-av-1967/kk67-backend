from flask import Flask, json
from flask_caching import Cache
import os
from flask_cors import CORS
import facebook as fb

config = {
  "CACHE_TYPE": "SimpleCache",
  "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)
CORS(app)

app.config["CORS_ORIGINS"] = ["https://www.kk-67.com", "http://localhost:3000"]
app.config.from_mapping(config)
cache = Cache(app)

page_id = os.environ.get("FB_PAGE_ID")
user_id = os.environ.get("FB_USER_ID")
user_token = os.environ.get('FB_USER_KEY')
page_token =  os.environ.get('FB_PAGE_KEY')

graph_user = fb.GraphAPI(access_token=user_token, version="3.0")
graph_page = fb.GraphAPI(access_token=page_token, version="3.0")

@app.get("/")
def health():
  return "Flask server running on Python 3.9"


@app.get("/posts/fb")
@cache.cached(timeout=300)
def get_fb_posts():
  page = graph_page.get_object(id=page_id, fields="posts{place,permalink_url,created_time,full_picture,id,attachments,message},picture,name")

  paging = page["posts"].pop("paging", None) # remove paging for now since it reveals api key
  return page

@app.get("/posts/ig")
@cache.cached(timeout=300)
def get_ig_posts():
  page = graph_user.get_object(id=user_id, fields="media{media_type, media_url, timestamp, permalink, caption, children{media_type, media_url}},profile_picture_url,name")

  paging = page["media"].pop("paging", None) # remove paging for now

  return page
