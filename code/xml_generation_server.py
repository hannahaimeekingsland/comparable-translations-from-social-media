import xml.etree.cElementTree as ET
from xml.dom import minidom
import sys
import json
import re
import os
import datetime
import fnmatch
from language_tagger import tag_language
from trending_videos_difference_server import difference
import fastText

# Load fastText language detection model
langdetect = fastText.load_model('/disk/data/share/MTproject/fastText/langdetect.bin')

categories = { '1' : 'Film & Animation', '2' : 'Cars & Vehicles', '10' : 'Music', '15' : 'Pets & Animals',
		   '17' : 'Sport', '19' : 'Travel & Events', '20' : 'Gaming', '22' : 'People & Blogs', '23' : 'Comedy',
		   '24' : 'Entertainment', '25' : 'News & Politics', '26' : 'How-to & Style', '27' : 'Education',
		   '28' : 'Science & Technology', '29' : 'Non-profits & Activism'}

# Lists all files in a 'category' directory
def file_list(category_name, date):
	files = []
	filepath = r"/disk/data/share/MTproject/" + category_name + "/"
	for file_ in os.listdir(filepath) :
		if str(date) in str(file_):
			files.append(file_)
	files.sort()
	return files

def xml_structure() :
	date = datetime.datetime.now().date()
	data = ET.Element("data")
	# Put all Youtube data into XML
	for category_name in categories.values() :
		filepath = r"/disk/data/share/MTproject/" + category_name + "/"
		category = ET.SubElement(data, "category")
		category.text = category_name
		files = file_list(category_name, date)
		if len(files) > 0 :
			with open(filepath + str(files[0]), 'r') as f:
				parsed_file = json.load(f)
				total1 = len(parsed_file)
				for i in range(0, total1):
					video = ET.SubElement(category, "video")
					title = ET.SubElement(video, "title")
					url = ET.SubElement(video, "URL")
					description = ET.SubElement(video, "description")
					title.text = parsed_file[i]['Title']
					title_lang = tag_language(parsed_file[i]['Title'], langdetect)[0]
					title.attrib['lang'] = str(title_lang)[11:14]
					url.text = parsed_file[i]['URL']
					description.text = parsed_file[i]['Description']
					# ET.dump(video)
			prev_add = []
			# To delete duplicates
			for i in range(1, len(files)):
				add, take = difference(files[0], files[i], category_name)
				if (i > 1) :
					add = [x for x in add if x not in prev_add]
				if len(add) > 0 :
					with open(filepath + str(files[i]), 'r') as f:
						parsed_file = json.load(f)
						total1 = len(parsed_file)
						for i in range(0, total1):
							# Add only URLs that are different to previously seen URLs
							if parsed_file[i]['URL'] in add:
								video = ET.SubElement(category, "video")
								title = ET.SubElement(video, "title")
								title_lang = tag_language(parsed_file[i]['Title'], langdetect)[0]
								title.attrib['lang'] = str(title_lang)[11:14]
								url = ET.SubElement(video, "URL")
								description = ET.SubElement(video, "description")
								title.text = parsed_file[i]['Title']
								url.text = parsed_file[i]['URL']
								description.text = parsed_file[i]['Description']
				prev_add.extend(add)
	filepath = r"/disk/data/share/MTproject/"
	# Convert to minidom format to pretty print + encode properly
	pretty_print = lambda data: '\n'.join([line for line in minidom.parseString(data).toprettyxml(indent="	").split('\n') if line.strip()])
	# xmlstr = minidom.parseString(ET.tostring(data)).toprettyxml(indent="	")
	with open(filepath + str(date) + ".xml", "w") as f:
		f.write(pretty_print(ET.tostring(data)))

if __name__ == '__main__':
	xml_structure()
