import indicoio
import xml.etree.ElementTree as ET
import HTMLParser
html_parser = HTMLParser.HTMLParser()
indicoio.config.api_key = '325841fe465c3d5967838467642d75cd'

class Video():
	def __init__(self, filename, candidate_name):
		tree = ET.parse(filename)
		self.xml = tree.getroot()
		self.candidate_name = candidate_name
		self.strings = None
		self.scores = {}

	def __str__(self):
		string = ''
		for line in self.xml:
			new = str(html_parser.unescape(line.text)).replace('\n', ' ') + ' '
			string += new
		return string


	def parse(self, slide_length, window_length):
		self.strings = []
		for i in range(0, int(len(self.xml)/slide_length)):
			self.strings.append([])
			for k in range(i*slide_length, i*slide_length + window_length):
				try:
					new_string = str(html_parser.unescape(self.xml[k].text)).replace('\n', ' ')
					self.strings[i].append(new_string)
				except:
					IndexError
		for i in range(len(self.strings)):
			sentence = self.strings[i]
			self.strings[i] = ' '.join(sentence)

	def score(self, slide_length, window_length, AItype='tags'):
		self.parse(slide_length, window_length)
		if AItype == 'tags':
			self.scores['tags'] = [indicoio.text_tags(i) for i in self.strings]
		elif AItype == 'keywords':
			self.scores['keywords'] = [indicoio.keywords(i) for i in self.strings]
		elif AItype == 'names':
			self.scores['names'] = [indicoio.named_entities(i) for i in self.strings]
		else:
			raise Exception('Warning: {} not a valid category'.format(category))

def blocks(vid, slide_length, window_length, threshold=0, AItype='tags'):
	new_blocks = []
	vid.score(slide_length, window_length, AItype)
	for nums in vid.scores[AItype]:
		start = vid.scores[AItype].index(nums)*slide_length
		end = start + window_length
		t0 = float(vid.xml[start].attrib['start'])
		dur = sum([float(i.attrib['dur']) for i in vid.xml[start:end]])
		new_nums = {}
		for topic in nums:
			if nums[topic] >= threshold: # and check if topic is in list
				new_nums[topic] = nums[topic]
		new_blocks.append({'time': [t0, t0 + dur], 'values': new_nums, 'candidate': vid.candidate_name})
	return new_blocks

def findtags(block, tags):
	intervals = []
	for interval in block:
		if any([word in interval['values'] for word in tags]):
			intervals.append(interval)
	return intervals


vid = Video('transcript2.xml', 'Bernie Sanders')
# tags = ['crime', 'firearms', 'guns']
# result = blocks(vid, 2, 4, 0.5)
# vals = findtags(result, tags)
# print(vals)
print(vid)