import pickle

directories = ["spacex"]
classes = ("/positive", "/negative", "/neutral")

count = 0

for directory in directories:
    corpus = pickle.load(open("./"+directory+"/corpus", "rb"))
    # inReplyStatusId, userId, numRetweet, numFavourite, text
    for c in classes:
        listOfStatusId = pickle.load(open("./" + directory+c+".txt", "rb"))
        replyGraph = {}
        for statusId in listOfStatusId:
            inReplyStatusId = corpus[statusId][0]
            if inReplyStatusId != -1 and inReplyStatusId in listOfStatusId:
                count += 1
                if inReplyStatusId in replyGraph:
                    replyGraph[inReplyStatusId].append(statusId)
                else:
                    replyGraph[inReplyStatusId] = [statusId]
        pickle.dump(replyGraph, open("./" + directory+c+"ReplyGraph", "wb"))

print(count)
