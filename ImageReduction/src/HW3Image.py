from nltk.tokenize import TweetTokenizer
from sklearn.feature_selection import VarianceThreshold
import random
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import normalize
from sklearn.manifold import TSNE

print("\tK-Means Algorithm - Image Version\n")
testFileName = input("Input the test file name: ")
testFile = open(testFileName, "r")
#K = input("Input K: ")
K = 10

print("Creating initial cluster...")
LineHolder = []
Clusters = []
clusterCenters = []
temp = []
tknzr = TweetTokenizer()
for cnt, line in enumerate(testFile):
    line = line.replace(",", " ")
    for number in tknzr.tokenize(line):
        temp.append(float(number))
    LineHolder.append(temp)
    temp = []
print("Done\n\nStarting feature selection/reduction...")

selector = VarianceThreshold(0)
LineHolder = selector.fit_transform(LineHolder)
LineHolder = LineHolder.tolist()
LineHolder = TSNE(method = 'exact').fit_transform(LineHolder)
LineHolder = normalize(LineHolder)
LineHolder = LineHolder.tolist()

Clusters.append(LineHolder)
ClustersCopy = Clusters.copy()
currHighestSSE = 0
currHighest = []
tempNumber = 0

print("Done\n\nStarting bisection of clusters...")
print("Note: Counter resets if a better bisection of highest SSE cluster is found")
while(len(Clusters) < K):
    print("\tNumber of Clusters: " + str(len(Clusters)))
    #Get cluster with the highest SSE
    for cnt, cluster in enumerate(Clusters):
        if(clusterCenters == []):
            clusterCenters.append(cluster[random.randint(0,(len(cluster) - 1))])
        for i in cluster:
            tempNumber = tempNumber + mean_squared_error(clusterCenters[cnt], i)
        if(len(cluster) == 0):
            tempNumber = 0
        else:
            tempNumber = tempNumber / len(cluster)
        if(tempNumber > currHighestSSE):
            currHighestSSE = tempNumber
            currHighest = cluster
            currHIndex = cnt
        tempNumber = 0
    print("Highest SSE cluster selected")
    
    SSE1 = 0
    SSE2 = 0
    overallSSE = 0
    tempNumber = 0
    cluster1 = []
    cluster2 = []
    tempClusterCenters = []
    center1 = []
    center2 = []
    finalSSE = 1000000
    finalCluster1 = []
    finalCluster2 = []
    finalClusterCenters = []
    test = 0
    ctr = 0
    furthestTemp = 0
    furthestCenter1 = []
    furthestCenter2 = []
    firstRun = True
    
    for x in LineHolder[0]:
        center1.append(0)
        center2.append(0)
    while(finalSSE != test or ctr != 40):
        if(finalSSE != test):
            ctr = 0
        print("Counter: " + str(ctr))
        ctr = ctr + 1
        test = finalSSE
        if(firstRun):
            for cl in currHighest:
                if(mean_squared_error(cl, clusterCenters[currHIndex]) > furthestTemp):
                    furthestTemp = mean_squared_error(cl, clusterCenters[currHIndex])
                    furthestCenter1 = cl
            tempClusterCenters.append(furthestCenter1)
            furthestTemp = 0
            for cl in currHighest:
                if(mean_squared_error(cl, clusterCenters[currHIndex]) > furthestTemp):
                    if(cl != tempClusterCenters[0]):
                        furthestTemp = mean_squared_error(cl, clusterCenters[currHIndex])
                        furthestCenter2 = cl
            tempClusterCenters.append(furthestCenter2)
            firstRun = False
        else:          
            tempClusterCenters.append(currHighest[random.randint(0,(len(currHighest) - 1))])
            tempNumber = random.randint(0,(len(currHighest) - 1))
            while(currHighest[tempNumber] == tempClusterCenters[0]):
                tempNumber = random.randint(0,(len(currHighest) - 1))
            tempClusterCenters.append(currHighest[tempNumber])
        
        for i in currHighest:
            if(mean_squared_error(tempClusterCenters[0], i) < mean_squared_error(tempClusterCenters[1], i)):
                cluster1.append(i)
            else:
                cluster2.append(i)
        tempNumber = 0
        for a in cluster1:
            tempNumber = tempNumber + mean_squared_error(tempClusterCenters[0], a)
        SSE1 = tempNumber / len(cluster1)
        tempNumber = 0
        for b in cluster2:
            tempNumber = tempNumber + mean_squared_error(tempClusterCenters[1], b)
        SSE2 = tempNumber / len(cluster2)
        overallSSE = (SSE1 + SSE2) / 2

        if(overallSSE < finalSSE):
            finalSSE = overallSSE
            finalCluster1 = cluster1
            finalCluster2 = cluster2
            clustCount = 0
            for entry in finalCluster1:
                for cnt, line in enumerate(LineHolder[0]):
                    center1[cnt] = center1[cnt] + entry[cnt]
                    clustCount = clustCount + 1
            for cnt, line in enumerate(LineHolder[0]):
                center1[cnt] = center1[cnt] / clustCount
            
            clustCount = 0
            for entry in finalCluster2:
                for cnt, line in enumerate(LineHolder[0]):
                    center2[cnt] = center2[cnt] + entry[cnt]
                    clustCount = clustCount + 1
            for cnt, line in enumerate(LineHolder[0]):
                center2[cnt] = center2[cnt] / clustCount
            finalClusterCenters = [center1, center2]
        center1 = []
        center2 = []
        for x in LineHolder[0]:
            center1.append(0)
            center2.append(0)
        cluster1 = []
        cluster2 = []
        tempClusterCenters = []
    #print(finalSSE) 
    Clusters.remove(currHighest)
    Clusters.append(finalCluster1)
    Clusters.append(finalCluster2)
    clusterCenters.pop(currHIndex)
    clusterCenters.append(finalClusterCenters[0])
    clusterCenters.append(finalClusterCenters[1])
    #Readjust every point now that there are competing centers
    print("\nPre-adjusted cluster lengths:")
    for cnt, clusters in enumerate(Clusters):
        print(len(clusters))
        for cnte, c in enumerate(clusterCenters):
            for point in clusters:
                currLowest = mean_squared_error(clusterCenters[cnt], point)
                if(mean_squared_error(c, point) < currLowest):
                    Clusters[cnte].append(point)
                    clusters.remove(point)
                    currLowest = mean_squared_error(c, point)
    print("Adjusted cluster lengths:")
    for clusters in Clusters:
        print(len(clusters))
    finalClusterCenters = []
    currHighestSSE = 0
    currHighest = []
    tempNumber = 0
    currHIndex = 0
    print("\n")
    
print("Finished calculations. Writing to file...")
resultFile = open("results-image.dat","w+")
for line in ClustersCopy:
    for realLine in line:
        for cnt, cluster in enumerate(Clusters):
            if realLine in cluster:
                resultFile.write(str(cnt + 1) + "\n")
print("Finished!")