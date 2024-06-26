from datetime import datetime
import json
import pytz

from read import get2
from files import readJson, writeJson

def parse_time(data,time='endTime'):
    try:
        return datetime.strptime(data[time], '%Y-%m-%d %H:%M:%S')
    except:
        return datetime.strptime(data[time], '%Y-%m-%d %H:%M')


def log(Length,path='data/logs.json'):
    pdt_zone = pytz.timezone("America/Los_Angeles") 
    currentTime = datetime.now(pdt_zone).strftime('%Y-%m-%d %H:%M:%S %Z')
    if Length > 0:
        messege = f"Added {Length} songs at {currentTime}. Total songs are {len(get2())}"
        oldLogs = readJson(path)
        oldLogs.append({currentTime: messege})
        writeJson(path,oldLogs)
    print(f"Added {Length} songs at {currentTime}. Total songs are {len(get2())}")  



def write(history,jsonFile='data/history.json'):
    newHistory = []
    for story in history:
        newStory = {}
        newStory['endTime'] = story['endTime']
        try:
            if type(story['artistName']) in [list, tuple]:
                newStory['artistName'] = tuple(story['artistName'])
        except Exception as e:
            print(e)
            print(json.dumps(story, indent=4))
            raise ValueError("Could not write")
        else:
            newStory['artistName'] = (story['artistName'],)
        # newStory['artistName'] = story['artistName']
        newStory['trackName'] = story['trackName']
        if 'msPlayed' in story:
            newStory['msPlayed'] = story['msPlayed']
        else:
            newStory['msPlayed'] = None
        if 'duration_ms' in story:
            newStory['duration_ms'] = story['duration_ms']
        else:
            newStory['duration_ms'] = None

        newHistory.append(newStory)
    
    sortedHistory = sorted(newHistory, key=parse_time)
    print("About to write to history.json")
    writeJson(jsonFile, sortedHistory)
    print("Written to history.json")


def fix():
    print("about to start fixing incomplete artists")
    json_data = readJson('data/history.json')
    dataWithMultipleArtists = [data for data in json_data if len(data['artistName']) > 1] #All entries in history.json where there are multiple artists
    artistsInMultipleArtists = [data['artistName'] for data in json_data if len(data['artistName']) > 1] #All Artists in dataWithMultipleArtists
    artistsInMultipleArtists2 = [] #The previous list would be [['artist1','artist2'],['artist1','artist3']], while this one is ['artist1', 'artist2','artist3']
    for artists in artistsInMultipleArtists:
        for artist in artists:
            if artist not in artistsInMultipleArtists2:
                artistsInMultipleArtists2.append(artist)


    fixedSongs = 0 
    for data in json_data:
        artists = data['artistName']
        if len(artists) == 1 and artists[0] in artistsInMultipleArtists2:
            artist = artists[0]
            for otherData in dataWithMultipleArtists:
                if otherData['trackName'] == data['trackName']:
                    if artist in otherData['artistName']:
                        data['artistName'] = otherData['artistName']
                        fixedSongs += 1
    
    writeJson('data/history.json',json_data)
    print(f"finished fixing incomplete artists, fixed {fixedSongs} tracks")

def prune(jsonFile='data/history.json'):#Removes duplicate entries, meaning exact time must match, as well as artist and track names
    print("about to start pruning")
    data = readJson(jsonFile)
    prunedData = []
    prunedCount = 0
    for entry in data:
        if entry in prunedData:
            prunedCount += 1
        else:
            prunedData.append(entry)
            
    if prunedCount > 0:
        print(f"Pruned {prunedCount} copies")
        writeJson(jsonFile, prunedData)
        log(prunedCount * -1)

    print("finished prining")