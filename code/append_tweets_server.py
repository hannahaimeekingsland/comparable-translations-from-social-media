# Import the necessary methods from tweepy library
import json
import time
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import os
from language_tagger import tag_language
import re
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from xml.dom import minidom
import fastText

# search_results = [[]]
# tweeno = 0

# Variables that contains the user credentials to access Twitter API
access_token = "542269909-oIJ1nciP9OvTJFiHbQzFlpAc1gzbWMVSjeoaWdev"
access_token_secret = "uKrSG8iEzrxO8nMxWtNwnTtUq2spe9TXinEJWH8Vcmfl8"
consumer_key = "F0hAT7yfesuxJkXDThao40NS3"
consumer_secret = "p8KBxW0noCWc4ydX3NGVzsxFwWis5gPXvEkMwY4zJAeob99pPl"

#List of tokens
access_token_list = ['542269909-oIJ1nciP9OvTJFiHbQzFlpAc1gzbWMVSjeoaWdev',
                     '542269909-79NIOk6Tl9LMSP4I6E0KqzX83zM9obRFk5Vw0fu1',
                     '542269909-sXfqbksrJlNGmZHYozcEAO20MVgdwxQR9EH7jDD4',
                     '542269909-AoslssQkaS3J7W7qWBOOHmem3StjNIzLAi7MY6c7',
                     '542269909-dkvo0HXBWn7e1sUSuQJlzJI89Kg2TT7YE2ROfKb2',
                     '542269909-Z5Iuylw7zG8uOGHnNIZeZvuWFURMP6WyJejXuBJT',
                     '542269909-CoKU0erjAVR2AQ36lt1dx976mCwmGf1d041VuJwd',
                     '542269909-1TyIN8i1evY3P2YWmP0yRjSZz8l45smjPtOQ4FL1',
                     '542269909-OGgZt9TIUzsXMFYqtW2q8dWQbZgeThw2WdNxFYXK',
                     '542269909-rvaPycTjv6kC6wxvCGqOtK2XDoBfLBQGDXCPlzLr']
access_token_secret_list = ['uKrSG8iEzrxO8nMxWtNwnTtUq2spe9TXinEJWH8Vcmfl8',
                            '1qfAgLogRGO7S4tF61dEkuchNG9yAytN86vZCarQxxo3e',
                            '4zik2lobcrHdVxY1V10laRNdmLF1yIu3x5QChfB4RuP9d',
                            'Y3bwXKbND7LBbQlldfoFy0dfDirP6h6kHyGiCLhIm71pL',
                            'cLsJNz3qNQgRqhmGBUeGTx2PBvT0Gw9mTRAZ9fOhQB4tC',
                            'Kwyw7CWWszrhpgiECHwpSYyPY0Mv0wKVXkBMljwHBHTsV',
                            'b1yxJsQsBHVR9vKZ4SJ1XtbovXsOrXURC7U7fKB6IBJj0',
                            'jyJ39RaT80RanJVYtUDHSAnZkaIuvf7IimgjzPcWrYvcs',
                            'Xn7jITswMXwzPmcg6nqCwvakRKPaR6a8POBp5OMe85f2z',
                            '0tOaSIVbwbMCTnPcntN0oiAjKOM6fMFr5PWXHbL5YtN2m']
consumer_key_list = ['F0hAT7yfesuxJkXDThao40NS3','r1Z3syfJvRHmWg2xcfVZryiIP',
                     'INgpbF5ZFRrlpz0zRqYBBTSTp', 'cF5dBZU3keQdAXlMW7MYU8sAr',
                     'l5zOytEjN2ymX8DyuF3ESgarp', 'sTESsdLnw26oHGVe0p5n5KfYg',
                     'xx98fJkAsHDUOvqe2vUCEj04l', 'Cl06oTfG6HLetZSyOpYKyb1Tb',
                     'DzNuIhBMSaBHgPLz9tXcMRzQZ', 'ifezTiP06SCOTnOmGsCKrk6ya']
consumer_secret_list = ['p8KBxW0noCWc4ydX3NGVzsxFwWis5gPXvEkMwY4zJAeob99pPl',
                        '5whrwrd8oP46EPX2KZ19bjRyW6D7mpp8qLeKo6WLcQZ95aZNOX',
                        'z4mvWkZBTdbxaHLLbm089eGBBo5rG5Pjq8AcetTb2Y3zzitiQd',
                        'PG0Q14spxRvFKCRpgEofKrlwdZLRPvBdoaQ5YQjVzFDtd9soCy',
                        'pEdjWM2uPAWInDHYQgEqIvocV0dyxkxSjetwI0MYY5GtHKCfye',
                        'tzBSno6ZiAqd0sS0baJvbzom2dd5zent1eggMDp0XoaKawtqLw',
                        'VpdlRTW5iBoobkE5fTiujr3rhjdPUZvRChXxHxG7aaYDleEXF2',
                        'yKP7rmrmqY5to9BZswpVYVxwmItJ6rX5MyGu615ySpmbNx9ovm',
                        'LjGwGfeIypU9AYwo59mwLnZmCzqXWNOvjE8Rxiiiu096Q98F3P',
                        'TJuRPNT22xSC9E0XO4bCQACaFR6xamfPzffVWWy8fS5vI1msA2']


