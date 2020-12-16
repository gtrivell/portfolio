from nltk.tokenize import TweetTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import VarianceThreshold
from sklearn.neural_network import MLPClassifier

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
print("Done\n\nVectorizing data...")

vectorizer = TfidfVectorizer(max_df = 0.15,min_df=0.0013)
X = vectorizer.fit_transform(ClassificationHolder)
print ("Train file dimensions:")
print(X.shape)

selector = VarianceThreshold(0.00003)
X2 = selector.fit_transform(X)

print("\nCreating MLP model...")
GNB = MLPClassifier(solver='lbfgs', verbose=True,random_state=1)
GNB2 = GNB.fit(X2, ClassificationIndex)

print("\nApplying test data on model...")

TestClassificationHolder = []

for cnt, line in enumerate(testFile):
    TestClassificationHolder.append(" ".join(tknzr.tokenize(line)))
    
XTest = vectorizer.transform(TestClassificationHolder)
XTest2 = selector.transform(XTest)
resultFile = open("resultsMLP.dat","w+")
count = 0    
resultsHolder = GNB2.predict(XTest2)
for entry in resultsHolder:
        if(entry == '0'):
            resultFile.write("0\n")
        else:
            resultFile.write("1\n")
print("Results in resultsMLP.dat")
print("Finished!")