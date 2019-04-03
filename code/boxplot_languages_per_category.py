from matplotlib import pyplot as plt
import sys
import xml.etree.cElementTree as ET
from math import log

colours = ['yellow', 'springgreen', 'red', 'mediumvioletred', 'salmon', 'midnightblue', 'turquoise', 'teal',
           'orchid', 'pink', 'darkgrey', 'purple', 'black', 'darkorange', 'tan']

def language_breakdown(video):
    language_dict = {}
    for tweet in video.findall("./tweets/tweet"):
        if tweet.attrib['twitterLang'] in language_dict :
            language_dict[tweet.attrib['twitterLang']] += 1
        else:
            language_dict[tweet.attrib['twitterLang']] = 1
    return language_dict


def graph(final_dict, category_name) :
    # Generate boxplot
    fig, ax = plt.subplots(figsize=(10, 7))
    pos = list(range(len(final_dict.keys()) + 1))
    print(pos)
    bp = ax.boxplot(final_dict.values())
    # ax.legend(legend_values, legend_names)
    for flier in bp['fliers']:
        flier.set(marker='o', color='#e7298a', alpha=0.5)
    ax.set_xticklabels(final_dict.keys())
    ax.set_title('Frequency of different languages within tweets associated with video category: '  + category_name, fontsize=14)
    ax.set_xlabel("Language", fontsize=12)
    ax.set_ylabel('Amount of tweets (log10)', fontsize=12)
    # ax.set_ylim([0,25000])
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = 'Helvetica'
    plt.rcParams['axes.edgecolor']='#333F4B'
    plt.rcParams['axes.linewidth']=0.8
    plt.rcParams['xtick.color']='#333F4B'
    plt.rcParams['ytick.color']='#333F4B'
    plt.rcParams['text.color']='#333F4B'
    # ax.tick_params(axis='both', which='major', labelsize=12)
    ax.tick_params(axis='x', rotation=45)
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_smart_bounds(True)
    ax.spines['bottom'].set_smart_bounds(True)
    # ax.spines['bottom'].set_position(('axes', -0.04))
    # ax.spines['left'].set_position(('axes', 0.0))
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    for i in range(1, len(sys.argv)):
        filename = sys.argv[i]
    tree = ET.parse(r"/disk/data/share/MTproject/" + str(filename))
    data = tree.getroot()
    for category in data:
        category_name = category.text.replace('\t', '').replace('\n', '')
        video_dict = {}
        for video in category.findall("./video"):
            video_title = video.find('title').text.replace('\t', '').replace('\n', '')
            # Generate a language breakdown per video
            video_dict[video_title] = language_breakdown(video)

        final_dict = {}

        # Place languages and frequencies in another dictionary assessing them per video
        # Dictionary looks like {en: [2,3,4,5], ko: [1,1]} where each entry in the list
        # represents frequency for one video
        for title, lang_dict in video_dict.items() :
            if len(lang_dict) > 0 :
                for key, value in lang_dict.items():
                    if key in final_dict :
                        dict_list = final_dict.get(key)
                        dict_list.append(value)
                        final_dict[key] = dict_list
                    else:
                        dict_lst = []
                        dict_lst.append(value)
                        final_dict[key] = dict_lst

        print(category_name)
        graph(final_dict, category_name)
