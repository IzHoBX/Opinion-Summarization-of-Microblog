import pickle
import requests
import urllib
import asyncio
import aiohttp
from aiohttp import ClientSession

async def fetch(session, pair):

    url = "https://wat.d4science.org/wat/relatedness/graph"
    params = {}
    params["lang"] = "en"
    params["gcube-token"] = "0fea3a55-cec4-4b2e-8dcc-2b9ccb6ed83c-843339462"
    params["relatedness"] = "jaccard"
    data = urllib.parse.urlencode(params)
    for id in pair:
        data += "&ids=" + str(id)
    try:
        async with session.get(url+"?"+data) as response:
            return (pair, (await response.json())["pairs"][0])
    except:
        return (pair, None)

async def run(allPairs):
    global temp
    tasks = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        for pair in allPairs:
            task = asyncio.ensure_future(fetch(session, pair))
            tasks.append(task)

        temp = await asyncio.gather(*tasks)

# directories = ("spacex", "brexit", "election", "isis", "nobel", "note7")
directories = ("isis", "nobel", "note7")
classes = ("/positive", "/negative", "/neutral")

urlForId = "https://wat.d4science.org/wat/title"
paramsForId = {}
paramsForId["gcube-token"] = "0fea3a55-cec4-4b2e-8dcc-2b9ccb6ed83c-843339462"
url = "https://wat.d4science.org/wat/relatedness/graph"
params = {}
params["lang"] = "en"
params["gcube-token"] = "0fea3a55-cec4-4b2e-8dcc-2b9ccb6ed83c-843339462"
params["relatedness"] = "jaccard"

try:
    f = open("./cache", "rb")
    titleToId = pickle.load(f)
    f.close()
except FileNotFoundError:
    titleToId = {}
scoreCache = {}
temp = []


