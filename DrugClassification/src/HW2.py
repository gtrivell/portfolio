from sklearn import tree
from nltk.tokenize import TweetTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import VarianceThreshold

print("\tK Drug Classification\n")
trainFileName = input("Input the training file name: ")
testFileName = input("Input the test file name: ")
trainFile = open(trainFileName, "r")
testFile = open(testFileName, "r")

ClassificationHolder = []
ClassificationIndex = []
tknzr = TweetTokenizer()

print("\nProcessing train file...")

for cnt, line in enumerate(trainFile):
    ClassificationIndex.append(line[0])
    ClassificationHolder.append(" ".join(tknzr.tokenize(line[2:])))
print("Done\n\nVectorizing and creating tree...")

vectorizer = TfidfVectorizer(max_df = 0.15,min_df=0.0013)
X = vectorizer.fit_transform(ClassificationHolder)
print ("Train file dimensions:")
print(X.shape)

selector = VarianceThreshold(0.00000)
X2 = selector.fit_transform(X)

clf = tree.DecisionTreeClassifier(min_samples_leaf=7)
clf = clf.fit(X2, ClassificationIndex)
print("Number of nodes in tree:")
print(clf.get_n_leaves())
print("Depth of tree:")
print(clf.get_depth())

print("\nApplying test data on tree...")

TestClassificationHolder = []

for cnt, line in enumerate(testFile):
    TestClassificationHolder.append(" ".join(tknzr.tokenize(line)))
    
XTest = vectorizer.transform(TestClassificationHolder)
XTest2 = selector.transform(XTest)
resultFile = open("results.dat","w+")
count = 0    
resultsHolder = clf.predict(XTest2)
for entry in resultsHolder:
        if(entry == '0'):
            resultFile.write("0\n")
        else:
            resultFile.write("1\n")
print("Results in results.dat")
print("Finished!")