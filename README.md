# Opinion-Summarization-of-Microblog

NOTE: This document details some the implementations related procedures and tools for the project. For theoretical aspects regarding to designs, please refer to our report.

## Requirements
The followings are the frameworks and libraries that were used in the project. If you want to run them on your computer, please ensure the followings are installed.
front-end:
1. We have used expo to build our front end using React. To run the build and run it, please:
  - install npm
  - install expo
    sudo npm install -g expo-cli
2. The backend is built using python 3.7. The required modules are:
  - pickle
  - numpy
  - requests
  - urllib
  - scikit-network==0.12.1 (please do not use the latest version 0.13.1 as there is a bug in it and will not start)
  - TextBlob
  - sklearn

## Front-end
The directory called `/AwesomeProject` stores the code for front-end, which we built using expo on React.

## Back-end
The directory called `/dataset` contains all codes for the backend. From there, you can see a the following files and directories:
Filename or directory name| Purpose | Output File that stores the results
---------|--------|---------
brexit, election, isis, nobel, note7, spacex | These directories contains texts of twitter posts of the respective topics. Also, they contain files that store intermediate data structures during the pipelined processing. For the descriptions below, we use placeholder `TOPIC` to represent any of these directories. | -
SentimentClassifier.py | First step of the processing procedures. It classifies twitter posts of each topic into 3 sentiment classes, namely positive, negative and neutral. For the descriptions below, we use placeholder `CLASS` to represent any of the 3 classes. | TOPIC/CLASS.txt
CorpusToList.py | It reads all the twitter posts in each sentiment class, store them in list and the list is saved in a file. This is necessary to make later steps easier with list indexing. | TOPIC/CLASSlistCorpus
WGConstruct.py | Second step. It constructs a WordGraph for each sentiment class. | TOPIC/CLASS
GraphClustering.py | Third step. It clusters the WGs that are constructed in the previous step. Each of the resulting clusters represents a topical aspect in the sentiment class. | /TOPIC/CLASSClusteredWG
TweetToClusterAssignment.py | Fourth step. Assigns each twitter post back to Graph Clusters of within its sentiment class. When this code is run, it will create/extends the `cache` file to cache data pulled from WAT REST API. | cache, /TOPIC/CLASS/ClusterToAssignedTweets
TfIdfSummarizing.py | Last step. For each graph clusters, it will take all the Tweets that are assigned to it and pick the one best summarizing Tweet to represent the cluster. | /TOPIC/CLASSReps

### Credits
These are some of the resources that helped us greatly by simplifying/providing implementation for some steps.
1. Dataset from https://github.com/nguyenlab/summarization-tsix
2. WAT REST API for tagging texts with entities and entity-relatedness computation at https://sobigdata.d4science.org/web/tagme/wat-api
