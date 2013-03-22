# Necessary to avoid rounding on integer numbers
from __future__ import division

import sys
import re

from TaggingCounts import TaggingCounts
from TaggingPreprocessing import TaggingPreprocessing

class ReadCounts(object):
    def __init__(self):
        self.filenameIn = "";
        self.taggingCounts = TaggingCounts();

    def load(self, filenameIn, taggingCounts):
        self.filenameIn = filenameIn
        self.taggingCounts = taggingCounts
        print("Reading");
        try:
            self.file = open(self.filenameIn)
        except Exception:
            print "[BukvikParser:parseFile]: problem opening file filenameIn = ", self.filenameIn
            sys.exit(1)
            
        lineNo = 0
        # http://docs.python.org/2/library/re.html
        rex_emission = re.compile(r'^\s*(\d+)\s+WORDTAG\s+(\S*)\s+(\S*)\s*$') # 6 WORDTAG O complication
        rex_unigram = re.compile(r'^\s*(\d+)\s+1-GRAM\s+(\S*)\s*$') # 41072 1-GRAM I-GENE
        rex_bigram = re.compile(r'^\s*(\d+)\s+2-GRAM\s+(\S*)\s+(\S*)\s*$') # 24435 2-GRAM I-GENE I-GENE
        rex_trigram = re.compile(r'^\s*(\d+)\s+3-GRAM\s+(\S*)\s+(\S*)\s+(\S*)\s*$') # 3-GRAM O O STOP
        
        for line in self.file:
            lineNo=lineNo+1;

            match = rex_emission.search(line)
            if match:
                var_count = match.group(1)
                var_tag = match.group(2)
                var_word = match.group(3)
                #if(lineNo < 20):
                #    print "Emission: count:" + var_count + ", tag: " + var_tag + ", word: " + var_word
                self.taggingCounts.wordTagCount[var_word][var_tag] = int(var_count);
                self.taggingCounts.wordsHash[var_word] = True;
                self.taggingCounts.tagssHash[var_tag] = True;
                continue

            match = rex_unigram.search(line)
            if match:
                var_count = match.group(1)
                var_tag_1 = match.group(2)
                #print "Unigram: count:" + var_count + ", tag_1: " + var_tag_1
                self.taggingCounts.unigramsCount[var_tag_1] = int(var_count);
                continue

            match = rex_bigram.search(line)
            if match:
                var_count = match.group(1)
                var_tag_1 = match.group(2)
                var_tag_2 = match.group(3)
                #print "Bigram: count:" + var_count + ", tag_1: " + var_tag_1 + ", tag_2: " + var_tag_2
                self.taggingCounts.bigramsCount[var_tag_1][var_tag_2] = int(var_count);
                continue

            match = rex_trigram.search(line)
            if match:
                var_count = match.group(1);
                var_tag_1 = match.group(2);
                var_tag_2 = match.group(3);
                var_tag_3 = match.group(4);
                #print "Trigram: count:" + var_count + ", tag_1: " + var_tag_1 + ", tag_2: " + var_tag_2 + ", tag_3: " + var_tag_3;
                self.taggingCounts.trigramsCount[var_tag_1][var_tag_2][var_tag_3] = int(var_count);
                continue

            if not match:
                #print str(lineNo)+":"+line
                continue

        self.taggingCounts.tags = self.taggingCounts.tagssHash.keys();
        self.taggingCounts.words = self.taggingCounts.wordsHash.keys();
        print "Tags: " + str(self.taggingCounts.tags);
        print "Search trigram['O']['O']['I-GENE']: " + str(self.taggingCounts.trigramsCount['O']['O']['I-GENE']);

    def getEmissionParameters(self, taggingCounts):
        self.taggingCounts = taggingCounts
        print "Calculating Emissions parameters started ..."
        for word in self.taggingCounts.words:
            emissionMax = 0;
            for tag in self.taggingCounts.wordTagCount[word].keys():
                if(len(self.taggingCounts.wordTagCount[word].keys()) > 1):
                    print "word/tag: " + word + "/" + tag;
                    print "getEmissionParameters: " + str(self.taggingCounts.wordTagCount[word][tag]) + ", " + str(self.taggingCounts.unigramsCount[tag]);
                self.taggingCounts.emissionCount[word][tag] = self.taggingCounts.wordTagCount[word][tag] / self.taggingCounts.unigramsCount[tag];
                if(emissionMax < self.taggingCounts.emissionCount[word][tag]):
                    self.taggingCounts.emissionCountMax[word] = tag;
                    emissionMax = self.taggingCounts.emissionCount[word][tag];
                    if(len(self.taggingCounts.wordTagCount[word].keys()) > 1):
                        print "...This is max";
                #print "getEmissionParameters: " + str(self.taggingCounts.wordTagCount[word][tag] / self.taggingCounts.unigramsCount[tag]);
        print "Calculating Emissions parameters finished ..."
    
    def tag(self, filenameIn, filenameOut, taggingCounts):
        self.filenameIn = filenameIn
        self.filenameOut = filenameOut
        print "Tagging started ..."

        try:
            self.fileIn = open(self.filenameIn)
        except Exception:
            print "[BukvikParser:parseFile]: problem opening file filenameIn = ", self.filenameIn
            sys.exit(1)
            
        try:
            self.fileOut = open(self.filenameOut, "w")
        except Exception:
            print "[BukvikParser:parseFile]: problem opening file filenameOut = ", self.filenameOut
            sys.exit(1)
            
        lineNo = 0
        
        rex_word = re.compile(r'^\s*(\S+)$') # <word_orig>
        for line in self.fileIn:
            lineNo=lineNo+1;
        
            match = rex_word.search(line)
            if match:
                word_orig = match.group(1)
                word_final = TaggingPreprocessing.WordNormalize(word_orig);

                if(not self.taggingCounts.wordsHash.has_key(word_final)):
                    #print "Word " + word_orig + " -> " + TaggingPreprocessing.RARE;
                    word_final = TaggingPreprocessing.RARE;
                tag = self.taggingCounts.emissionCountMax[word_final];
                self.fileOut.write(word_orig + " " + tag + "\n");
            else:
                self.fileOut.write(line);

        self.fileIn.close();
        self.fileOut.close();

        print "Tagging finished ..."
    