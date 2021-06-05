#docId,count,feild
#feild = 0:body,1:reference,2:links,3:category,4:InfoBox
from collections import Counter,defaultdict,OrderedDict

class BuildBlockDict():

    def __init__(self,indexPath):
        self.indexPath = indexPath
        self.BlockSize = 10000
        self.currentSize = 0
        self.blockCount = 0
        self.documentCount = 0
        self.BlockDict = defaultdict(str)
        self.feildDict = { 0:'b',1:'r',2:'l',3:'c',4:'i',5:'t'}


    def addPageToDict(self,pageDetails):
        pageTitleLst = pageDetails[1]
        pageEachTypeList = pageDetails[2]
        for feild,lst in enumerate(pageEachTypeList):
            counter = Counter(lst)
            for entry in counter.items():
                tempstr = str(self.documentCount) + "," + str(entry[1]) + "," + str(self.feildDict[feild]) + ":"
                self.BlockDict[entry[0]] += tempstr
        self.documentCount += 1
        
        titleCounter = Counter(pageTitleLst)
        for entry in titleCounter.items():
            tempstr = str(self.documentCount) + "," + str(entry[1]) + "," + str(self.feildDict[5]) + ":"
            self.BlockDict[entry[0]] += tempstr
        
        self.currentSize += 1
        print(self.currentSize)
        if self.currentSize == self.BlockSize:
            self.writeBlockToFile()
            


    def writeBlockToFile(self):
        if self.currentSize:
            self.blockCount += 1
            fileName = self.indexPath + "block" + str(self.blockCount)+".txt"
            with open(fileName, "w") as f: 
                for entry in sorted(self.BlockDict.keys()):
                    f.write(str(entry) + "$" + self.BlockDict[entry])
                    f.write("\n")
            self.currentSize = 0
            self.BlockDict = defaultdict(str)
        return self.blockCount    #write to file
