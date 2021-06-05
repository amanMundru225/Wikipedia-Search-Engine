from bisect import bisect_left 
from collections import defaultdict
import math
import string
from nltk.stem import PorterStemmer
from time import time
import sys

class searchQueries:
    def __init__(self,indexPath):
        self.titleSeekList = []
        self.inMemoryIndex = []
        self.inMemoryDocIds = []
        self.inMemoryWords = []
        self.wordsPerDocument = []
        self.indexPath = indexPath
        self.readStats()
        self.loadSeekTitleFile()
        self.loadInMemoryIndex()
        self.loadWordsPerDocument()
        self.ps = PorterStemmer()
        self.formStopWordSet()

    def formStopWordSet(self):
        self.stopWordSet = set()
        with open('stopwords.txt','r') as file: 
            for line in file:     
                for word in line.split():           
                    self.stopWordSet.add(word)
        return 
    

    def readStats(self):
        with open('indexStats.txt','r') as file: 
            self.documentCount = int(file.readline().split(":")[1])
        

    def loadSeekTitleFile(self):
        with open('seekTitleFile.txt','r') as file: 
            for entry in file:
                entries = entry.split(":")
                self.titleSeekList.append(entries)
    

    
    def loadWordsPerDocument(self):
        with open('wordsPerDocument.txt','r') as file: 
            self.wordsPerDocument = file.readline().split(",")[:-1]
        
    
    
    def loadInMemoryIndex(self):
        with open('InMemoryIndex.txt','r') as file: 
            for entry in file:
                lst = entry.split(":")
                self.inMemoryIndex.append(lst)
    
    def cleanQuery(self,query):
        punctuations = string.punctuation
        table = punctuations.maketrans(punctuations+string.ascii_uppercase," "*len(punctuations)+string.ascii_lowercase,string.digits)
        cleanQueryWordList = query.translate(table).split()
        stoppedStemmedWords = [self.ps.stem(word) for word in cleanQueryWordList if word not in self.stopWordSet]
        return stoppedStemmedWords


    def search(self,filePath):
        lst = []
        with open(filePath,"r") as file:
            for query in file:
                print(query)
                if ":" in query:
                    ts = time()
                    result =self.feildQuery(query)
                    diff = time() - ts
                    result.append([diff,diff/len(result)])
                    lst.append(result)
                    
                else:
                    ts = time()
                    result = self.normalTextQuery(query)
                    diff = time() - ts
                    result.append([diff,diff/len(result)])
                    lst.append(result)
                    
        return lst
    

       
    def getPostingOfWord(self,word):
        if not self.inMemoryWords:
            self.inMemoryWords = [entry[0] for entry in self.inMemoryIndex]
        idx = bisect_left(self.inMemoryWords,word)-1
        seekPos,fileNumber = self.inMemoryIndex[idx][1].split("_")
        fileNumber = fileNumber.strip("\n")
        f = open(self.indexPath + "Index_" + str(fileNumber)+ ".txt" ,"r")
        #print(self.indexPath + "Index_" + str(fileNumber)+ ".txt")
        f.seek(int(seekPos))
        for idx,line in enumerate(f):
            if (idx == 1025) or not line:
                return []
            else:
                wordtemp,posting = line.split("$")
                if wordtemp == word:
                    return posting.split(":")[:-1]


    def getTitle(self,docId):
        if not self.inMemoryDocIds:
            self.inMemoryDocIds = [int(entry[0]) for entry in self.titleSeekList]
        idx = bisect_left(self.inMemoryDocIds,docId)
        if idx == 0:
            start = 0
        else:
            start = self.inMemoryDocIds[idx-1]
        seekPos = self.titleSeekList[idx][1].strip("\n")
        f = open("titles.txt","r")
        f.seek(int(seekPos))
        for en,line in enumerate(f):
            if (en == 2049) or not line:
                return ""
            else:
                if start + en == docId:
                    return line.strip("\n")
        
        



    def normalTextQuery(self,query):
        k,text = query.split(",")
        cleanQueryWords = self.cleanQuery(text)
        dict = defaultdict(int)
        for word in cleanQueryWords:
            postingList = self.getPostingOfWord(word)
            if not postingList:
                continue
            word_idf = self.documentCount / len(postingList)
            idf = math.log(word_idf)
            for posting in postingList:
                lst = posting.split(",")
                docId = int(lst[0])
                count = int(lst[1])
                if int(self.wordsPerDocument[docId]) == 0:
                    continue
                if(lst[2] == "i"):
                    dict[docId] += (3 * count * idf) / int(self.wordsPerDocument[docId])
                elif(lst[2] == "t"):
                    dict[docId] += (10 * count * idf) / int(self.wordsPerDocument[docId])
                else:
                    dict[docId] += (1 * count * idf) / int(self.wordsPerDocument[docId])
        sorted_lst = [[key,val] for key,val in sorted(dict.items(), key=lambda item: item[1])]
        result = []
        val= min(len(sorted_lst),int(k))
        for i in range(val):
            #result.append(self.titleList[sorted_lst[i][0]].strip("\n"))
            docId = sorted_lst[i][0]
            result.append(str(docId) + "," + self.getTitle(docId))
        return result

        

    def parseFeildQuery(self,text):
        templst = text.split(":")
        lst = []
        for term in templst:
            lst.extend(term.split())
        currfeild = ""
        queryList = []
        for term in lst:
            if len(term) == 1 and term in ['b','r','l','c','i','t']:
                currfeild = term
            else:
                if term not in self.stopWordSet:
                    term = self.ps.stem(term)
                    queryList.append([currfeild,term])
        return queryList
        
    
    def feildQuery(self,query):
        k,text = query.split(",")
        queryList =  self.parseFeildQuery(text)
        dict = defaultdict(int)
        for entry in queryList:
            postingList = self.getPostingOfWord(entry[1])
            if not postingList:
                continue
            word_idf = self.documentCount / len(postingList)
            idf = math.log(word_idf)
            for posting in postingList:
                lst = posting.split(",")
                docId = int(lst[0])
                count = int(lst[1])
                if int(self.wordsPerDocument[docId]) == 0:
                    continue
                if(lst[2] == "i"):
                    dict[docId] += (4 * count * idf) / int(self.wordsPerDocument[docId])
                elif(lst[2] == "t"):
                    dict[docId] += (10 * count * idf) / int(self.wordsPerDocument[docId])
                else:
                    dict[docId] += (1 * count * idf) / int(self.wordsPerDocument[docId])
        sorted_lst = [[key,val] for key,val in sorted(dict.items(), key=lambda item: item[1])]
        result = []
        print(len(sorted_lst),int(k))
        val= min(len(sorted_lst),int(k))
        for i in range(val):
            docId = sorted_lst[i][0]
            result.append(str(docId) + "," + self.getTitle(docId))
        return result
        

s = searchQueries("IndexDir/")
lst = s.search(sys.argv[1])
with open("queries_op.txt","w") as file:
    for entries in lst:
        for entry in entries:
            file.write(str(entry))
            file.write("\n")
        file.write("\n\n")
