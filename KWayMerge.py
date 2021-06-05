import heapq
import ast

class KWayMerge():
    
    def __init__(self,fileCount,indexPath):
        self.indexPath = indexPath
        self.fileCount = fileCount
        self.inMemFileSize = 1000
        self.outputBlockSize = 1024
        self.blocksPerFile = 2048
        self.currBlockCount = 0
        self.currFileNumber = 1
        self.prevOutputWord = ""
        self.prevOutWordValue = ""
        self.totalWordCount = 0
        self.seekFile = open( "InMemoryIndex.txt","w")


    def getFilePointers(self):
        lst = []
        for i in range(1,self.fileCount+1):
            fileName = self.indexPath + "block" + str(i)+".txt"
            lst.append(open(fileName,"r"))
        return lst

    def readDataFromFile(self,fileIndex):
        lst = []
        i = 0
        while i < self.inMemFileSize:
            line = self.listOfFilePointers[fileIndex].readline()
            if line:
                word,string = line.split("$")
                lst.append([word,string])
            else:
                break   
            i = i + 1
        return lst

    def writeDataToOutputfile(self,outData):
        self.currBlockCount += 1
        if(self.currBlockCount == self.blocksPerFile):
            self.currBlockCount = 0
            self.currFileNumber += 1
            self.outputFilePointer.close()
            self.outputFilePointer = open(self.indexPath + "Index_" + str(self.currFileNumber)+ ".txt" ,"w")

        self.addEntryToSeekFile()
        for entry in outData:
            if self.prevOutputWord == entry[0]:
                self.prevOutWordValue = self.prevOutWordValue.rstrip("\n")+entry[1]
            else:
                self.totalWordCount += 1
                self.outputFilePointer.write(self.prevOutputWord + "$" + self.prevOutWordValue.rstrip("\n"))
                self.outputFilePointer.write("\n")
                self.prevOutWordValue = ""
                self.prevOutputWord = entry[0]
                self.prevOutWordValue = entry[1]
        
    
    def closeFiles(self):
        print("closing files")
        for ptr in self.listOfFilePointers:
            ptr.close()
        self.totalWordCount += 1
        self.outputFilePointer.write(self.prevOutputWord + "$" + self.prevOutWordValue)
        self.outputFilePointer.write("\n")
        self.outputFilePointer.close()
        self.seekFile.close()

    
    def getTotalUniqueWordCount(self):
        return self.totalWordCount

    
    def addEntryToSeekFile(self):
        seekPos = self.outputFilePointer.tell()
        word = self.prevOutputWord
        entry = str(word) + ":" + str(seekPos) + "_" + str(self.currFileNumber)
        self.seekFile.write(entry)
        self.seekFile.write("\n")

    
    def mergeFiles(self):
        self.listOfFilePointers = self.getFilePointers()
        self.outputFilePointer = open(self.indexPath + "Index_" + str(self.currFileNumber)+ ".txt" ,"w")

        outList = []
        # reading data from files
        listOfFileLists = []
        filesCurrentPos = []
        for i in range(self.fileCount):
            listOfFileLists.append(self.readDataFromFile(i))
            filesCurrentPos.append(0)
        
        #create heap with heapData in format (word,fileNumber)
        heapList = []
        for i in range(self.fileCount):
            word = listOfFileLists[i][0][0]
            heapList.append((word,i))
        heapq.heapify(heapList)

        #now begin merging
        while heapList:
            minElement = heapq.heappop(heapList)
            fileNumber  = minElement[1]
            outList.append(listOfFileLists[fileNumber][filesCurrentPos[fileNumber]])
            if filesCurrentPos[fileNumber] == len(listOfFileLists[fileNumber]):
                pass
            else:
                filesCurrentPos[fileNumber] += 1
            # if reached end of fileNumber list read data
                if filesCurrentPos[fileNumber] == len(listOfFileLists[fileNumber]):
                    tempList = self.readDataFromFile(fileNumber)
                    if tempList:
                        listOfFileLists[fileNumber] = tempList
                        filesCurrentPos[fileNumber] = 0
                
                # if no updation of filecurrentPos once it reaches end of list implies file reached end
                if filesCurrentPos[fileNumber] == len(listOfFileLists[fileNumber]):
                    pass
                else:
                    word = listOfFileLists[fileNumber][filesCurrentPos[fileNumber]][0]
                    heapq.heappush(heapList,(word,fileNumber))
            
            if len(outList) == self.outputBlockSize:
                self.writeDataToOutputfile(outList)
                outList = []

        self.writeDataToOutputfile(outList)
        self.closeFiles()