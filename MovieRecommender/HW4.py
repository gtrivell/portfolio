from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import normalize
import numpy as np

print("\tMovie Reccomender")
trainFile = open("train.dat", "r")
testFile = open("test.dat", "r")
tagsFile = open("tags.dat", "r")
movieActorsFile = open("movie_actors.dat", "r", errors='ignore')
movieDirectorsFile = open("movie_directors.dat", "r", errors='ignore')
movieGenresFile = open("movie_genres.dat", "r")
movieTagsFile = open("movie_tags.dat", "r")

ClassificationHolder = []
ClassificationIndex = []
Tags = dict()
movieIDIndex = []
movieProfiles = []

#Tags have the ID for a key as a string ex. Tags["21"] = "bill murray"
print("\nProcessing tags...")
firstLineDone = False
for cnt, line in enumerate(tagsFile):
    if(firstLineDone):   
        Tags[line.split('\t')[0]] = line.split('\t')[1]
    else:
        firstLineDone = True
print("Done\n\nCreating movie profiles...")

print("\tProcessing actors...")
firstLineDone = False
movieIDHolder = 0
lineHolder = []
for cnt, line in enumerate(movieActorsFile):
    lineHolder = line.split('\t')
    if(firstLineDone):
        if(lineHolder[0] != movieIDHolder): #New movie found in file
            movieIDIndex.append(lineHolder[0])
            movieIDHolder = lineHolder[0]
            #Create a string describing movie and append 
            movieProfiles.append("")
            if(int(lineHolder[3]) < 5):
                movieProfiles[len(movieProfiles) - 1] = movieProfiles[len(movieProfiles) - 1] + lineHolder[1] + " "
        else:
            if(int(lineHolder[3]) < 5):
                movieProfiles[len(movieProfiles) - 1] = movieProfiles[len(movieProfiles) - 1] + lineHolder[1] + " "
    else:
        firstLineDone = True

print("\tProcessing directors...")
firstLineDone = False
lineHolder = []
for cnt, line in enumerate(movieDirectorsFile):
    lineHolder = line.split('\t')
    if(firstLineDone):
        if(movieIDIndex[cnt - 1] == lineHolder[0]):
            movieProfiles[cnt - 1] = movieProfiles[cnt - 1] + lineHolder[1] + " "
        else:
            for count, entry in enumerate(movieIDIndex):
                if(entry == lineHolder[0]):
                    movieProfiles[count] = movieProfiles[count] + lineHolder[1] + " "
                    break
    else:
        firstLineDone = True      

print("\tProcessing genres...")
firstLineDone = False
lineHolder = []
for cnt, line in enumerate(movieGenresFile):
    lineHolder = line.split('\t')
    if(firstLineDone):
        for count, entry in enumerate(movieIDIndex):
            if(entry == lineHolder[0]):
                movieProfiles[count] = movieProfiles[count] + lineHolder[1].rstrip() + " "
                break
    else:
        firstLineDone = True
       
print("\tProcessing tags...")
firstLineDone = False
lineHolder = []
tagIDHolder = []
tagWeightHolder = []
movieIDHolder = 1
for cnt, line in enumerate(movieTagsFile):
    lineHolder = line.split('\t')
    if(firstLineDone):
        if(lineHolder[0] != movieIDHolder):
            for count, tag in enumerate(tagIDHolder):
                for count2, entry in enumerate(movieIDIndex):
                    if(entry == lineHolder[0]):
                        for x in range(int(tagWeightHolder[count])):
                            movieProfiles[count2] = movieProfiles[count2] + Tags[tag].rstrip().replace(" ", "_") + " "
                        break
            tagIDHolder = []
            tagWeightHolder = []
        tagIDHolder.append(lineHolder[1])
        tagWeightHolder.append(lineHolder[2].rstrip())
    else: 
        firstLineDone = True
print("Example profile:")
print(movieProfiles[len(movieProfiles) - 2]) #kate_winslet kathy_bates leonardo_di_caprio michael_shannon sam_mendes Drama Romance chuck_palahniuk       
print("Done\n")

