import re
import fastText
import sys

def tag_language(text):
	##Get rid of all punctuation in text
	text = re.sub(r'[^\w\s]','',text)
	##Predict label using pretrained langdetect model
	langdetect = fastText.load_model('/disk/data/share/MTproject/fastText/langdetect.bin')
	pred = langdetect.predict(text)
	# print(text, pred)
	##Returns prediction - a tuple respresenting language and accuracy
	return pred

if __name__ == '__main__':
	text = ""
	for i in range(1, len(sys.argv)):
		text += ' ' + str(sys.argv[i]).lower()
	tag_language(text)

	


