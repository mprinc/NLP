# Necessary to avoid rounding on integer numbers
from __future__ import division

import sys
import re

from TaggingCountsUnigram import TaggingCountsUnigram
from TaggingPreprocessing import TaggingPreprocessing

class TaggerUnigram(object):
    def __init__(self):
        self.filenameIn = "";
        self.taggingCountsUnigram = TaggingCountsUnigram();

    def getEmissionParameters(self, taggingCountsUnigram):
        self.taggingCountsUnigram = taggingCountsUnigram
        print "Calculating Emissions parameters for unigram tagger started ..."
        for word in self.taggingCountsUnigram.words:
            emissionMax = 0;
            for tag in self.taggingCountsUnigram.wordTagCount[word].keys():
                if(len(self.taggingCountsUnigram.wordTagCount[word].keys()) > 1):
                    print "word/tagUnigram: " + word + "/" + tag;
                    print "getEmissionParametersUnigram: " + str(self.taggingCountsUnigram.wordTagCount[word][tag]) + ", " + str(self.taggingCountsUnigram.nonterminalsCount[tag]);
                self.taggingCountsUnigram.emissionCount[word][tag] = self.taggingCountsUnigram.wordTagCount[word][tag] / self.taggingCountsUnigram.nonterminalsCount[tag];
                if(emissionMax < self.taggingCountsUnigram.emissionCount[word][tag]):
                    self.taggingCountsUnigram.emissionCountMax[word] = tag;
                    emissionMax = self.taggingCountsUnigram.emissionCount[word][tag];
                    #if(len(self.taggingCountsUnigram.wordTagCount[word].keys()) > 1):
                    #    print "...This is max";
                #print "getEmissionParametersUnigram: " + str(self.taggingCountsUnigram.wordTagCount[word][tagUnigram] / self.taggingCountsUnigram.nonterminalsCount[tagUnigram]);
        print "Calculating Emissions parameters for unigram tagger finished ..."
    
    def tag(self, filenameIn, filenameOut):
        self.filenameIn = filenameIn
        self.filenameOut = filenameOut
        print "Tagging Unigram started ..."

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

                if(not self.taggingCountsUnigram.wordsHash.has_key(word_final)):
                    #print "Word " + word_orig + " -> " + TaggingPreprocessing.RARE;
                    word_final = TaggingPreprocessing.RARE_WORD;
                tag = self.taggingCountsUnigram.emissionCountMax[word_final];
                self.fileOut.write(word_orig + " " + tag + "\n");
            else:
                self.fileOut.write(line);

        self.fileIn.close();
        self.fileOut.close();

        print "Tagging Unigram finished ..."
