import sys
import json
import os

categories = { '1' : 'Film & Animation', '2' : 'Cars & Vehicles', '10' : 'Music', '15' : 'Pets & Animals',
           '17' : 'Sport', '19' : 'Travel & Events', '20' : 'Gaming', '22' : 'People & Blogs', '23' : 'Comedy',
           '24' : 'Entertainment', '25' : 'News & Politics', '26' : 'How-to & Style', '27' : 'Education',
           '28' : 'Science & Technology', '29' : 'Non-profits & Activism'}

def compare(file1, file2, category) :
    filepath = r"/disk/data/share/MTproject/" + category + "/"
    filename1 = os.path.join(filepath + str(file1))
    filename2 = os.path.join(filepath + str(file2))
    if (not os.path.exists(filename1)) :
        print(filename1 + ' does not exist for ' + category)
        return 0
    if (not os.path.exists(filename2)) :
        print(filename2 + ' does not exist for ' + category)
        return 0
    else:
        with open(filename1, 'r') as f:
            parsed_file1 = json.load(f)
        with open(filename2, 'r') as f2:
            parsed_file2 = json.load(f2)
        total1 = len(parsed_file1)
        total2 = len(parsed_file2)
        count_same_item = 0
        for i in range(0, total1):
            for j in range(0, total2):
                if (parsed_file1[i]['URL'] == parsed_file2[j]['URL']) :
                    count_same_item += 1
                    break
        percentage = count_same_item / max(total1, total2) * 100
        return percentage

if __name__ == '__main__':
    for category in categories.values() :
        percentage = compare(sys.argv[1], sys.argv[2], category)
        print(str(category) + ': ' + str(percentage))
