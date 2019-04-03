# -*- coding: utf-8 -*-

import os
import datetime
import json

import google.oauth2.credentials

import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from oauth2client import client # Added
from oauth2client import tools # Added
from oauth2client.file import Storage # Added

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "/disk/data/share/MTproject/client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
now = datetime.datetime.now()

def get_authenticated_service():
    credential_path = os.path.join('./', '/disk/data/share/MTproject/credential_sample.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRETS_FILE, SCOPES)
        credentials = tools.run_flow(flow, store)
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def print_response(response):
  print(response)

# Build a resource based on a list of properties given as key-value pairs.
# Leave properties with empty values out of the inserted resource.
def build_resource(properties):
  resource = {}
  for p in properties:
    # Given a key like "snippet.title", split into "snippet" and "title", where
    # "snippet" will be an object and "title" will be a property in that object.
    prop_array = p.split('.')
    ref = resource
    for pa in range(0, len(prop_array)):
      is_array = False
      key = prop_array[pa]

      # For properties that have array values, convert a name like
      # "snippet.tags[]" to snippet.tags, and set a flag to handle
      # the value as an array.
      if key[-2:] == '[]':
        key = key[0:len(key)-2:]
        is_array = True

      if pa == (len(prop_array) - 1):
        # Leave properties without values out of inserted resource.
        if properties[p]:
          if is_array:
            ref[key] = properties[p].split(',')
          else:
            ref[key] = properties[p]
      elif key not in ref:
        # For example, the property is "snippet.title", but the resource does
        # not yet have a "snippet" object. Create the snippet object here.
        # Setting "ref = ref[key]" means that in the next time through the
        # "for pa in range ..." loop, we will be setting a property in the
        # resource's "snippet" object.
        ref[key] = {}
        ref = ref[key]
      else:
        # For example, the property is "snippet.description", and the resource
        # already has a "snippet" object.
        ref = ref[key]
  return resource

# Remove keyword arguments that are not set

def remove_empty_kwargs(**kwargs):
  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.items():
      if value:
        good_kwargs[key] = value
  return good_kwargs

def videos_list_most_popular(client, **kwargs):
  # See full sample for function
  kwargs = remove_empty_kwargs(**kwargs)

  response = client.videos().list(
    **kwargs
  ).execute()
  return response

def video_categories_list():
  categories = { '1' : 'Film & Animation', '2' : 'Cars & Vehicles', '10' : 'Music', '15' : 'Pets & Animals',
            '17' : 'Sport', '19' : 'Travel & Events', '20' : 'Gaming', '22' : 'People & Blogs', '23' : 'Comedy',
            '24' : 'Entertainment', '25' : 'News & Politics', '26' : 'How-to & Style', '27' : 'Education',
            '28' : 'Science & Technology', '29' : 'Non-profits & Activism'}

  return categories

def write_video_info(response):
    # Write video info to JSON file
    categories = video_categories_list()
    for i in range(0, len(response['items'])) :
        categoryId = response['items'][i]['snippet']['categoryId']
        if (categoryId in categories.keys()) :
            category = categories[categoryId]
            newpath = r"/disk/data/share/MTproject/" + category
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            filename = os.path.join(newpath, str(now) + '.json')
            if (not os.path.exists(filename)) :
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump([], f)
          #    print("https://www.youtube.com/watch?v=" + (response['items'][i]['id']) + "\n" + (response['items'][i]['snippet']['title']) + "\n" +
          #       (response['items'][i]['snippet']['description'])  + "\n")
            with open(filename, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            with open(filename, mode='w', encoding='utf-8') as f:
                URL = "https://www.youtube.com/watch?v=" + (response['items'][i]['id'])
                entry = {}
                entry["URL"] = URL
                entry["Title"] = (response['items'][i]['snippet']['title'])
                entry["Description"] = response['items'][i]['snippet']['description']
                json_data.append(entry)
                json.dump(json_data, f)
    nextPageToken = response.get("nextPageToken")
    return nextPageToken


if __name__ == '__main__':
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
  client = get_authenticated_service()

  video_categories = video_categories_list()

# Get most international most popular chart
for cat_id,cat_name in video_categories.items() :
   response = videos_list_most_popular(client,
     part='snippet,contentDetails,statistics',
     chart='mostPopular',
     regionCode='',
     maxResults=50,
     videoCategoryId=cat_id)

   nextPageToken = write_video_info(response)

   # Paging through results
   while nextPageToken:
     response = videos_list_most_popular(client,
       part='snippet,contentDetails,statistics',
       chart='mostPopular',
       regionCode='',
       maxResults=50,
       videoCategoryId=cat_id,
       pageToken=nextPageToken)
     nextPageToken = write_video_info(response)
