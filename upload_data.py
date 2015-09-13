import json, httplib, datetime, time

APPLICATION_ID = 'iXDvlSh7XJjt7J5a0vB6kgWSljEjtIICxAWTQnrF'
API_KEY = 'zl51tL6NUU8tomJyBch31vaDaMTXCND9sdMBkYRY'
headers = {
        "X-Parse-Application-Id" : APPLICATION_ID,
        "X-Parse-REST-API-Key": API_KEY,
        "Content-Type" : "application/json"
        }

connection = httplib.HTTPSConnection('api.parse.com', 443)
connection.connect()

issues = [issue['issue'] for issue in json.loads(open('issues.json').read())]
issueIDs = {}
candidates = json.loads(open('candidates.json').read())
candidateIDs = {}

videos = json.loads(open('video_issues.json').read())
metadata = json.loads(open('metadata.json').read())

for issue in issues:
    connection.request('POST', '/1/classes/Issues', json.dumps({
        'issueName' : issue
        }), headers)
    issueIDs[issue] = json.loads(connection.getresponse().read())['objectId']

raw_input("Enter to continue")

for candidate in candidates:
    connection.request('POST', '/1/classes/Candidates', json.dumps({
        'first_name' : candidate['name'].split(' ')[0],
        'last_name' : ' '.join(candidate['name'].split(' ')[1:]),
        'party' : candidate['party']
        }), headers)
    candidateIDs[candidate['name']] = json.loads(connection.getresponse().read())['objectId']

raw_input("Enter to continue")

for video in videos:
    for video_info in metadata:
        if video_info['video_id'] == video['video_id']:
            issueID = issueIDs[video['issue']]
            candidateID = candidateIDs[video_info['speaker_name']]
            connection.request('POST', '/1/classes/Videos', json.dumps({
                'issuesID' : issueID,
                'candidatesID' : candidateID,
                'videoID' : video['video_id'],
                'startTime' : video['startTime'],
                'endTime' : video['endTime']
                'confidence' : video['confidence'],
                'timestamp' : 
                    {
                          "__type": "Date",
                            "iso": video_info['timestamp']
                            }
            }), headers)
            json.loads(connection.getresponse().read())


