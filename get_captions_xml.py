from bs4 import BeautifulSoup
import json
import sys
import urllib2

if __name__ == '__main__':
    xml_urls = {}
    for line in sys.stdin:
        videoId = line.strip()
        soup = BeautifulSoup(urllib2.urlopen('https://youtube.com/watch?v=' + videoId))
        scripts = soup.findAll('script')
        try:
            for script in scripts:
                if 'ytplayer' in script.text:
                    startIndex = script.text.index('{"')
                    endIndex = script.text.index(";ytplayer.load")
                    ytplayerConfig = json.loads(script.text[startIndex:endIndex])
                    caption_tracks = ytplayerConfig['args']['caption_tracks']
                    for caption_part in caption_tracks.split('&'):
                        if caption_part[:2] == 'u=':
                            xml_link = urllib2.unquote(caption_part.split('=')[1])
                            xml_urls[videoId] = xml_link
        except:
            xml_urls[videoId] = ''
    print json.dumps(xml_urls)
