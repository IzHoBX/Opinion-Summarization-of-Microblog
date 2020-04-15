import http.server
import socketserver
import requests
import urllib
import json
import socket
import os
import ssl
import pickle
import random
from textblob import TextBlob
from http.server import BaseHTTPRequestHandler, HTTPServer

positive = set()
negative = set()
neutral = set()
all = []
SET = "/SET?"
state = "spacex"
SUBMIT = "/SUBMIT?"

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global state
        if SET in self.path and self.path.index(SET) == 0:
            state = self.path[len(SET):]
            prepareForTopic(state)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            return
        elif SUBMIT in self.path and self.path.index(SUBMIT) == 0:
            input =  self.path[len(SUBMIT):]
            input = input.replace("%20", " ")
            print(input)
            x = []
            result = TextBlob(input).sentiment.polarity
            if result < -0.05:
                c = "negative"
            elif result > 0.05:
                c = "positive"
            else:
                c = "neutral"
            x.append("sentiment:" + c)

            url = "https://wat.d4science.org/wat/tag/tag"
            params = {}
            params["lang"] = "en"
            params["gcube-token"] = "0fea3a55-cec4-4b2e-8dcc-2b9ccb6ed83c-843339462"
            urlForId = "https://wat.d4science.org/wat/title"
            paramsForId = {}
            paramsForId["gcube-token"] = "0fea3a55-cec4-4b2e-8dcc-2b9ccb6ed83c-843339462"

            # get annotations
            params["text"] = input
            data = urllib.parse.urlencode(params)
            res = requests.get(url, data)
            entities = []
            for r in res.json()["annotations"]:
                entity = r["title"]
                confidence = r["rho"]
                entities.append(entity)

            s = ""
            for e in entities:
                s += e
            x.append("entities:" + s)

            # get stored WG clusters
            meta = pickle.load(open("./" + state + "/" + c + "ClusteredWG", "rb"))
            # [allEntities, entityIndicesByTweet, numpy.array(matrix), listsOfNodesBelongingToTheSameCluster]


            # prepare for conversion from entity to ids
            try:
                f = open("./cache", "rb")
                titleToId = pickle.load(f)
                f.close()
            except FileNotFoundError:
                titleToId = {}
            for e in entities:
                if not e in titleToId:
                    paramsForId["title"] = e
                    data = urllib.parse.urlencode(paramsForId)
                    res = requests.get(urlForId, data)
                    titleToId[e] = res.json()["wiki_id"]

            # pull relatedness
            url = "https://wat.d4science.org/wat/relatedness/graph"
            params["relatedness"] = "jaccard"
            for title in meta[0]:
                data += "&ids=" + str(titleToId[title])
            for e in entities:
                data += "&ids=" + str(titleToId[e])
            res = requests.get(url, data)
            res = res.json()["pairs"]
            print("received pairwise relatedness data")
            print("total number of pairs:" + str(len(res)))
            scoreCache = {}
            for pair in res:
                id1 = pair["src_title"]["wiki_id"]
                id2 = pair["dst_title"]["wiki_id"]
                score = pair["relatedness"]
                scoreCache[(id1, id2)] = score

            indicesOfAssignedClusters = []
            # compute assignments
            for j in range(0, len(meta[3])):
                setOfIndicesOfEntitiesOfACluster = meta[3][j]
                sum = 0
                denom = 0
                for e in entities:
                    for indexFromCluster in setOfIndicesOfEntitiesOfACluster:
                        id1 = titleToId[e]
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
                            print("pulling outside of batch")
                            data = urllib.parse.urlencode(params)
                            data+="&ids="+str(id1)
                            data+="&ids="+str(id2)
                            res = requests.get(url, data)
                            try:
                                score = res.json()["pairs"][0]["relatedness"]
                            except:
                                #for some reason server not returning score for this pair
                                denom -= 1 #exclude this term for evaluation
                        denom += 1
                if denom == 0:#should only happen to zero-entity tweets
                    sum = 0
                else:
                    sum /= denom
                if sum > 0.001:
                    indicesOfAssignedClusters.append(j)

            clusterToIndicesOfAssignedTweet = pickle.load(open("./" + state +"/"+ c + "ClusterToAssignedTweets", "rb"))
            corpus = pickle.load(open("./"+state+"/corpus", "rb"))
            # inReplyStatusId, userId, numRetweet, numFavourite, text
            related = []
            for i in indicesOfAssignedClusters:
                for j in clusterToIndicesOfAssignedTweet[i]:
                    related.append(corpus[j][4])

            x = json.dumps({"res":x+related})
        else:
            global positive
            global negative
            global neutral
            global all
            print("received" + self.path)
            if self.path == "/positive":
                x = json.dumps({"res":positive})
            elif self.path == "/negative":
                x = json.dumps({"res":negative})
            elif self.path == "/neutral":
                x = json.dumps({"res":neutral})
            else:
                x = json.dumps({"res":all})
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(bytes(x,"utf-8"))
        self.wfile.close()
        return

def prepareForTopic(topic):
    global positive
    global negative
    global neutral
    global all
    corpus = pickle.load(open("./"+state+"/corpus", "rb"))
    # inReplyStatusId, userId, numRetweet, numFavourite, text
    positive = set()
    negative = set()
    neutral = set()
    all = []
    f = open("./" + topic + "/positiveReps", "rb")
    l = pickle.load(f)
    f.close()
    for index, post in l:
        positive.add(post)
    positive = list(positive)
    f = open("./" + topic + "/neutralReps", "rb")
    l = pickle.load(f)
    f.close()
    for index, post in l:
        neutral.add(post)
    neutral = list(neutral)
    f = open("./" + topic + "/negativeReps", "rb")
    l = pickle.load(f)
    f.close()
    for index, post in l:
        negative.add(post)
    negative = list(negative)
    f = pickle.load(open("./" + topic + "/positive.txt", "rb"))
    for id in f:
        all.append(corpus[id][4])
    f = pickle.load(open("./" + topic + "/negative.txt", "rb"))
    for id in f:
        all.append(corpus[id][4])
    f = pickle.load(open("./" + topic + "/neutral.txt", "rb"))
    for id in f:
        all.append(corpus[id][4])
    random.shuffle(all)

prepareForTopic("spacex")
print('starting server on port 7777...')

server_address = ("", 7777)
httpd = HTTPServer(server_address, MyHandler)
httpd.serve_forever()
