# Opinion-Summarization-of-Microblog

NOTE: This document details some the implementations related procedures and tools for the project. For theoretical aspects regarding to designs, please refer to our report.

## Requirements
The followings are the frameworks and libraries that were used in the project. If you want to run them on your computer, please ensure the followings are installed.
front-end:
1. We have used expo to build our front end using React. To run the build and run it, please:
  - install npm (Node JS)
  - install expo: `sudo npm install -g expo-cli`
2. The backend is built using python 3.7. The required modules are:
  - pickle
  - numpy
  - requests
  - urllib
  - scikit-network==0.12.1 (please do not use the latest version 0.13.1 as there is a bug in it and will not start)
  - TextBlob
  - sklearn

## Executing
To try out our system,
1. Navigate to the directory `/dataset` and run the backend interfacing script using command `python backend.py`. It will open up a localhost server that serves over port 7777.
2. Run the front end code by navigating into the directory `/Frontend`, then run command `npm start`.
3. A tab will be opened on your default web browser shortly. Expect a terminal window to be spawned as well.
4. In the web browser tab, select `Run in web browser` on the menu pane on your left.
5. The frontend project will now build. It may take upto 1 minute. You can see the progress in the terminal window.
6. When the build is completed, another browser tab will be spawned, showing a page titled "summarized & classified posts".
7. Congratulations! You have now access to our system.

## Front end features
Since this project is more of a Proof-of-Concept, it does not have full features of a social media. Also, since react-native is optimised for mobile, some of the visual elements are less elegant when browsing through web browsers. Here are the features provided through the frontend:
### Home tab
1. In the **home** tab, there will be a list showing summarized posts. Each of this post are picked to represent one or more topical aspect. By default, posts of *positive* sentiment are shown.
2. To change to another sentiment, click on **neutral** and **negative** button on the top of the **home** tab. The list will be updated.
3. To see all posts, i.e. not classified and not summarized, click on **all** button.
### Add tab
1. The **Add** tab showcases the classification capability in our system.
2. Type in the content you wish to post in the "What's on your mind" text box. Try writing as you would in Twitter, i.e. Microblog style.
3. Click **Publish**. An alert dialog will pop up in at most 30 seconds.
4. In the alert dialog, it will show, in the following order:
* The sentiment that our system detects the input as.
* List of entities that our system detects from the input
* A list of other posts in the corpus that our system detects as relevant to the input. It does not necessarily means the input is a summary of all those posts, however.
4. Note that the input is not added to the corpus in the system despite the name of the **Publish** button.

## Front-end
The directory called `/Frontend` stores the code for front-end, which we built using expo on React.

## Back-end
The directory called `/dataset` contains all codes for the backend. From there, you can see a the following files and directories:
Filename or directory name| Purpose | Output File that stores the results
---------|--------|---------
backend.py | The script that serves REST API to the front end over localhost port 7777. | -
brexit, election, isis, nobel, note7, spacex | These directories contains texts of twitter posts of the respective topics. Also, they contain files that store intermediate data structures during the pipelined processing. For the descriptions below, we use placeholder `TOPIC` to represent any of these directories. | -
SentimentClassifier.py | First step of the processing procedures. It classifies twitter posts of each topic into 3 sentiment classes, namely positive, negative and neutral. For the descriptions below, we use placeholder `CLASS` to represent any of the 3 classes. | TOPIC/CLASS.txt
CorpusToList.py | It reads all the twitter posts in each sentiment class, store them in list and the list is saved in a file. This is necessary to make later steps easier with list indexing. | TOPIC/CLASSlistCorpus
WGConstruct.py | Second step. It constructs a WordGraph for each sentiment class. | TOPIC/CLASS
GraphClustering.py | Third step. It clusters the WGs that are constructed in the previous step. Each of the resulting clusters represents a topical aspect in the sentiment class. | /TOPIC/CLASSClusteredWG
TweetToClusterAssignment.py | Fourth step. Assigns each twitter post back to Graph Clusters of within its sentiment class. When this code is run, it will create/extends the `cache` file to cache data pulled from WAT REST API. | cache, /TOPIC/CLASS/ClusterToAssignedTweets
TfIdfSummarizing.py | Last step. For each graph clusters, it will take all the Tweets that are assigned to it and pick the one best summarizing Tweet to represent the cluster. | /TOPIC/CLASSReps

## Credits
These are some of the resources that helped us greatly by simplifying/providing implementation for some steps.
1. Dataset from https://github.com/nguyenlab/summarization-tsix
2. WAT REST API for tagging texts with entities and entity-relatedness computation at https://sobigdata.d4science.org/web/tagme/wat-api
