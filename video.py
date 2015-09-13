import indicoio, json, urllib2
import xml.etree.ElementTree as ET
import HTMLParser
html_parser = HTMLParser.HTMLParser()
indicoio.config.api_key = 'ec26d63d5cd8ec2544d77fa2f6efc51f'

class Video():
    def __init__(self, video_id, href):
        self.video_id = video_id
        print href
        self.xml = ET.fromstring(urllib2.urlopen(href).read())
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
        for topic in nums:
            if nums[topic] >= threshold: # and check if topic is in list
                for issue in issues:
                    if topic.lower().replace('_', '') in issue['synonyms']:
                        if len(new_blocks) and new_blocks[-1]['issue'] == issue['issue'] and new_blocks[-1]['endTime'] > t0 - 10:
                            new_blocks[-1]['endTime'] = t0 + dur
                            print "I'm mergin', fool"
                        else:
                            new_blocks.append(
                                    {'video_id' : vid.video_id,
                                        'issue' : issue['issue'],
                                        'confidence' : nums[topic],
                                        'startTime' : t0,
                                        'endTime' : t0 + dur,
                                        })

    return new_blocks

if __name__ == '__main__':
    video_resources = json.loads(open('xml_urls.json', 'r').read())
    issues = json.loads(open('issues.json', 'r').read())
    results = []
    for video_id in video_resources:
        if len(video_resources[video_id]) > 0:
            vid = Video(video_id, video_resources[video_id])
            result = blocks(vid, 2, 4, 0.5)
            print(result)
            results += result
    f = open('video_issues.json', 'w')
    f.write(json.dumps(results))
    f.close()
