from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def readHtmlFileAndReturnDictionary(fileName):
	
	wordCountDictionary = {}
	with open(fileName,'r') as fileToRead
		rawContent = fileToRead.read()
		print strip_tags(rawContent)

if __name__ == "__main__":
	readHtmlFileAndReturnDictionary('docs/Tennessee_Titans.htm')
