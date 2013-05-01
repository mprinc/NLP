import sys
import codecs

from collections import defaultdict

def defaultTree():
    return defaultdict(defaultTree);

class FilesManagement(object):
    WORD_NULL = "NULL"
    @staticmethod
    def WordNormalize(word):
        #word = word.lower();
        return word;

    def __init__(self):
        self.filenameIn = "";
        self.filenameOut = "";
        self.sentences = [];
        self.sentencesNulled = [];

        self.wordsCount = defaultTree();

    def load(self, filenameIn):
        self.filenameIn = filenameIn
        print("Preprocessing reading started ...");

        self.sentences = [];
        self.wordsCount = defaultTree();

        try:
            self.file = codecs.open(self.filenameIn, encoding="utf-8", mode="r")
            # or
            #     self.file = open(self.filenameIn, "r")
            # but then we need to decode read data with
            # print ("Sentence: %s" % (line.decode('string_escape')));
            # while with
            #    self.file = codecs.open(self.filenameIn, encoding="utf-8", mode="r")
            # we have to decode with:
            # print ("Sentence: %s" % (line.decode('unicode_escape')));
            # http://docs.python.org/2/howto/unicode.html
            # http://stackoverflow.com/questions/147741/character-reading-from-file-in-python
            # http://www.evanjones.ca/python-utf8.html
            # http://dryice.name/blog/python/reading-utf-8-file-in-python/
            # http://stackoverflow.com/questions/934160/write-to-utf-8-file-in-python
            # http://stackoverflow.com/questions/491921/unicode-utf8-reading-and-writing-to-files-in-python
                            

        except Exception:
            print "[BukvikParser:parseFile]: problem opening file filenameIn = ", self.filenameIn
            sys.exit(1)
            
        lineNo = 0
        # http://docs.python.org/2/library/re.html
        
        for line in self.file:
            lineNo=lineNo+1;
            
            sentenceList = [x.strip() for x in line.split()];
            self.sentences.append(sentenceList);
            sentenceListNulled = sentenceList[:];
            sentenceListNulled.insert(0, FilesManagement.WORD_NULL);
            self.sentencesNulled.append(sentenceListNulled);

            if(lineNo < 5):
                print ("Sentence (%d words): %s" % (len(sentenceList), str(sentenceList).decode('unicode_escape')));

            for word in sentenceList:
                if(not self.wordsCount.has_key(word)):
                    self.wordsCount[word] = 0;
                self.wordsCount[word] += 1;
                
        for word, count in self.wordsCount.items()[0:5]:
            print "wordsCount: word:" + word + ", count:" + str(count)
            

        print("Preprocessing reading finished ...");