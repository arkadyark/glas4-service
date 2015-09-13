import requests, json

if __name__== __main__:
	poll = requests.get('http://elections.huffingtonpost.com/pollster/api/polls.json').json()
	date = poll[0]['end_date']
	gop_src = poll[1]['questions'][0]['subpopulations'][0]['responses']
	dem_src = poll[1]['questions'][1]['subpopulations'][0]['responses']
	gop, dem = {}, {}
	for i in gop_src:
		gop[str(i['first_name']) + ' ' + str(i['last_name'])] = i['value']
	for i in dem_src:
		dem[str(i['first_name']) + ' ' + str(i['last_name'])] = i['value']
	del gop['None None']
	del dem['None None']
	gop, dem = sorted(gop, key=gop.get)[-5:], sorted(dem, key=dem.get)[-5:]
	candidates = []
	for i in gop:
		candidates.append({'name': i, 'party': 'Republicans'})
	for i in dem:
		candidates.append({'name': i, 'party': 'Democrats'})
	f = open('candidates.json', 'w')
	f.write(json.dumps(candidates))
	f.close()