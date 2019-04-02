from trending_videos_statistics_server import compare
import matplotlib
from matplotlib import pyplot as plt
import sys

categories = { '1' : 'Film & Animation', '2' : 'Cars & Vehicles', '10' : 'Music', '15' : 'Pets & Animals',
           '17' : 'Sport', '19' : 'Travel & Events', '20' : 'Gaming', '22' : 'People & Blogs', '23' : 'Comedy',
           '24' : 'Entertainment', '25' : 'News & Politics', '26' : 'How-to & Style', '27' : 'Education',
           '28' : 'Science & Technology', '29' : 'Non-profits & Activism'}

def graph(category, filenames, percentages) :
    plt.figure(figsize=(8, 6), dpi=80)
    plt.subplot(1, 1, 1)
    plt.bar(filenames, percentages)
    plt.title(category)
    plt.xlabel('Time elapsed (hours)')
    plt.xticks(rotation=90)
    plt.ylabel('Percentage alike')
    time_labels = []
    time_elapsed = 0
    for i in range(0, len(percentages)) :
        time_labels.append(str(time_elapsed))
        time_elapsed += 1
    plt.xticks(filenames, time_labels)
    plt.show()

if __name__ == '__main__':
    filenames = []
    for i in range(1, len(sys.argv)) :
        filenames.append(sys.argv[i])
    filenames.sort()
    print(filenames)
    graph_dict = {}
    for category in categories.values() :
        percentages = []
        for f in range(0, len(filenames)) :
            percentages.append(compare(filenames[0], filenames[f], category))
        graph_dict[category] = percentages

    print(graph_dict)
    for category, percentages in graph_dict.items():
        print(category)
        print(percentages)
        graph(category, filenames, percentages)
