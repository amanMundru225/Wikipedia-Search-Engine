import xml.sax
import PreProcess
import BuildBlockDict

import os

class MyHandler(xml.sax.ContentHandler):
    def __init__(self,indexPath,indexStatsPath):
        xml.sax.ContentHandler.__init__(self)
        self.indexPath = indexPath
        self.indexStatsPath = indexStatsPath
        if not os.path.exists(indexPath):
            os.mkdir(indexPath)
        self.writeTitle = False
        self.writeId = False
        self.writeText = False
        self.insideRevision = False
        self.documentCount = 0
        self.blockCount = 0
        self.preProcess = PreProcess.Preprocess()
        self.totalWords = 0
        self.buildDict = BuildBlockDict.BuildBlockDict(self.indexPath)
        self.resetValues()
     
    def startElement(self, name, attrs):
        if name == "id":
            self.writeId = True
        elif name == "title":
            self.writeTitle = True
        elif name == "text":
            self.writeText = True
        elif name == "revision":
            self.insideRevision = True
    
    def endElement(self, name):
        if name == "id":
            self.writeId = False
        elif name == "title":
            self.writeTitle = False
            self.titleList = self.preProcess.parseTitle(self.title)
        elif name == "text":
            self.writeText = False
            self.textLists = self.preProcess.processText(self.text)
        elif name == "revision":
            self.insideRevision = False
        elif name == "page":
            self.documentCount += 1
            pageList = [self.id,self.titleList]
            pageList.append(self.textLists)
            self.buildDict.addPageToDict(pageList)
            self.resetValues()


    def resetValues(self):
        self.id = ""
        self.title = ""
        self.text = ""
    
    def characters(self, data):
        if self.writeId == True and self.insideRevision == False:
            self.id += data
        elif self.writeTitle == True:
            self.title += " " + data
        elif self.writeText == True:
            self.text += " " + data
    

    def endDocument(self):
        # writing final block to disk
        self.totalWords = self.preProcess.getTotalWordCount()
        self.blockCount = self.buildDict.writeBlockToFile()
        self.preProcess.finishingTouches()