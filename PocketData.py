
import requests
import os
import json
import csv

#Pocket's api url:
URL = "https://getpocket.com/v3/get"

#My unique consumer key and access token:
consKey = "consumer key"
accToken = "access token"

#dictionary of the query parameters:
parameters = {"consumer_key": consKey, "access_token": accToken, "state": "read", "since": "1483250400"}

#actually sending and storing the results from the API
response = requests.post(URL, params=parameters)

#printing status code to enable more accurate understanding of failure - 200 indicates success (I think)
print("Status code: " + str(response.status_code) + "\n")

#getting the results from the API into json format and separating the item 'dictionary' - with item numerical IDs as the top category - as 'articles'
reply = response.json()
articles = reply["list"]

#counting number of articles and printing them
numArt = len(articles)
print("Articles in queue: " + str(numArt))

#determining the total and max number of words in the articles
sumW = 0
maxL = 0
maxTitle = ""
for each in articles.keys():
    wordsEach = int(articles[each]["word_count"])
    if wordsEach > maxL:
        maxL = wordsEach
        maxTitle = articles[each]["resolved_title"]
    sumW = sumW + wordsEach
print("Words in queue: " + str(sumW))
print("Average length: " + str(int(sumW/numArt)))
print("Max length: " + str(maxL) + " in " + maxTitle + "\n")

#creating .csv file for more detailed illustration of Pocket data
with open('PocketDataArchive.csv', 'w') as csvfile:
    #a list of the information to be recorded for each article
    a = 'resolved_url'
    b = 'word_count'
    c = 'time_added'
    d = 'time_read'
    fieldnames = [a, b, c, d]

    #enabling the dictionary returned in json format to be written to a .csv
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for each in articles.keys():
        writer.writerow({a:articles[each][a], b:articles[each][b], c:articles[each][c], d:articles[each][d]})
