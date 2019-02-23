# Honours Project

This branch deals with the YoutubeAPI side of the project.

## Set up

You must have credentials for the Youtube Data API and OAuth 2.0 authorization.
To obtain these please go through these instructions https://developers.google.com/youtube/v3/getting-started.

## Running on the server

When running any python code on the hawksworth server, you must activate python 3 first -

```source ./py3/bin/activate```

To install via pip with the virtual environment -

```py3/bin/pip install --user [packages]```

To run the script:

```python get_trending_videos_server.py```

This script will retrieve the 'most popular' chart for videos from the following categories:
* Film & Animation
* Cars & Vehicles
* Music
* Pets & Animals
* Sport
* Travel & Events
* Gaming
* People & Blogs
* Comedy
* Entertainment
* News & Politics
* How-to & Style
* Education
* Science & Technology
* Non-profits & Activism

The output is a file, named after the time the script was run in format `yyyy-mm-dd hh:mm:ss.json`. Inside the file,
the URL, title and description of each video are stored in JSON format.

## Setting up cron job on the server

There is currently several cron jobs running on the server:

```HOME=/tmp
0 * * * * /disk/data/share/MTproject/py3/bin/python /disk/data/share/MTproject/get_trending_videos_server.py
```
This crontab runs the `get_trending_videos_server.py` script every hour, at :00 minutes past the hour.

## trending_videos_statistics_server.py

This is a script that compares two files, input via command line like so:

```python trending_videos_statistics_server.py [filename1] [filename2] ```

The script returns a percentage detailing how many popular videos are the same, per category, for the two files. If one or both of the files does not exist, it returns 0. **For each filename, remember to escape any spaces in the filename with the \ character.**

## trending_videos_difference.py

This file takes two files as the command line argument, sorts them by newest, and returns two lists of URLS - 'add' symbolising the URLs appearing in the newest file that were not in the older file, and 'take' symbolising the URLs that are in older file, but no longer in the newer.

## xml_generation_server.py 

A script that generates an XML file of all videos from all categories, at the end of every day. The structure of it is as such; 

```<data><category><video><title><URL><description></video></category></data>```

There is a cron job set up to run this script:

```
45 23 * * * /disk/data/share/MTproject/py3/bin/python /disk/data/share/MTproject/xml_generation_server.py

```

## append_tweets_server.py

This script uses the Twitter Streaming API to continuously collect tweets for each video, until it has reached the maximum amount of tokens for one API key. It tags every tweet with the language of the tweet using the fastText model. There is a cron job set up to run every 3 hours, after the initial xml file generation. 

```
0 02-23/3 * * * /disk/data/share/MTproject/py3/bin/python /disk/data/share/MTproject/append_tweets_server.py

```

## FastText interpreter

The fastText (language identification) API is installed on the server - under directory fastText-0.1.0. Data has been pre trained on the model, so you just need to run 

``` ./fasttext predict langdetect.bin - ```

and type into the interpreter what you wish to tag by language.

## FastText language tagging 

The file ```language_tagger.py``` includes a method that tags any sentence with it's language using the fastText language identification model. **You must remove any '\n' characters for this to work on large amounts of text.**

To import the method, use ```from language_tagger import tag_language```
