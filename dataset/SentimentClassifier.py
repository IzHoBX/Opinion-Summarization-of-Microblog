import os
from textblob import TextBlob
import pickle

directories = ("isis", "nobel", "note7")

for directory in directories:
    pos = []
    neg = []
    neu = []
    f = open("./"+directory+"/"+directory)
    data = f.read()
    eachPostLine = data.split("\t")
    corpus = {}
    for line in eachPostLine:
        if line == "":
            continue
        fields = line.split("|||")
        # statusId, inReplyStatusId, userId, numRetweet, numFavourite, text
        linedata = []
        statusId = int(fields[0])
        inReplyStatusId = int(fields[1])
        linedata.append(inReplyStatusId)
        userId = fields[2]
        linedata.append(userId)
        numRetweet = int(fields[3])
        linedata.append(numRetweet)
        numFavourite = int(fields[4])
        linedata.append(numFavourite)
        text = fields[5]
        linedata.append(text)
        result = TextBlob(text).sentiment.polarity
        if result < -0.05:
            neg.append(statusId)
        elif result > 0.05:
            pos.append(statusId)
        else:
            neu.append(statusId)
        corpus[statusId] = linedata
    f.close()
    pickle.dump(corpus, open("./"+directory+"/corpus", "wb"))
    pickle.dump(pos, open("./" + directory + "/positive.txt", "wb"))
    pickle.dump(neg, open("./" + directory + "/negative.txt", "wb"))
    pickle.dump(neu, open("./" + directory + "/neutral.txt", "wb"))

# http://wis.ewi.tudelft.nl/websci11
