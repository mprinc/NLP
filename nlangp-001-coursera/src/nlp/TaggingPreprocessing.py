import sys
import re

from collections import defaultdict
from TaggingCountsUnigram import TaggingCountsUnigram
from TaggingCountsViterbi import TaggingCountsViterbi
from nlp.TaggingCountsViterbi import TaggingCountsViterbi

def defaultTree():
    return defaultdict(defaultTree);

class TaggingPreprocessing(object):
    RARE_WORD = "_RARE_";
    RARE_COUNT = 5;
    
    @staticmethod
    def WordNormalize(word):
        word = word.lower();
        return word;

    def __init__(self):
        self.filenameIn = "";
        self.filenameOut = "";
        self.wordsCount = defaultTree();
        self.wordsRaw = [];
        self.tagsRaw = [];
        self.wordsRare = defaultTree();

    def load(self, filenameIn):
        self.filenameIn = filenameIn
        print("Preprocessing reading started ...");
        try:
            self.file = open(self.filenameIn)
        except Exception:
            print "[BukvikParser:parseFile]: problem opening file filenameIn = ", self.filenameIn
            sys.exit(1)
            
        lineNo = 0
        # http://docs.python.org/2/library/re.html
        rex_word_tag = re.compile(r'^\s*(\S+)\s+(\S*)\s*$') # word tag
        
        for line in self.file:
            lineNo=lineNo+1;

            match = rex_word_tag.search(line)
            if match:
                var_word = match.group(1)
                var_tag = match.group(2)

                #preprocessing word
                var_word = TaggingPreprocessing.WordNormalize(var_word);
                
                self.wordsRaw.append(var_word);
                self.tagsRaw.append(var_tag);

                if(not self.wordsCount.has_key(var_word)):
                    self.wordsCount[var_word] = 0;
                self.wordsCount[var_word] = self.wordsCount[var_word] + 1;
                if(lineNo < 20):
                    print "Word tag: word: " + var_word + ", tag: " + var_tag + ", count: " + str(self.wordsCount[var_word]);
                continue
            else:
                self.wordsRaw.append("");
                self.tagsRaw.append("");
        print("Preprocessing reading finished ...");
        
    def findRareWords(self):
        print("Finding rare words started ...");
        for count, word in enumerate(self.wordsCount):
            #print "findRareWords word:" + word + ", count:" + str(count)
            if(count<TaggingPreprocessing.RARE_COUNT):
                #print "findRareWords word:" + word + ", count:" + str(count)
                self.wordsRare[word] = True;
        print("Finding rare words finished ...");
                
    def findRareWordsClasses(self):
        print("Finding rare words started ...");
        for count, word in enumerate(self.wordsCount):
            #print "findRareWords word:" + word + ", count:" + str(count)
            if(count<TaggingPreprocessing.RARE_COUNT):
                #print "findRareWords word:" + word + ", count:" + str(count)
                self.wordsRare[word] = True;
        print("Finding rare words finished ...");
                
    def saveUnigram(self, filenameOut):
        self.filenameOut = filenameOut
        print("Preprocessing saving started ...");
        try:
            self.file = open(self.filenameOut, "w")
        except Exception:
            print "[BukvikParser:parseFile]: problem opening file filenameIn = ", self.filenameIn
            sys.exit(1)
            
        wordNo = 0
        while wordNo < len(self.wordsRaw):
            word = self.wordsRaw[wordNo];
            if(self.wordsRare.has_key(word)):
                self.file.write(TaggingPreprocessing.RARE_WORD);
            else:
                self.file.write(word);
            self.file.write(" " + self.tagsRaw[wordNo] + "\n");
            wordNo = wordNo+1;
        self.file.close();
        print("Preprocessing saving finished ...");

    def saveViterbi(self, filenameOut):
        self.filenameOut = filenameOut
        print("Preprocessing saving started ...");
        try:
            self.file = open(self.filenameOut, "w")
        except Exception:
            print "[BukvikParser:parseFile]: problem opening file filenameIn = ", self.filenameIn
            sys.exit(1)
        wordNo = 0
        #newSentence = True;
        #previousWord = "";
        while wordNo < len(self.wordsRaw):
            # We do not need to preprocess sentences since count_freqs script is doing it for us in this case
            #if(newSentence):
                #self.file.write(TaggingCountsViterbi.WORD_START + " " + TaggingCountsViterbi.TAG_START + "\n");
                #self.file.write(TaggingCountsViterbi.WORD_START + " " + TaggingCountsViterbi.TAG_START + "\n");
                #newSentence = False;

            word = self.wordsRaw[wordNo];
            word_final = word;
            if(self.wordsRare.has_key(word)):
                word_final = TaggingPreprocessing.RARE_WORD;

            tag_final = self.tagsRaw[wordNo];
            # We do not need to preprocess sentences since count_freqs script is doing it for us in this case
            #if(previousWord == TaggingCountsViterbi.WORD_STOP_CHECK and word == ''):
                #self.file.write(TaggingCountsViterbi.WORD_STOP + " " + TaggingCountsViterbi.TAG_STOP);
                #self.file.write("\n");
                #newSentence = True;
            #else:
            self.file.write(word_final + " " + tag_final + "\n");
            #previousWord = word;
            wordNo = wordNo+1;
        self.file.close();
        print("Preprocessing saving finished ...");

    def saveViterbiClasses(self, filenameOut):
        self.filenameOut = filenameOut
        print("Preprocessing saving started ...");
        try:
            self.file = open(self.filenameOut, "w")
        except Exception:
            print "[BukvikParser:parseFile]: problem opening file filenameIn = ", self.filenameIn
            sys.exit(1)
        wordNo = 0
        #newSentence = True;
        #previousWord = "";
        while wordNo < len(self.wordsRaw):
            # We do not need to preprocess sentences since count_freqs script is doing it for us in this case
            #if(newSentence):
                #self.file.write(TaggingCountsViterbi.WORD_START + " " + TaggingCountsViterbi.TAG_START + "\n");
                #self.file.write(TaggingCountsViterbi.WORD_START + " " + TaggingCountsViterbi.TAG_START + "\n");
                #newSentence = False;

            word = self.wordsRaw[wordNo];
            word_final = word;
            if(self.wordsRare.has_key(word)):
                word_final = TaggingPreprocessing.RARE_WORD;

            tag_final = self.tagsRaw[wordNo];
            # We do not need to preprocess sentences since count_freqs script is doing it for us in this case
            #if(previousWord == TaggingCountsViterbi.WORD_STOP_CHECK and word == ''):
                #self.file.write(TaggingCountsViterbi.WORD_STOP + " " + TaggingCountsViterbi.TAG_STOP);
                #self.file.write("\n");
                #newSentence = True;
            #else:
            self.file.write(word_final + " " + tag_final + "\n");
            #previousWord = word;
            wordNo = wordNo+1;
        self.file.close();
        print("Preprocessing saving finished ...");