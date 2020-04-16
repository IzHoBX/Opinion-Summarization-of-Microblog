import asyncio
import aiohttp
from aiohttp import ClientSession
import urllib
import requests
import pickle
import numpy

async def fetch(session, statusId):
    line = corpus[statusId][4]
    url = "https://wat.d4science.org/wat/tag/tag"
    params = {}
    params["lang"] = "en"
    params["gcube-token"] = "0fea3a55-cec4-4b2e-8dcc-2b9ccb6ed83c-843339462"
    params["text"] = line
    data = urllib.parse.urlencode(params)
    async with session.get(url+"?"+data) as response:
        return (statusId, (await response.json())["annotations"])

async def run(statusIds):
    global temp
    tasks = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        for statusId in statusIds:
            task = asyncio.ensure_future(fetch(session, statusId))
            tasks.append(task)

        temp = await asyncio.gather(*tasks)

#directories = ("brexit", "election", "isis", "nobel", "note7")
directories = ("isis", "nobel", "note7")
classes = ("/positive.txt", "/negative.txt", "/neutral.txt")
count = 0
temp = []
try:
    f = open("./cache", "rb")
    titleToId = pickle.load(f)
    f.close()
except FileNotFoundError:
    titleToId = {}

for directory in directories:
    corpus = pickle.load(open("./"+directory+"/corpus", "rb"))
    # inReplyStatusId, userId, numRetweet, numFavourite, text
    for c in classes:
        print("doing " + directory + " " + c)
        listOfStatusId = pickle.load(open("./" + directory+c, "rb"))
        allEntities = []
        entityIndicesByTweet = {}
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(run(listOfStatusId))
        loop.run_until_complete(future)
        for statusId, annotationsOfAPost in temp:
            entityIndices = set()
            for r in annotationsOfAPost:
                titleToId[r["title"]] = r["id"]
                entity = r["title"]
                confidence = r["rho"]
                if entity not in allEntities:
                    index = len(allEntities)
                    allEntities.append(entity)
                else:
                    index = allEntities.index(entity)
                entityIndices.add(index)
            entityIndicesByTweet[statusId] = entityIndices
        matrix = []
        for i in range(0, len(allEntities)):
            matrix.append([0]*len(allEntities))
        for statusId, entityIndicesOfSingleTweet in entityIndicesByTweet.items():
            for i1 in entityIndicesOfSingleTweet:
                for i2 in entityIndicesOfSingleTweet:
                    if i1 != i2:
                        matrix[i1][i2] += 1 +  2 * corpus[statusId][2] + corpus[statusId][3]
        pickle.dump([allEntities, entityIndicesByTweet, numpy.array(matrix)], open( "./"+directory+(c[:-4]), "wb"))

pickle.dump(titleToId, open("./cache", "wb"))
