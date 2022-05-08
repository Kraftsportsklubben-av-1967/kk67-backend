import re
from urllib.request import Request
from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)


@app.get("/test")
def test():
  key =  os.environ.get('FB_USER_KEY')
  print(key)
  return "test"

@app.get("/posts")
def get_posts():
  token = os.environ.get('FB_USER_KEY')
  r = requests.get(f'https://graph.facebook.com/v13.0/284710781586877?fields=picture&access_token={token}')
  print(token)

  return r.json()