#Reading and writing paths
path = '/disk/data/share/MTproject/'
pathwr = '/disk/data/share/MTproject/'

langdetect = fastText.load_model('/disk/data/share/MTproject/fastText/langdetect.bin')

# This is a basic listener that just prints received tweets to stdout.
'''class StdOutListener(StreamListener):

    def on_data(self, data):
        print (data)
        return True

    def on_error(self, status):
        print (status)'''

# This handles Twitter authetification and the connection to Twitter Search/Streaming API
# l = StdOutListener()
auth = OAuthHandler(consumer_key_list[0], consumer_secret_list[0])
auth.set_access_token(access_token_list[0], access_token_secret_list[0])

# print(consumer_key_list[0], consumer_secret_list[0], access_token_list[0], access_token_secret_list[0])

# Using search API instead of the Streaming API
# stream = Stream(auth, l)
api = API(auth)

# Getting the current date
now = datetime.now() - timedelta(1)
date = str(now).split()
filenm = path + str(date[0]) + '.xml'

# To make sure we don't cross the limit
count = 0

# To make sure we don't cross the list count
ctr = 1

tree = ET.parse(filenm)
root = tree.getroot()

for item in root.findall("category"):

    # print(str(items[0]))
    # print(str(date[0]))
    # Get all the videos for the category
    videonode = item.findall('video')

    # For each and every individual video
    for video in videonode:

        # All the tweets we already have
        tweelist = []

        # If we have not reached the parsing limit yet
        if count != 180:
            count = count + 1

            url = video.find("URL").text

            # Trying to find the tweetsnode if we already have tweets.
            tweetsnode = video.find("tweets")
            # print(tweetsnode)

            '''THIS IS FOR PARSING THE TWEETS FOR THE URL'''

            # The tweets
            search_results = []

            # Number of automated tweets
            autom = 0

            # Number of non automated tweets
            counter = 0

            # Getting the url in the format we want
            items = url.split("=")
            url = "youtu.be/" + items[1]
            print(count)
            print(url)

            # Storing 100 tweets to the respective index
            searchr = (api.search(q=url, count=100, tweet_mode='extended'))

            # Creating a list of the search results
            for i in searchr:
                search_results.append(i._json)

            '''END OF TWEETS PARSING'''

            '''THIS IS FOR APPENDING THE TWEETS'''

            # IF we haven't parsed any tweets yet, we don't have a tweets node
            if tweetsnode is None:
                print("NOT GOT")
                tnode = ET.SubElement(video, 'tweets')
                tweecount = str(0)
                tnode.set('number', tweecount)
            # Make sure we don't scrape duplicate tweets, create a list of already existing tweets
            else:
                print("appending list")
                tweetsnode = video.find("tweets")
                tlist = tweetsnode.findall("tweet")
                for t in tlist:
                    tweelist.append(t.text)

            # For all the tweets we got in the search results
            for tweet in search_results:

                # print('In for loop')
                tweetext = str(tweet["full_text"])
                tweelan = str(tweet["lang"])
                tweeid = str(tweet["id_str"])

                # Parsing out the automated tweets
                if tweetext.split("\n")[0][-8:] == "@YouTube":
                    autom += 1

                elif tweetext[0:13] == "https://t.co/" and re.match(r"[A-Za-z0-9]{10}", tweetext[13:]) and len(
                        tweetext) == 23:
                    autom += 1

                else:
                    # print('else')
                    counter += 1
                    tnode = video.find("tweets")

                    # Either we don't have the tweet yet or we don't have tweets at all
                    if tweetext not in tweelist or len(tweelist) == 0:
                        tn = ET.SubElement(tnode, "tweet")

                        # Getting the number of tweets and updating them
                        tweecount = int(tnode.attrib['number'])
                        tweecount += 1
                        tnode.set('number', str(tweecount))

                        tweetext = tweetext.replace('\n','')
                        # print(tweetext)
                        fastTextLang = tag_language(tweetext, langdetect)[0]
                        tn.text = tweetext
                        tn.set('fastTextLang', str(fastTextLang)[11:14])
                        tn.set('twitterLang', tweelan)
                        tn.set('id', tweeid)
                        # print('Appended to xml doc')

                '''END OF APPENDING TWEETS'''

        # Sleep for 15 minutes
        else:
            count = 0
            print(ctr)
            # Not covered all the tokens
            if ctr < 10:
                print("GOTCHA\n\n\n\n")
                auth = OAuthHandler(consumer_key_list[ctr], consumer_secret_list[ctr])
                auth.set_access_token(access_token_list[ctr], access_token_secret_list[ctr])
                api = API(auth)
                ctr = ctr + 1
            else:
                print("\n\n")
                # Reset both counters
                ctr = 1
                auth = OAuthHandler(consumer_key_list[0], consumer_secret_list[0])
                auth.set_access_token(access_token_list[0], access_token_secret_list[0])
                api = API(auth)
                time.sleep(900)

# tree.write(filenm)
pretty_print = lambda root: '\n'.join([line for line in minidom.parseString(root).toprettyxml(indent="	").split('\n') if line.strip()])
# xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="	")
with open(filenm, "w") as f:
    f.write(pretty_print(ET.tostring(root)))
