import sys
import json
from datetime import datetime
import os
import difflib

categories = { '1' : 'Film & Animation', '2' : 'Cars & Vehicles', '10' : 'Music', '15' : 'Pets & Animals',
           '17' : 'Sport', '19' : 'Travel & Events', '20' : 'Gaming', '22' : 'People & Blogs', '23' : 'Comedy',
           '24' : 'Entertainment', '25' : 'News & Politics', '26' : 'How-to & Style', '27' : 'Education',
           '28' : 'Science & Technology', '29' : 'Non-profits & Activism'}

def difference(file1, file2, category) :
    print(category)
    filepath = r"/disk/data/share/MTproject/" + category + "/"
    filename1 = os.path.join(filepath + str(file1))
    filename2 = os.path.join(filepath + str(file2))
    # Determine which is the earlier/later file
    earlier_file = max(filename1, filename2)
    later_file = min(filename1, filename2)
    if (not os.path.exists(filename1)) :
        print(filename1 + ' does not exist for ' + category)
        return 0, 0
    if (not os.path.exists(filename2)) :
        print(filename2 + ' does not exist for ' + category)
        return 0, 0
    else:
        with open(earlier_file, 'r') as f:
            parsed_earlier = json.load(f)
        with open(later_file, 'r') as f2:
            parsed_later = json.load(f2)
        total1 = len(parsed_earlier)
        total2 = len(parsed_later)
    add = []
    take = []
    earlier_urls = []
    later_urls = []
    for dict_ in parsed_earlier:
        earlier_urls.append(dict_['URL'])
    for dict_ in parsed_later:
        later_urls.append(dict_['URL'])

    add = [x for x in later_urls if x not in earlier_urls]
    take = [x for x in earlier_urls if x not in later_urls]

    return add, take

if __name__ == '__main__':
    for category in categories.values() :
        add, take = difference(sys.argv[1], sys.argv[2], category)
        print(add)
        print(take)
