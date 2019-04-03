import re
import fastText
import sys

def tag_language(text, langdetect):
	# Get rid of all punctuation in text
	text = re.sub(r'[^\w\s]','',text)
	# Get rid of all newline characters
	text = text.replace('\n','')
	# Predict label using pretrained langdetect model
	pred = langdetect.predict(text)
	# print(text, pred)
	# Returns prediction - a tuple respresenting language and accuracy
	return pred

if __name__ == '__main__':
	text = ""
	for i in range(1, len(sys.argv)):
		text += ' ' + str(sys.argv[i]).lower()
	langdetect = fastText.load_model('/disk/data/share/MTproject/fastText/langdetect.bin')
	tag_language(text, langdetect)
