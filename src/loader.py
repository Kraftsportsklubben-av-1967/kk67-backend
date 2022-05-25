import os
import facebook as fb
import requests

graph_api_url = "https://graph.facebook.com/v13.0/{}{}/?access_token={}&fields={}&limit=25&after={}"

page_id = os.environ.get("FB_PAGE_ID")
user_id = os.environ.get("FB_USER_ID")
user_token = os.environ.get('FB_USER_KEY')
page_token =  os.environ.get('FB_PAGE_KEY')

graph_user = fb.GraphAPI(access_token=user_token, version="3.0")
graph_page = fb.GraphAPI(access_token=page_token, version="3.0")

def update_paging(page, edge):
  if "error" in page[edge]:
    return page

  if "previous" not in page[edge]["paging"]:
    page[edge]["paging"]["cursors"].pop("before", None)
  
  if "next" not in page[edge]["paging"]:
    page[edge]["paging"]["cursors"].pop("after", None)
  
  page[edge]["paging"].pop("next", None)
  page[edge]["paging"].pop("previous", None)

  return page

def load_posts_from_instagram(pagination_token):
  if pagination_token is None:
    return graph_user.get_object(id=user_id, fields="media{media_type, media_url, timestamp, permalink, caption, children{media_type, media_url}},profile_picture_url,name")

  # Restructure response to be the same as None case

  profile = graph_user.get_object(id=user_id, fields="profile_picture_url,name")
    
  page = requests.get(graph_api_url.format(user_id, '/media', user_token, "media_type, media_url, timestamp, permalink, caption, children{media_type, media_url}", pagination_token)).json()

  profile.update({"media": page})

  return profile 

def load_posts_from_facebook(pagination_token):
  if pagination_token is None:
    return graph_page.get_object(id=page_id, fields="posts{place,permalink_url,created_time,full_picture,id,attachments,message},picture,name")
  
  # Restructure response to be the same as None case

  profile = graph_page.get_object(id=page_id, fields="picture,name,id")
  
  page = requests.get(graph_api_url.format(page_id, '/posts', page_token, "place,permalink_url,created_time,full_picture,id,attachments,message", pagination_token)).json()

  profile.update({"posts": page})

  return profile

