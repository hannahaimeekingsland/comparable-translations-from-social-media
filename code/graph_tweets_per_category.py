from matplotlib import pyplot as plt
import sys
import xml.etree.cElementTree as ET

categories = { '1' : 'Film & Animation', '2' : 'Cars & Vehicles', '10' : 'Music', '15' : 'Pets & Animals',
               '17' : 'Sport', '19' : 'Travel & Events', '20' : 'Gaming', '22' : 'People & Blogs', '23' : 'Comedy',
               '24' : 'Entertainment', '25' : 'News & Politics', '26' : 'How-to & Style', '27' : 'Education',
               '28' : 'Science & Technology', '29' : 'Non-profits & Activism'}

def amount_of_tweets(category_name):
    # Search XML file for all tweets under a particular category
    print(category.findall('./video/tweets'))
    return len(category.findall("./video/tweets/tweet"))

def graph(category_dict) :
    fig, ax = plt.subplots(figsize=(10, 7))
    plt.bar(list(category_dict.keys()), list(category_dict.values()), color='salmon')
    plt.title('Amount of tweets collected per category every day', fontsize=14)
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Amount of tweets', fontsize=12)
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = 'Helvetica'
    plt.rcParams['axes.edgecolor']='#333F4B'
    plt.rcParams['axes.linewidth']=0.8
    plt.rcParams['xtick.color']='#333F4B'
    plt.rcParams['ytick.color']='#333F4B'
    plt.rcParams['text.color']='#333F4B'
    # ax.tick_params(axis='both', which='major', labelsize=12)
    ax.tick_params(axis='x', rotation=70)
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_smart_bounds(True)
    # ax.spines['bottom'].set_smart_bounds(True)
    # ax.spines['bottom'].set_position(('axes', -0.04))
    ax.spines['left'].set_position(('axes', 0.015))
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    for i in range(1, len(sys.argv)):
        filename = sys.argv[i]
    tree = ET.parse(r"/disk/data/share/MTproject/" + str(filename))
    data = tree.getroot()
    category_dict = {}
    for category in data :
        category_name = category.text.replace('\t', '').replace('\n', '')
        print(category_name)
        category_dict[category_name] = amount_of_tweets(category)
        print(category_dict)
    graph(category_dict)
