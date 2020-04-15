import urllib
import requests
import pickle
import numpy

#directories = ("brexit", "election", "isis", "nobel", "note7")
directories = ["spacex"]
classes = ("/positive.txt", "/negative.txt", "/neutral.txt")
url = "https://wat.d4science.org/wat/tag/tag"
params = {}
params["lang"] = "en"
params["gcube-token"] = "0fea3a55-cec4-4b2e-8dcc-2b9ccb6ed83c-843339462"
count = 0

for directory in directories:
    corpus = pickle.load(open("./"+directory+"/corpus", "rb"))
    # inReplyStatusId, userId, numRetweet, numFavourite, text
    for c in classes:
        print("doing " + directory + " " + c)
        listOfStatusId = pickle.load(open("./" + directory+c, "rb"))
        allEntities = []
        entityIndicesByTweet = {}
        for statusId in listOfStatusId:
            line = corpus[statusId][4]
            count += 1
            if count % 500 == 0:
                print(count)
            params["text"] = line
            data = urllib.parse.urlencode(params)
            res = requests.get(url, data)
            entityIndices = set()
            try:
                for r in res.json()["annotations"]:
                    entity = r["title"]
                    confidence = r["rho"]
                    if entity not in allEntities:
                        index = len(allEntities)
                        allEntities.append(entity)
                    else:
                        index = allEntities.index(entity)
                    entityIndices.add(index)
                entityIndicesByTweet[statusId] = entityIndices
            except:
                print("error in line:" + line)
                print("res: " + str(res))
        matrix = []
        for i in range(0, len(allEntities)):
            matrix.append([0]*len(allEntities))
        for statusId, entityIndicesOfSingleTweet in entityIndicesByTweet.items():
            for i1 in entityIndicesOfSingleTweet:
                for i2 in entityIndicesOfSingleTweet:
                    if i1 != i2:
                        matrix[i1][i2] += 1 +  2 * corpus[statusId][2] + corpus[statusId][3]
        pickle.dump([allEntities, entityIndicesByTweet, numpy.array(matrix)], open( "./"+directory+(c[:-4]), "wb"))

''' note about results:
there are empty (or unicode incompatible lines in brexit (neutral) and election (neutral)). This will cause the
indices of WG data out of sync with the ordering in corpus. Hence will ignore these 2 topics. '''