print("\nCreating utility matrix...")
firstLineDone = False
firstDone = False
userIDHolder = 0
userIDCountHolder = 0
userIDIndex = []
userProfiles = []
for cnt, line in enumerate(trainFile):
    if(cnt % 10000 == 0):
        print(cnt)
    lineHolder = line.split(' ')
    if(firstLineDone):
        if(lineHolder[0] != userIDHolder): #New user found in file
            if(firstDone):
                while(userIDCountHolder < len(movieProfiles)):
                    userProfiles[len(userProfiles) - 1] = userProfiles[len(userProfiles) - 1] + "0 "
                    userIDCountHolder = userIDCountHolder + 1
            userIDIndex.append(lineHolder[0])
            userIDHolder = lineHolder[0]
            #Create a string describing movie and append 
            userProfiles.append("")
            for count, entry in enumerate(movieIDIndex):
                if(entry == lineHolder[1]):
                    userProfiles[len(userProfiles) - 1] = userProfiles[len(userProfiles) - 1] + lineHolder[2].rstrip() + " "
                    userIDCountHolder = count + 1
                    break
                else: 
                    userProfiles[len(userProfiles) - 1] = userProfiles[len(userProfiles) - 1] + "0 "
            firstDone = True
        else:
            for count, entry in enumerate(movieIDIndex[userIDCountHolder:]):
                if(lineHolder[1] + "" not in movieIDIndex):
                    break
                else:
                    if(entry == lineHolder[1]):
                        userProfiles[len(userProfiles) - 1] = userProfiles[len(userProfiles) - 1] + lineHolder[2].rstrip() + " "
                        userIDCountHolder = userIDCountHolder + count + 1
                        break
                    else: 
                        userProfiles[len(userProfiles) - 1] = userProfiles[len(userProfiles) - 1] + "0 "
    else:
        firstLineDone = True
while(userIDCountHolder < len(movieProfiles)): #The final line left the loop without filling out with 0's
    userProfiles[len(userProfiles) - 1] = userProfiles[len(userProfiles) - 1] + "0 "
    userIDCountHolder = userIDCountHolder + 1

print("Done\n\nAmount of movies:")
print(len(movieProfiles)) #10174
print("\nAmount of users:")
print(len(userProfiles)) #2113
print("\nCreating something...")

#Turn the user profiles in to arrays of doubles rather than just the string representation
userProfilesRedux = []
for count, user in enumerate(userProfiles): 
    tempArray = userProfiles[count].split(' ')[:-1]
    tempArray2 = []
    for cnt, entry in enumerate(tempArray):
        if(entry == "0"):
            tempArray2.append(float(0))
        else:
            tempArray2.append(float(entry))
    userProfilesRedux.append(np.array(tempArray2))
    tempArray2 = []

#Sample prints
#print(len(userProfiles[0])) #20398
#print(len(userProfiles[1])) #20734
#print(len(userProfiles[2])) #20372
#print(len(userProfilesRedux[0])) #10174
#print(len(userProfilesRedux[1])) #10174
#print(len(userProfilesRedux[2])) #10174
#print(len(userProfilesRedux[3])) #10174

#Failed attempt at using matrix factorization
#The resulting array(H) was full of 0's instead of a number between 0 and 5
"""
model = NMF(n_components=2113, verbose=True)

W = model.fit_transform(userProfilesRedux)
H = model.components_
print("Done")
print(H)

testFile = open("test.dat", "r")
firstLineDone = False
userIndex = 0
movieIndex = 0
rating = 0
resultFile = open("results.dat","w+")
for line in testFile:
    lineHolder = line.split(' ')
    if(firstLineDone):
        if lineHolder[1].rsplit()[0] not in movieIDIndex:
            movieIndex = 0
        else:
            movieIndex = movieIDIndex.index(lineHolder[1].rsplit()[0])
        userIndex = userIDIndex.index(lineHolder[0])
        rating = H[userIndex][movieIndex]
        rating = round(rating, 1)
        if(rating > 5):
            rating = 5
        resultFile.write(str(rating) +"\n")
    else:
        firstLineDone = True        
"""

firstLineDone = False
testFile = open("test.dat", "r")
resultFile = open("result.dat","w+")
clf = MLPRegressor(max_iter = 50, solver = 'lbfgs', hidden_layer_sizes = 15)
vectorizer = TfidfVectorizer()
for cnt, line in enumerate(testFile):
    print(cnt)
    lineHolder = line.split(' ')
    if(firstLineDone):
        
        if(lineHolder[1].rsplit()[0] + "" not in movieIDIndex):
            print("ISSUE! New movie found")
            resultFile.write("3.0\n")
        elif(lineHolder[0] + "" not in userIDIndex):
            print("ISSUE! New user found")
            resultFile.write("3.0\n")
        else:
            movieIndex = movieIDIndex.index(lineHolder[1].rsplit()[0] + "")
            movie = movieProfiles[movieIndex]
            userIndex = userIDIndex.index(lineHolder[0])
            Y = userProfilesRedux[userIndex]
            trueY = []
            X = []
            for cnt, entry in enumerate(Y):
                if(entry != 0.0):
                    X.append(movieProfiles[cnt])
                    trueY.append(entry)
            
            Xt = vectorizer.fit_transform(X)
            Xt = normalize(Xt)
            moviet = vectorizer.transform([movie])
            trueY = np.asarray(trueY,dtype=np.float64)
            clf.fit(Xt,trueY)
            rating = clf.predict(moviet)
            
            rating1 = round(rating[0], 1)
            if(rating1 > 5):
                rating1 = 5
            #print(rating1)
            resultFile.write(str(rating1) + "\n")
    else:
        firstLineDone = True
resultFile.close()
print("Done")