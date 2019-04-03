import os
import json
import sys
import xml.etree.cElementTree as ET


def percentage_agreement(data):
    count = 0
    total = 0
    for tweet in data.findall("./category/video/tweets/tweet"):
        total += 1
        # print(tweet.attrib['twitterLang'])
        # print((tweet.attrib['fastTextLang'])[:2])
        if (tweet.attrib['twitterLang'] == (tweet.attrib['fastTextLang'])[:2] or (tweet.attrib['twitterLang'] == 'pt' and tweet.attrib['fastTextLang'] == 'por')
            or (tweet.attrib['twitterLang'] == 'es' and tweet.attrib['fastTextLang'] == 'spa') or (tweet.attrib['twitterLang'] == 'ja' and tweet.attrib['fastTextLang'] == 'jpn')
            or (tweet.attrib['twitterLang'] == 'tr' and tweet.attrib['fastTextLang'] == 'tur') or (tweet.attrib['twitterLang'] == 'zh' and tweet.attrib['fastTextLang'] == 'cmn')):
            count += 1
    return count/total * 100

if __name__ == '__main__':
    filenames = []
    for i in range(1, len(sys.argv)):
        filenames.append(sys.argv[i])
    # print(filenames)
    percentage = 0
    for filename in filenames:
        tree = ET.parse(r"/disk/data/share/MTproject/" + str(filename))
        data = tree.getroot()
        percentage = percentage_agreement(data)
    print('Percentage agreement of fastText and twitter language models: ' + str(percentage))
