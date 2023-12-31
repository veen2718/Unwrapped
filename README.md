# Unwrapped - Spotify Stats

A python script that gives detailed statistics about your Spotify history

## Instructions

Download the latest release from the release page.
Extract the zip.

### Downloading Spotify Data

Go to https://www.spotify.com/ca-en/account/privacy#/
Request your Account Data. Within 5 days you should get an email containing a zip with your data. 
There is a folder in that zip called 'Spotify Account Data'. That folder should contain several files including one or more files named similar to 'StreamingHistory0.json'. 
Copy the entire folder into the 'Unwrapped' folder with the python script. 

### Getting Spotify API Client ID and Client Secret

If you do not want to use the Spotify API and only want to get data from downloading it from Spotify's website, you can change the value of the ``useAPI`` in the vars.py file to False


Go to https://developer.spotify.com/dashboard/applications

Log in with your spotify account

Click on 'create an app', and pick an 'App name' and 'App description', the name and description do not matter

After creation, you can see your Client ID and Client Secret, which you will need in the next step

### Setting up Github Credentials for backup
The next step is to setup GitHub credentials for backup. This is recommended so that you can set up this same script on multiple devices, or if possible a raspberry pi or something such that you can easily automate this script to run once every hour or so. This is because although you were able to get much of your data by requesting it from Spotify, when using the spotify API to get data, it is only possible to get the 50 most recent tracks. This is why it is beneficial to automate this process so that you will always have the most accurate version of your Spotify data. 


#### Creating a Github Repo
On the Github website, click create a new repository, and ensure that it is set to private, and choose whatever name you want. It will take you to a page that will have a section labeled Quick Setup. Make sure it is set to https and copy the link. Open the gitcredentials.py file, and set the `repoURL` variable to that link. Then set the `username` variable to your username.


#### Creating a Github Personal Access Token
You will need to create a Github personal access token instead of a password. On the github website, click your profile picture, and click settings. Then click Developer Settings. Then click Personal Access token and click Fine-grained token, and click new. Choose any token name. For expiration, choose a custom date an year from the day you set this up, which is the maximum. You will need to regenerate the token. Under repository access click All repositories or Only select repositories, and select the repository you created. 

Under Permissions and Repository Permissions, give the token read and write access to commit statuses, contents and administration.

Then click generate token, and copy the token to the `password` variable in the gitcredentials.py file.

### Setting up the python script

Do all the following steps if you want to use the Spotify API:

- In the release folder, create a file called 'apikeys.py'

- in the file add the following lines of code

    ```python

    client_id_spotify = "YOUR_SPOTIFY_CLIENT_ID"
    client_secret_spotify = "YOUR_SPOTIFY_CLIENT_SECRET"
    ```

- Replace YOUR_CLIENT_ID and YOUR_CLIENT_SECRET with your Spotify Client ID and Secret from earlier. 

Do the next step regardless of whether or not you want to use the Spotify API:

- Run ``pip  install -r requirements.txt``, which will install required libraries


### Usage

#### Differences between user.py and main.py
The main.py is intended for automation and will not download from google drive or upload if there are no files to write. This is different from the user.py, which is intended for the user to use, as it will download from google drive no matter what to ensure the user has the most recent data. In the following instructions, when I mention main.py, I mean use user.py if you are manually running to view your stats, but for automation purposes use main.py.

#### Usage

Run main.py, and a folder will be created called *stats*. In that folder there shoud be an *artists.txt* and *tracks.txt*, containing a table with the data. Once table is generated, the 'Spotify Account Data' folder will be deleted,and a history.json will be created to store the data. 

Later, you may request your data again, and copy the 'Spotify Account Data' folder into the SpotifyAnalyze folder. Running main.py again will merge any new history from the 'Spotify Account Data' with your old history.

Every time you run main.py, it will make an API call, and add the 50 most recently played songs to the history.json. Because of limits of the Spotify API you cannot get the entire history from the API, so I recommend that you use a command scheduler to schedule the main.py script to run frequently. 


### Automation
I highly recommend that you automate this script to run frequently. This is because through Spotify's API you can only get the 50 most recently played songs from a user's history. This is why you requested and downloaded your data from Spotify because that way you have a lot more of your history. But by frequentely calling Spotify's API and storing the songs when we can, we can build a near complete record of streaming history which can then be analyzed by this script. For Linux, MacOS or WSL you can use Crontab to schedule this file to run, or on MacOS you can use Automator and on Windows you can use Task Scheduler. 


### vars.py
There are multiple variables the user can change in the vars.py file

`mMin`: This is the number of minutes a song will have to play before the song counts as a track

`getDownloadedData`: If this is true, it will check the Spotify Account Data folder and read data from there, else it will read from history.json. If the Spotify Account Data folder has been deleted, it will act as though this is false.

`sortBy`: If this is set to 0, it will sort the table by the number of times a track is played. If this is set to 1, it will sort the table by the number of minutes a track is played for. 

`useAPI`: If this is False, will not use the Spotify API, and will just use downloaded data

`useGithubBackup`: If this is set to False, will not use Github for backup

### Updating to newer version
When updating to a newer version, simply copy the history.json file into the folder with the new release 

## Current Features

- Generate table for artist data including artist name, minutes played, times their tracks are played
- Generate table for track data including track name, artist of track, minutes played, times the track is played
- Get data from Spotify API in addition to downloaded data

## Upcoming Features

- GUI
- Graph with interest in songs/artists over time
- Android App