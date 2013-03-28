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

    RARE_NUMERIC = "_RARE_NUMERIC_";
    RARE_ALL_NUMERIC = "_RARE_ALL_NUMERIC_";
    RARE_ALL_NON_ALFANUMERIC = "_RARE_ALL_NON_ALFANUMERIC_";
    RARE_ALL_CAP = "_RARE_ALL_CAP_";
    RARE_LAST_CAP = "_RARE_LAST_CAP_";
    RARE_FIRST_CAP = "_RARE_FIRST_CAP_";
    
    @staticmethod
    def WordNormalize(word):
        #word = word.lower();
        return word;

    @staticmethod
    def getRareWordClass(word):
        rex_number = re.compile(r'\d'); # at least one numeric
        rex_all_number = re.compile(r'^\s*(\d+)\s*$'); # all numeric
        rex_all_non_alfanumeric = re.compile(r'[^A-Za-z\d]'); # at least one non alfanumeric
        rex_all_cap = re.compile(r'^\s*([A-Z]+)\s*$'); # all capital
        rex_last_cap = re.compile(r'^\s*.+[A-Z]\s*$'); # at least some non-capital, but last is capital
        rex_first_cap = re.compile(r'^\s*[A-Z].+\s*$'); # at least some non-capital, but first is capital
        #r'\b\S*[a-z]\S*[A-Z]\b'

        rareWordClass = TaggingPreprocessing.RARE_WORD;
        if(rex_all_number.search(word)):
            print ("find all numeric word: %s" % (word));
            rareWordClass = TaggingPreprocessing.RARE_ALL_NUMERIC;
        elif(rex_number.search(word)):
            #print ("find numeric word: %s" % (word));
            rareWordClass = TaggingPreprocessing.RARE_NUMERIC;
        elif(rex_all_non_alfanumeric.search(word)):
            print ("find non alfanumeric word: %s" % (word));
            rareWordClass = TaggingPreprocessing.RARE_ALL_NON_ALFANUMERIC;
        elif(rex_all_cap.search(word)):
            #print ("find All Cap word: %s" % (word));
            rareWordClass = TaggingPreprocessing.RARE_ALL_CAP;
        elif(rex_last_cap.search(word)):
            #print ("find Last Cap word: %s" % (word));
            rareWordClass = TaggingPreprocessing.RARE_LAST_CAP;
        elif(rex_first_cap.search(word)):
            #print ("find First Cap word: %s" % (word));
            rareWordClass = TaggingPreprocessing.RARE_FIRST_CAP;
        else:
            #print ("findRareWords word: %s" % (word));
            rareWordClass = TaggingPreprocessing.RARE_WORD;
        return rareWordClass;

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

        self.wordsCount = defaultTree();
        self.wordsRaw = [];
        self.tagsRaw = [];
        self.wordsRare = defaultTree();

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
                var_word = match.group(1);
                var_tag = match.group(2);

                #preprocessing word
                var_word = TaggingPreprocessing.WordNormalize(var_word);
                
                self.wordsRaw.append(var_word);
                self.tagsRaw.append(var_tag);

                if(not self.wordsCount.has_key(var_word)):
                    self.wordsCount[var_word] = 0;
                self.wordsCount[var_word] = self.wordsCount[var_word] + 1;
                if(lineNo < 100):
                    print ("Word tag: word: %s, tag: %s, count: %d" % (var_word, var_tag, self.wordsCount[var_word]));
            else:
                self.wordsRaw.append("");
                self.tagsRaw.append("");
        print("Preprocessing reading finished ...");
        
    def findRareWordsClasses(self, withClassess):
        print("Finding rare words started ...");

        wordNo = 0;
        #for count, word in enumerate(self.wordsCount):
        for word, count in self.wordsCount.items():
            #print "findRareWords word:" + word + ", count:" + str(count)
            
            if(count<TaggingPreprocessing.RARE_COUNT):
                if(wordNo<50): print ("word: %s, count: %d" % (word, count));
                if(not withClassess):
                    self.wordsRare[word] = TaggingPreprocessing.RARE_WORD;
                else:
                    self.wordsRare[word] = TaggingPreprocessing.getRareWordClass(word);
            wordNo = wordNo + 1;
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


    def saveViterbi(self, filenameOut, withClassess):
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
                if(not withClassess):
                    word_final = self.wordsRare[word];
                else:
                    word_final = self.getRareWordClass(word);

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