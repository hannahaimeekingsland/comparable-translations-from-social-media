from trending_videos_statistics_server import compare
import os
import json
from matplotlib import pyplot as plt
import sys
import xml.etree.cElementTree as ET

colours = ['yellow', 'springgreen', 'red', 'mediumvioletred', 'salmon', 'midnightblue', 'turquoise', 'teal',
           'orchid', 'pink', 'darkgrey', 'purple', 'black', 'darkorange', 'tan']

def language_breakdown(category_name):
    language_dict = {}
    for tweet in category_name.findall("./video/tweets/tweet"):
        if tweet.attrib['twitterLang'] in language_dict :
            language_dict[tweet.attrib['twitterLang']] += 1
        else:
            language_dict[tweet.attrib['twitterLang']] = 1
    return language_dict

def graph(category_dict) :
    index = 0
    print(category_dict)
    x = list(category_dict.keys())
    legend_names = []
    legend_values = []
    i = 0
    for language_dict in list(category_dict.values()):
        y = list(language_dict.values())
        print('Category')
        print(x[i])
        print('List of values for each language')
        print(y)
        fig, ax = plt.subplots(figsize=(10, 7))
        ax.bar(list(language_dict.keys()), y, color=colours[i])
        seen = set()
        # ax.legend(legend_values, legend_names)
        ax.set_title('Frequency of different languages within tweets associated with video category: '  + str(x[i]), fontsize=14)
        # ax.set_xlabel(x[i], fontsize=12)
        ax.set_ylabel('Amount of tweets', fontsize=12)
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
        # ax.spines['bottom'].set_smart_bounds(True)
        # ax.spines['bottom'].set_position(('axes', -0.04))
        ax.spines['left'].set_position(('axes', 0.015))
        i+=1
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    for i in range(1, len(sys.argv)):
        filename = sys.argv[i]
    tree = ET.parse(r"/disk/data/share/MTproject/" + str(filename))
    data = tree.getroot()
    category_dict = {}
    for category in data:
        category_name = category.text.replace('\t', '').replace('\n', '')
        # print(category_name)
        category_dict[category_name] = language_breakdown(category)
    graph(category_dict)
