# Necessary to avoid rounding on integer numbers
from __future__ import division

import sys
import codecs
import pickle
import codecs

from collections import defaultdict
from nlp.translation.FilesManagement import FilesManagement
from nlp.translation.TranslatorTContainer import TranslatorTContainer

def defaultTree():
    return defaultdict(defaultTree);

class TranslatorTrainer(object):
    PARAMS_KEY_VALUE_SEPARATOR = "@"
    PARAMS_KEY_1_SEPARATOR_LEFT = "{"
    PARAMS_KEY_1_SEPARATOR_RIGHT = "}"
    @staticmethod
    def WordNormalize(word):
        #word = word.lower();
        return word;

    def __init__(self):
        self.filenameIn = "";
        self.filenameOut = "";
        self.filenameParams = "";
        self.filesManagement1 = FilesManagement();
        self.filesManagement2 = FilesManagement();
        
        # If word1 is a word from the first language, and word2 is a word from the second language then we have the following organization        
        self.t = TranslatorTContainer.defaultTree();    # self.t[word1][word2]
        self.c1 = TranslatorTContainer.defaultTree();   # self.c1[word2]
        self.c2 = TranslatorTContainer.defaultTree();   # self.c2[word2][word1]

        self.wordsCount = defaultTree();

    def trainIBM1(self, filesManagement1, filesManagement2):
        self.filesManagement1 = filesManagement1;
        self.filesManagement2 = filesManagement2;
        self.t = TranslatorTContainer.defaultTree();
        
        print("Training started ...");
        
        self.initializeIBM1();
        for i in xrange(5):
            print("Running %d-th iteration" % (i+1));
            self.iterateIBM1();
            
        print("Preprocessing reading finished ...");
        
    def initializeIBM1(self):
        print("Initialization started ...");
        sentenceNo = 0
        # http://docs.python.org/2/library/re.html
        
        # 1 is added for NULL word
        words2No = len(self.filesManagement2.wordsCount.keys()) + 1;
        print("1/words2No = %e" % (1/words2No));
        for sentenceNo in xrange(len(self.filesManagement1.sentences)):
            sys.stdout.write("\rsentence %d" % (sentenceNo));
            sentence1 = self.filesManagement1.sentences[sentenceNo];
            sentence2 = self.filesManagement2.sentencesNulled[sentenceNo];
            for word1 in sentence1:
                for word2 in sentence2:
                    self.t[word1][word2] = 1/words2No;
        print("");

        # debug
        self.insightParamsT(5, 3)
        print("Initialization finished ...");
        
    def insightParamsT(self, word1Count, word2Count):
        print("Insigt on T params ...");
        for word1, hash2 in self.t.items()[0:word1Count]:
            print("W1: %s" % (word1));
            for word2, tVal in hash2.items()[0:word2Count]:
                print("\t(%s,%s) = %e" % (word1, word2, tVal));
        
    def iterateIBM1(self):
        print("Iteration started ...");
        self.c1 = TranslatorTContainer.defaultTree();
        self.c2 = TranslatorTContainer.defaultTree();
        
        # clear Cs
        print("\tClearing C parameters ...");
        for sentenceNo in xrange(len(self.filesManagement1.sentences)):
            sentence1 = self.filesManagement1.sentences[sentenceNo];
            sentence2 = self.filesManagement2.sentencesNulled[sentenceNo];
            for word1 in sentence1:
                for word2 in sentence2:
                    self.c1[word2] = 0;
                    self.c2[word2][word1] = 0;

        # updating Cs
        print("\tUpdating C parameters ...");
        for sentenceNo in xrange(len(self.filesManagement1.sentences)):
            sentence1 = self.filesManagement1.sentences[sentenceNo];
            sentence2 = self.filesManagement2.sentencesNulled[sentenceNo];
            for word1 in sentence1:
                
                deltaDiv = 0;
                for word2 in sentence2:
                    deltaDiv += self.t[word1][word2]; 

                for word2 in sentence2:
                    delta = self.t[word1][word2]/deltaDiv;
                    self.c1[word2] += delta;
                    self.c2[word2][word1] += delta;

        # updating Ts
        print("\tUpdating T parameters ...");
        for sentenceNo in xrange(len(self.filesManagement1.sentences)):
            sentence1 = self.filesManagement1.sentences[sentenceNo];
            sentence2 = self.filesManagement2.sentencesNulled[sentenceNo];
            for word1 in sentence1:
                for word2 in sentence2:
                    self.t[word1][word2] = self.c2[word2][word1] / self.c1[word2];

        # debug
        self.insightParamsT(5, 3)
        print("Iteration finished ...");

    def alignAndSaveIBM1(self, filesManagement1, filesManagement2, fileout):
        self.filesManagement1 = filesManagement1;
        self.filesManagement2 = filesManagement2;
        self.fileout = fileout;

        print("Aligning and saving started ...");
        
        try:
            self.file = codecs.open(self.fileout, encoding="utf-8", mode="w")
        except Exception:
            print("%s: %s, %s: %s" %(self.__class__.__name__, "storing T params", "Error accessing storage file", self.fileout))
            sys.exit(1)
            
        for sentenceNo in xrange(len(self.filesManagement1.sentences)):
            sentence1 = self.filesManagement1.sentences[sentenceNo];
            sentence2 = self.filesManagement2.sentencesNulled[sentenceNo];
            w1i = 0
            for word1 in sentence1:
                aMaxVal = 0;
                aMaxIndex = 0;
                w2i = 0;
                for word2 in sentence2:
                    a = self.t[word1][word2];
                    if(a > aMaxVal):
                        aMaxVal = a;
                        aMaxIndex = w2i;
                    w2i += 1
                self.file.write(" %d %d %d\n" % ((sentenceNo+1), aMaxIndex, (w1i+1)));
                w1i += 1

        self.file.close();
                

        print("Aligning and saving finished ...");
        
    def loadParamsIBM1(self, filenameParams):
        self.filenameParams = filenameParams;

        
        print("Loading params started ...");

        print("\tLoading T params started ...");
        self.t = TranslatorTContainer.defaultTree();

        try:
            self.file = codecs.open(self.filenameParams, encoding="utf-8", mode="r")
        except Exception:
            print("%s: %s, %s: %s" %(self.__class__.__name__, "storing T params", "Error accessing storage file", self.filenameParams))
            sys.exit(1)
            

        lineNo = 0
        # http://docs.python.org/2/library/re.html
        
        for line in self.file:
            lineNo=lineNo+1;
            
            if(line.count(TranslatorTrainer.PARAMS_KEY_1_SEPARATOR_RIGHT) != 1):
                print("Wrongly formated t-params line (occurence of '%s'=%d): %s" % (TranslatorTrainer.PARAMS_KEY_1_SEPARATOR_RIGHT, line.count(TranslatorTrainer.PARAMS_KEY_1_SEPARATOR_RIGHT), line));
            word1, word1Ts = line.split(TranslatorTrainer.PARAMS_KEY_1_SEPARATOR_RIGHT);
            word1 = word1[1:]; # skiping TranslatorTrainer.PARAMS_KEY_1_SEPARATOR_LEFT
            word2Vals = [x.strip() for x in word1Ts.split()];
            for word2Val in word2Vals:
                word2, val = word2Val.split("@");
                self.t[word1][word2] = float(val);

        self.file.close();

        print("\tLoading T params finished ...");
        # debug
        self.insightParamsT(5, 3)

        print("Loading params finished ...");
                
    def saveParamsIBM1(self, filenameParams):
        self.filenameParams = filenameParams;
        print("Saving params started ...");

        print("\tSaving T params started ...");

        try:
            self.file = codecs.open(self.filenameParams, encoding="utf-8", mode="w")
        except Exception:
            print("%s: %s, %s: %s" %(self.__class__.__name__, "storing T params", "Error accessing storage file", self.filenameParams))
            sys.exit(1)
            
        for word1, hash2 in self.t.items():
            #print("W1: %s" % (word1));
            self.file.write("%s%s%s"%(TranslatorTrainer.PARAMS_KEY_1_SEPARATOR_LEFT, word1, TranslatorTrainer.PARAMS_KEY_1_SEPARATOR_RIGHT));
            for word2, tVal in hash2.items():
                self.file.write(" %s%s%e" % (word2, TranslatorTrainer.PARAMS_KEY_VALUE_SEPARATOR, tVal));
            self.file.write("\n");

        self.file.close();
        print("\tSaving T params finished ...");

        print("Saving params finished ...");