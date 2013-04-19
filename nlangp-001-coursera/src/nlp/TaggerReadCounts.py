# Necessary to avoid rounding on integer numbers
from __future__ import division

import sys
import re

from TaggingCountsUnigram import TaggingCountsUnigram
from TaggingPreprocessing import TaggingPreprocessing

class TaggerReadCounts(object):
    def __init__(self):
        self.filenameIn = "";
        self.taggingCountsUnigram = TaggingCountsUnigram();

    def load(self, filenameIn, taggingCountsUnigram):
        self.filenameIn = filenameIn
        self.taggingCountsUnigram = taggingCountsUnigram
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
                #    print "Emission: count:" + var_count + ", tagUnigram: " + var_tag + ", word: " + var_word
                self.taggingCountsUnigram.wordTagCount[var_word][var_tag] = int(var_count);
                self.taggingCountsUnigram.wordsHash[var_word] = True;
                self.taggingCountsUnigram.tagssHash[var_tag] = True;
                continue

            match = rex_unigram.search(line)
            if match:
                var_count = match.group(1)
                var_tag_1 = match.group(2)
                #print "Unigram: count:" + var_count + ", tag_1: " + var_tag_1
                self.taggingCountsUnigram.nonterminalsCount[var_tag_1] = int(var_count);
                continue

            match = rex_bigram.search(line)
            if match:
                var_count = match.group(1)
                var_tag_1 = match.group(2)
                var_tag_2 = match.group(3)
                #print "Bigram: count:" + var_count + ", tag_1: " + var_tag_1 + ", tag_2: " + var_tag_2
                self.taggingCountsUnigram.bigramsCount[var_tag_1][var_tag_2] = int(var_count);
                continue

            match = rex_trigram.search(line)
            if match:
                var_count = match.group(1);
                var_tag_1 = match.group(2);
                var_tag_2 = match.group(3);
                var_tag_3 = match.group(4);
                #print "Trigram: count:" + var_count + ", tag_1: " + var_tag_1 + ", tag_2: " + var_tag_2 + ", tag_3: " + var_tag_3;
                self.taggingCountsUnigram.binaryRulesCount[var_tag_1][var_tag_2][var_tag_3] = int(var_count);
                continue

            if not match:
                #print str(lineNo)+":"+line
                continue

        self.taggingCountsUnigram.tags = self.taggingCountsUnigram.tagssHash.keys();
        self.taggingCountsUnigram.words = self.taggingCountsUnigram.wordsHash.keys();
        print "Tags: " + str(self.taggingCountsUnigram.tags);
        print "Search trigram['O']['O']['I-GENE']: " + str(self.taggingCountsUnigram.binaryRulesCount['O']['O']['I-GENE']);

    