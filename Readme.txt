Index Creation:
-----------------------

Index Creation is done in 4 modules:
	0.main.py
        1.xmlParser.py
        2.PreProcess.py
        3.BuildBlockDict.py
        4.KWayMerge.py	
    
    In xmlParser data is parsed from xml file and parsed document by document.

    In PreProcess data cleaning,stopword removal,stemming of words is done.Here we alos store 
        titles of each document parsed in separate file.For this titles file we also 
        maintain offset file where we store offset for every 2048 document.

    In BuildBlockDict store sorted files of certain size in memory.we later use these files 
        for creatingour final inverted index using k-way merge.

    In KWayMerge we merge all the files into inverted index of certain size.here we distribute
        inverted index into multiple files.Here we also create offset file for inverted index. 
        We store one offset for every 1024 word entries.


Searching:
--------------
search.py for searching either feild queries or normal text queries.
