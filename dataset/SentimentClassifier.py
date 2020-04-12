import os
from textblob import TextBlob

directories = ("brexit", "election", "isis", "nobel", "note7", "spacex")

for directory in directories:
    pos = open(directory + "/positive.txt", "w")
    neg = open(directory + "/negative.txt", "w")
    neu = open(directory + "/neutral.txt", "w")
    for subdir in os.listdir("./" + directory):
        if subdir == "positive.txt" or subdir == "neutral.txt" or subdir == "negative.txt" or subdir == ".DS_Store":
            continue
        for filename in os.listdir("./"+directory+"/"+subdir):
            f = open("./"+directory+"/"+subdir+"/"+filename)
            for line in f:
                result = TextBlob(line).sentiment.polarity
                if result < -0.05:
                    neg.write(line)
                elif result > 0.05:
                    pos.write(line)
                else:
                    neu.write(line)
            f.close()

pos.close()
neg.close()
neu.close()
