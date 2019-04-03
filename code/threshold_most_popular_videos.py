import sys
import heapq
import xml.etree.cElementTree as ET

categories = { '1' : 'Film & Animation', '2' : 'Cars & Vehicles', '10' : 'Music', '15' : 'Pets & Animals',
               '17' : 'Sport', '19' : 'Travel & Events', '20' : 'Gaming', '22' : 'People & Blogs', '23' : 'Comedy',
               '24' : 'Entertainment', '25' : 'News & Politics', '26' : 'How-to & Style', '27' : 'Education',
               '28' : 'Science & Technology', '29' : 'Non-profits & Activism'}

def language_breakdown(category):
    dict_ = {}
    for video in category.findall("./video"):
        language_dict = {}
        video_title = video.find('title').text.replace('\t', '').replace('\n', '')
        for tweet in video.findall("./tweets/tweet"):
            if tweet.attrib['twitterLang'] in language_dict :
                language_dict[tweet.attrib['twitterLang']] += 1
            else:
                language_dict[tweet.attrib['twitterLang']] = 1
        # Build language-frequency dictionary
        dict_[(video_title, video.find('title').attrib['lang'])] = language_dict
    return dict_

def list_videos(category_name):
    category.findall("./video/tweets/tweet")

if __name__ == '__main__':
    filename = sys.argv[1]
    threshold = sys.argv[2]
    tree = ET.parse(r"/disk/data/share/MTproject/" + str(filename))
    data = tree.getroot()
    for category in data :
        print(category.text)
        category.text = category.text.replace('\t', '').replace('\n', '')
        # if category.text == 'Music':
        dict_ = language_breakdown(category)
        for k, v in dict_.items() :
            freq_list = list(v.values())
            # Report videos where one language is over the frequency threshold
            if (any(x>int(threshold) for x in freq_list)):
                print(k)
                print(dict_.get(k))
