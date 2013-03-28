# Necessary to avoid rounding on integer numbers
from __future__ import division

import sys
import re

from TaggingCountsUnigram import TaggingCountsUnigram
from TaggingCountsViterbi import TaggingCountsViterbi
from TaggingPreprocessing import TaggingPreprocessing

class TaggerViterbi(object):
    def __init__(self):
        self.filenameIn = "";
        self.taggingCountsUnigram = TaggingCountsUnigram();
        self.taggingCountsViterbi = TaggingCountsViterbi(self.taggingCountsUnigram);

    def getEmissionParameters(self, taggingCountsUnigram, taggingCountsViterbi):
        self.taggingCountsUnigram = taggingCountsUnigram
        self.taggingCountsViterbi = taggingCountsViterbi

        print "Calculating Emissions parameters for unigram tagger started ..."
        for (tag1, dict1) in self.taggingCountsUnigram.bigramsCount.items():
            for (tag2, countBigram) in dict1.items():
                for tag3 in self.taggingCountsUnigram.tags:
                    countTrigram = self.taggingCountsUnigram.getTrigramCountOr0(tag1, tag2, tag3);
                    self.taggingCountsViterbi.mleTrigram[tag1][tag2][tag3] = countTrigram / countBigram;
        # count TaggingCountsViterbi.TAG_START MLEs
        
        print "Calculating Emissions parameters for unigram tagger finished ..."
    
    def tag(self, filenameIn, filenameOut, withClassess):
        self.filenameIn = filenameIn
        self.filenameOut = filenameOut
        print "Tagging with Viterbi Algoirithm started ..."

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
            
        wordsNo = 0
        
        rex_word = re.compile(r'^\s*(\S+)\s*$') # <word_orig>
        newSentence = True;
        for line in self.fileIn:
            wordsNo=wordsNo+1;
        
            if(newSentence):
                self.taggingCountsViterbi.initSentence();
                k = 1;
                newSentence = False;
                self.taggingCountsViterbi.sentence_words_original = ['']; # we want that index star at 1 not 0
                self.taggingCountsViterbi.sentence_words_final = [''];
                self.taggingCountsViterbi.sentence_tags = [''];

            match = rex_word.search(line);
            isLastWordInSentence = False;
            if match:
                word_orig = match.group(1);
                word_final = TaggingPreprocessing.WordNormalize(word_orig);
                if(not self.taggingCountsUnigram.wordsHash.has_key(word_final)):
                    #print "Word " + word_orig + " -> " + TaggingPreprocessing.RARE;
                    if(not withClassess):
                        word_final = TaggingPreprocessing.RARE_WORD;
                    else:
                        word_final = TaggingPreprocessing.getRareWordClass(word_final);
            else:
                word_orig = line;
                if(word_orig.rstrip("\r\n") != ""):
                    print("not empty line");
                    exit(1);
                word_final = TaggingCountsViterbi.WORD_STOP_CHECK;
                isLastWordInSentence = True;

            # calculating PI values
            # https://docs.google.com/document/d/1fjKQpeQeU_3pvdYFZcL8XcNqvAjZ3nxroicIxlTpa5E/edit
            tagSet_k_2 = self.taggingCountsViterbi.getTagSet(k-2, False);
            tagSet_k_1 = self.taggingCountsViterbi.getTagSet(k-1, False);
            tagSet_k = self.taggingCountsViterbi.getTagSet(k, isLastWordInSentence);
            self.taggingCountsViterbi.sentence_words_original.append(word_orig);
            self.taggingCountsViterbi.sentence_words_final.append(word_final);
            for tag_k_1 in tagSet_k_1:
                for tag_k in tagSet_k:
                    self.taggingCountsViterbi.sentence_pi[k][tag_k_1][tag_k] = 0;
                    for tag_k_2 in tagSet_k_2:
                        pi = self.taggingCountsViterbi.getPiOr0(k-1, tag_k_2, tag_k_1) \
                        * self.taggingCountsViterbi.getMLETrigramOr0(tag_k_2, tag_k_1, tag_k) \
                        * self.taggingCountsUnigram.getEmissionCountOr0(word_final, tag_k);
                        if(pi>self.taggingCountsViterbi.sentence_pi[k][tag_k_1][tag_k]):
                            self.taggingCountsViterbi.sentence_pi[k][tag_k_1][tag_k] = pi;

            if(isLastWordInSentence):
                n = k-1;
                # calculating tags
                # index is starting at 0 so we need one more element
                self.taggingCountsViterbi.sentence_tags = [None]*((n+1)+1);
                self.taggingCountsViterbi.sentence_tags[(n+1)] = TaggingCountsViterbi.TAG_STOP;
                # n+1 because we want to start with STOP tag at position (n+1) that is already defined
                for k in range(n+1, 1-1, -1): # n+1..1 (bec end point in range() is omited!
                    # iterate through all possible tags and see which one has the highest probability
                    piMax = 0;
                    tag_k = self.taggingCountsViterbi.sentence_tags[k];
                    for tag_k_1 in self.taggingCountsViterbi.sentence_pi[k].keys():
                        if(self.taggingCountsViterbi.sentence_pi[k][tag_k_1][tag_k] >= piMax):
                            piMax = self.taggingCountsViterbi.sentence_pi[k][tag_k_1][tag_k];                        
                            self.taggingCountsViterbi.sentence_tags[k-1] = tag_k_1;
                newSentence = True;
                
                #printing out words with tags
                for k in range(1, (n)+1): # 1..n (bec end point in range() is omited!
                    word_orig = self.taggingCountsViterbi.sentence_words_original[k];
                    tag = self.taggingCountsViterbi.sentence_tags[k];
                    self.fileOut.write(word_orig + " " + tag + "\n");
                self.fileOut.write("\n");
            else:
                k=k+1;

        self.fileIn.close();
        self.fileOut.close();

        print "Tagging with Viterbi Algoirithm finished ..."
