import re
import string
from threading import Thread
from nltk.stem import PorterStemmer


class Preprocess():

    def __init__(self):
        punctuations = string.punctuation
        self.table = punctuations.maketrans(punctuations+string.digits+string.ascii_uppercase," "*(len(punctuations) + 10)+string.ascii_lowercase,)
        self.formStopWordSet()
        self.ps = PorterStemmer()
        
        self.titleWriteBlockSize = 2048
        self.titleList = []
        self.wordsPerdocument = []
        self.documentCount = 0
        self.totalWordCount = 0

    def formStopWordSet(self):
        self.stopwordSet = set()
        with open('stopwords.txt','r') as file: 
            for line in file:     
                for word in line.split():           
                    self.stopwordSet.add(word)
        return 
        
    def getTotalWordCount(self):
        return self.totalWordCount

    def processText(self,text):
        self.cleanText = text.translate(self.table)
        listsOfEachTypeWords = self.parseText(text)
        lsts = self.doStoppingStemming(listsOfEachTypeWords)
        lsts.append(self.infoBox(text))
        numOfWords = self.titleLength
        for lst in lsts:
            numOfWords += len(lst)
        self.wordsPerdocument.append(numOfWords)
        return lsts
            
        
    def finishingTouches(self):
        file = open("wordsPerDocument.txt","a+")
        for entry in self.wordsPerdocument:
            file.write(str(entry) + ",")
        self.wordsPerDocument  = []
        file.close()
        self.writeBlockToFile()
        self.titleList = []
        


    def parseTitle(self,title):
        self.documentCount += 1
        self.titleList.append(title)
        if len(self.titleList) == self.titleWriteBlockSize:
            self.writeBlockToFile()
            self.titleList = []
        self.titleText = title.translate(self.table).split()
        self.titleLength = len(self.titleText)
        return [self.ps.stem(word) for word in self.titleText if word not in self.stopwordSet]


    def writeBlockToFile(self):
        titleFile = open("titles.txt","a+")
        seekTitleFile = open("seekTitleFile.txt","a+")
        seekPos = titleFile.tell()
        seekTitleFile.write(str(self.documentCount) + ":" + str(seekPos))
        seekTitleFile.write("\n")
        for entry in self.titleList:
            titleFile.write(entry)
            titleFile.write("\n")
        titleFile.close()
        seekTitleFile.close()

    def getSectionIndices(self,text):
        lst = [i.start() for i in re.finditer("==", text)]
        sectionStartIdxs = []
        sectionStartIdxs.append(0)
        sectionStartIdxs.extend([lst[i] for i in range(len(lst)) if i % 2 == 0])
        # appending Category starting indices if category present  else end of text
        CategoryIdx = text.find("[[Category:",sectionStartIdxs[-1])
        if CategoryIdx != -1:
            sectionStartIdxs.append(CategoryIdx)
            CategoryFlag = True
        else:
            CategoryFlag = False
            sectionStartIdxs.append(len(text) - 1)

        return sectionStartIdxs,CategoryFlag

    
    def parseText(self,text):
        idxArray = [0,-1,-1,-1,len(text)-1]
        sectionStartIdxs,categoryFlag = self.getSectionIndices(text)
        for i in range(1,len(sectionStartIdxs)):
            startIdx = sectionStartIdxs[i-1]
            cleanSectionStartText = self.cleanText[startIdx:startIdx + 30].strip()
            if cleanSectionStartText[:10] == "references":
                idxArray[1] = sectionStartIdxs[i-1]
            elif cleanSectionStartText[0:8] == "external":
                idxArray[2] = sectionStartIdxs[i-1]
        if categoryFlag:
            idxArray[3] = sectionStartIdxs[-1]
        return self.listOfEachType(idxArray)
        
    
    def listOfEachType(self,idxArray):
        i = len(idxArray) - 2
        while i > 0:
            if idxArray[i] == -1:
                idxArray[i] = idxArray[i+1]
            i = i - 1
        listsOfEachTypeWords =[]
        for i in range(1,len(idxArray)):
            splitList = self.cleanText[idxArray[i-1]:idxArray[i]].split()
            self.totalWordCount += len(splitList)
            listsOfEachTypeWords.append(splitList)
        return listsOfEachTypeWords
        
        
    
    def doStoppingStemming(self,wordsLists):
        lst = []
        for wordList in wordsLists:
            stoppedStemmedList = [self.ps.stem(word) for word in wordList if word not in self.stopwordSet]
            lst.append(stoppedStemmedList)
        return lst

    def infoBox(self,text):
        startPos = text.find("{{Infobox",0,1000)
        lst = []
        if startPos != -1:
            endPos = text.find("}}",startPos)
            lst = self.cleanText[startPos:endPos].split()
            lst = [self.ps.stem(word) for word in lst if word not in self.stopwordSet]
            
        return lst


        




    

            

            

        







        



            