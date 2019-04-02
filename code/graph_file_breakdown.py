from trending_videos_statistics_server import compare
import matplotlib
import os
import json
from matplotlib import pyplot as plt
import sys

categories = { '1' : 'Film & Animation', '2' : 'Cars & Vehicles', '10' : 'Music', '15' : 'Pets & Animals',
               '17' : 'Sport', '19' : 'Travel & Events', '20' : 'Gaming', '22' : 'People & Blogs', '23' : 'Comedy',
               '24' : 'Entertainment', '25' : 'News & Politics', '26' : 'How-to & Style', '27' : 'Education',
               '28' : 'Science & Technology', '29' : 'Non-profits & Activism'}

def file_list(category_name, date):
    files = []
    filepath = r"/disk/data/share/MTproject/" + category_name + "/"
    for file_ in os.listdir(filepath) :
        if str(date) in str(file_):
            files.append(file_)
    files.sort()
    return files

def amount_of_videos(category_name, filenames):
    filepath = r"/disk/data/share/MTproject/" + category_name + "/"
    video_counts = []
    avg_video_count = 0
    for i in range(len(filenames)) :
        with open(filepath + str(filenames[i]), 'r') as f:
            parsed_file = json.load(f)
            video_count = len(parsed_file)
            video_counts.append(video_count)
            avg_video_count = sum(video_counts) / len(filenames)

    return avg_video_count


def graph(avg_graph_dict) :
    fig, ax = plt.subplots(figsize=(10, 7))
    plt.bar(list(avg_graph_dict.keys()), list(avg_graph_dict.values()), color='lavender')
    plt.title('Average amount of videos collected per category, per hour', fontsize=14)
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Average amount of videos collected per hour', fontsize=12)
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
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    for i in range(1, len(sys.argv)):
        date = sys.argv[i]
    avg_graph_dict = {}
    graph_dict = {}
    for category in categories.values() :
        filenames = file_list(category, date)
        avg_video_count = amount_of_videos(category, filenames)
        avg_graph_dict[category] = avg_video_count
    graph(avg_graph_dict)
