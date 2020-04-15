import pickle

directories = ("brexit", "election", "isis", "nobel", "note7", "spacex")
classes = ("/positive.txt", "/negative.txt", "/neutral.txt")

for directory in directories:
    for c in classes:
        src = open("./" + directory + c, "r")
        a = []
        for line in src:
            a.append(line)
        pickle.dump(a, open("./" + directory + c[:-4] + "listCorpus", "wb"))
        src.close()
