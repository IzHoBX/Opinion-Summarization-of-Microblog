import sknetwork.clustering as sc
import pickle

# directories = ("spacex", "brexit", "election", "isis", "nobel", "note7")
directories = ["spacex"]
classes = ("/positive", "/negative", "/neutral")
l = sc.Louvain()

for directory in directories:
    for c in classes:
        meta = pickle.load(open("./" + directory + c, "rb"))
        # [allEntities, entityIndicesByTweet, numpy.array(matrix)]
        clustering = l.fit(meta[2]).labels_
        print("found " + str(max(clustering)) + " for " + directory +" " + c)
        graphClusters = []
        for i in range(0, max(clustering)+1):
            graphClusters.append([])
        for i in range(0, len(clustering)):
            graphClusters[clustering[i]].append(i)
        pickle.dump([meta[0], meta[1], meta[2], graphClusters], open( "./"+directory+c+"ClusteredWG", "wb"))
