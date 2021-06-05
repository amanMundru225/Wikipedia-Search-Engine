import xmlParser
import xml.sax
import sys
import KWayMerge
import os

from time import time
def main(wikiDumpPath,indexPath,indexStatsPath):
    handler = xmlParser.MyHandler(indexPath,indexStatsPath)
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)
    ts = time()
    for filename in os.listdir(wikiDumpPath):
        print("parsing",filename)
        parser.parse(wikiDumpPath + filename)

    print("Doing KWay merge")
    merge = KWayMerge.KWayMerge(handler.blockCount,indexPath)
    merge.mergeFiles()
    uniqueWords = merge.getTotalUniqueWordCount()
    with open(indexStatsPath, "w") as f:
        f.write("DocumentCount:" + str(handler.documentCount))
        f.write("\n")
        f.write("total words in corpus:" + str(handler.totalWords))
        f.write("\n")
        f.write("total unique words in corpus" + str(uniqueWords))
    for filename in os.listdir(indexPath):
        if filename.find("block") != -1:
            os.remove(indexPath + filename)
    print(time() - ts)


if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2],sys.argv[3])
