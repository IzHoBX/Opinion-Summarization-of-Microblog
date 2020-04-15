# reference: https://github.com/Yogayu/weibo-summary/blob/master/weiboApplication/Algorithms/Hybird-TFIDF.py
from math import log
import numpy as np
import sys, os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import string

# directories = ("spacex", "brexit", "election", "isis", "nobel", "note7")
directories = ["spacex"]
classes = ("/positive", "/negative", "/neutral")

for directory in directories:
    for c in classes:
        clusterToIndicesOfAssignedTweet = pickle.load(open("./" + directory + c + "ClusterToAssignedTweets", "rb"))
        corpus = pickle.load(open("./" + directory + c + "listCorpus", "rb"))
        clusterReps = []
        for cluster in clusterToIndicesOfAssignedTweet:
            if len(cluster) == 0:
                continue
            allPosts = []
            for indexOfTweet in cluster:
                allPosts.append(corpus[indexOfTweet])

            v = TfidfVectorizer(stop_words="english")
            X = v.fit_transform(allPosts)
            hybridTfIdf = X.sum(axis=0)

            # calculates weight for each document
            weights = []
            for i in range(X.shape[0]):
                row = X[i].toarray()[0]
                score_sum = 0
                for j in range(0, len(row)):
                    if row[j] > 0:
                        score_sum += row[j] * hybridTfIdf.item(0, j) #because frequency in post matters
                # this represents the desired document length
                MINIMUM_THRESHOLD = 8
                normalizing_factor = max(MINIMUM_THRESHOLD, len(allPosts[i].split(' ')))
                weights.append(score_sum/normalizing_factor)
            rowIndexOfRep = np.argmax(weights)
            postIndexAtRowIndex = cluster[rowIndexOfRep]

            ''' no need to do similarity measure since we are taking only 1 doc
            # constructing normal tf idf for similarity measure
            cos_mat = cosine_similarity(X, X)

            chosen_summary_indices = []
            similarityThreshold = 0.77 #best according to sharifi
            for index in sorted_indices:
                    if len(chosen_summary_indices) == 0:
                        chosen_summary_indices.append(index)
                    else:
                        for i in chosen_summary_indices:
                            if cos_mat[index][i] < similarityThreshold:
                                chosen_summary_indices.append(index)'''
            clusterReps.append((postIndexAtRowIndex, corpus[postIndexAtRowIndex]))
        pickle.dump(clusterReps, open("./" + directory + c + "Reps", "wb"))
        print(clusterReps)