for directory in directories:
    corpus = pickle.load(open("./"+directory+"/corpus", "rb"))
    # inReplyStatusId, userId, numRetweet, numFavourite, text
    for c in classes:
        meta = pickle.load(open("./" + directory + c + "ClusteredWG", "rb"))
        replyGraph = pickle.load(open("./" + directory+c+"ReplyGraph", "rb"))
        # [allEntities, entityIndicesByTweet, numpy.array(matrix), listsOfNodesBelongingToTheSameCluster]

        clusterToIndicesOfAssignedTweet = []
        for i in range(0, len(meta[3])):
            clusterToIndicesOfAssignedTweet.append([])

        print("numberOfEntities: " + str(len(meta[0])))
        for e in range(0, len(meta[0])):
            if not meta[0][e] in titleToId:
                print("looking id for:" + meta[0][e])
                paramsForId["title"] = meta[0][e]
                data = urllib.parse.urlencode(paramsForId)
                res = requests.get(urlForId, data)
                titleToId[meta[0][e]] = res.json()["wiki_id"]
        print("done with ids")

        allPairsToRetrieve = set()
        for statusId, setOfIndicesOfEntitiesOfATweet in meta[1].items():
            for j in range(0, len(meta[3])):
                setOfIndicesOfEntitiesOfACluster = meta[3][j]
                for indexFromTweet in setOfIndicesOfEntitiesOfATweet:
                    for indexFromCluster in setOfIndicesOfEntitiesOfACluster:
                        if indexFromTweet == indexFromCluster:
                            continue
                        id1 = titleToId[meta[0][indexFromTweet]]
                        id2 = titleToId[meta[0][indexFromCluster]]
                        if not (id1, id2) in scoreCache and not (id2, id1) in scoreCache and not (id1, id2) in allPairsToRetrieve and not (id2, id1) in allPairsToRetrieve:
                            allPairsToRetrieve.add((id1, id2))

        allPairs = list(allPairsToRetrieve)
        print("Total numPair required: " + str(len(allPairs)))

        data = urllib.parse.urlencode(params)
        temp = set()
        for id1, id2 in allPairs:
            if not id1 in temp:
                data += "&ids=" + str(id1)
                temp.add(id1)
            if not id2 in temp:
                data += "&ids=" + str(id2)
                temp.add(id2)
        print("number of id in link:" + str(len(temp)))

        res = requests.get(url, data)
        res = res.json()["pairs"]
        print("received pairwise relatedness data")
        print("total number of pairs received:" + str(len(res)))
        for pair in res:
            id1 = pair["src_title"]["wiki_id"]
            id2 = pair["dst_title"]["wiki_id"]
            score = pair["relatedness"]
            scoreCache[(id1, id2)] = score

        allPairsToRetrieve = set()
        for statusId, setOfIndicesOfEntitiesOfATweet in meta[1].items():
            for j in range(0, len(meta[3])):
                setOfIndicesOfEntitiesOfACluster = meta[3][j]
                for indexFromTweet in setOfIndicesOfEntitiesOfATweet:
                    for indexFromCluster in setOfIndicesOfEntitiesOfACluster:
                        if indexFromTweet == indexFromCluster:
                            continue
                        id1 = titleToId[meta[0][indexFromTweet]]
                        id2 = titleToId[meta[0][indexFromCluster]]
                        if not (id1, id2) in scoreCache and not (id2, id1) in scoreCache and not (id1, id2) in allPairsToRetrieve and not (id2, id1) in allPairsToRetrieve:
                            allPairsToRetrieve.add((id1, id2))

        allPairs = list(allPairsToRetrieve)
        while len(allPairs) > 0:
            print("Total numPair required: " + str(len(allPairs)))
            loop = asyncio.get_event_loop()
            future = asyncio.ensure_future(run(allPairs))
            loop.run_until_complete(future)

            allPairs = []
            count = 0
            for ((id1, id2), data) in temp:
                if data == None:
                    allPairs.append((id1, id2))
                    continue
                count += 1
                id1 = int(data["src_title"]["wiki_id"])
                id2 = int(data["dst_title"]["wiki_id"])
                score = data["relatedness"]
                scoreCache[(id1, id2)] = score

            print("received through async:" + str(count))

        print("done with pairwise relatedness")

        for statusId, setOfIndicesOfEntitiesOfATweet in meta[1].items():
            for j in range(0, len(meta[3])):
                setOfIndicesOfEntitiesOfACluster = meta[3][j]
                sum = 0
                denom = 0
                for indexFromTweet in setOfIndicesOfEntitiesOfATweet:
                    for indexFromCluster in setOfIndicesOfEntitiesOfACluster:
                        id1 = titleToId[meta[0][indexFromTweet]]
                        id2 = titleToId[meta[0][indexFromCluster]]
                        if id1 == id2:
                            sum += 1
                            denom += 1
                            continue
                        if (id1, id2) in scoreCache:
                            sum += scoreCache[(id1, id2)]
                        elif (id2, id1) in scoreCache:
                            sum += scoreCache[(id2, id1)]
                        else:
                            # for some reason this pair isn't in cache during mass pull
                            print("pulling outside of batch: " + str(id1) + " " + str(id2))
                            data = urllib.parse.urlencode(params)
                            data+="&ids="+str(id1)
                            data+="&ids="+str(id2)
                            res = requests.get(url, data)
                            try:
                                score = res.json()["pairs"][0]["relatedness"]
                                sum += score
                                scoreCache[(id1, id2)] = score
                            except:
                                #for some reason server not returning score for this pair
                                denom -= 1 #exclude this term for evaluation
                        denom += 1
                if denom == 0:#should only happen to zero-entity tweets
                    sum = 0
                else:
                    sum /= denom
                if sum > 0.001:
                    clusterToIndicesOfAssignedTweet[j].append(statusId)
                    if statusId in replyGraph:
                        for s in replyGraph[statusId]:
                            clusterToIndicesOfAssignedTweet[j].append(s)
        pickle.dump(clusterToIndicesOfAssignedTweet, open("./" + directory + c + "ClusterToAssignedTweets", "wb"))

pickle.dump(titleToId, open("./cache", "wb"))
