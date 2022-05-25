from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
from loader import load_posts_from_instagram, load_posts_from_facebook, update_paging

config = {
  "CACHE_TYPE": "SimpleCache",
  "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)
CORS(app)

app.config["CORS_ORIGINS"] = ["https://www.kk-67.com", "http://localhost:3000"]
app.config.from_mapping(config)
cache = Cache(app)


@app.get("/")
def health():
  return "Flask server running on Python 3.9"

@app.get("/posts/fb/")
@app.get("/posts/fb/<page_id>")
@cache.cached(timeout=300)
def get_fb_posts(page_id=None):
  return update_paging(load_posts_from_facebook(page_id), "posts")


@app.get("/posts/ig/")
@app.get("/posts/ig/<page_id>")
@cache.cached(timeout=300)
def get_ig_posts(page_id=None):
  return update_paging(load_posts_from_instagram(page_id), "media")


if __name__ == "__main__":
  app.run()