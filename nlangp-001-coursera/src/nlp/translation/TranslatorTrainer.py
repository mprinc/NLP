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
        
        # IBM 1
        # If word1 is a word from the first language, and word2 is a word from the second language then we have the following organization        
        self.t = TranslatorTContainer.defaultTree();    # self.t[word1][word2]
        self.c1 = TranslatorTContainer.defaultTree();   # self.c1[word2]
        self.c2 = TranslatorTContainer.defaultTree();   # self.c2[word2][word1]

        # IBM 2
        self.q = TranslatorTContainer.defaultTree();    # self.q[j][i][l][m]
        self.c3 = TranslatorTContainer.defaultTree();   # self.c3[i][l][m]
        self.c4 = TranslatorTContainer.defaultTree();   # self.c4[j][i][l][m]

        self.wordsCount = defaultTree();

    # ===================================================================================================================
    # IBM 1
    # ===================================================================================================================
    
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

        print("\tLoading T params started (%s)..." % (self.filenameParams));
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

    # ===================================================================================================================
    # IBM 2
    # ===================================================================================================================
    

    # self.q = TranslatorTContainer.defaultTree();    # self.q[j][i][l][m]
    # self.c3 = TranslatorTContainer.defaultTree();   # self.c3[i][l][m]
    # self.c4 = TranslatorTContainer.defaultTree();   # self.c4[j][i][l][m]

    def trainIBM2(self, filesManagement1, filesManagement2, fileparams):
        self.filesManagement1 = filesManagement1;
        self.filesManagement2 = filesManagement2;
        self.fileparams = fileparams;
        self.t = TranslatorTContainer.defaultTree();
        self.q = TranslatorTContainer.defaultTree();
        
        print("IBM2 Training started ...");
        
        # load T params
        self.loadParamsIBM1(self.fileparams);

        self.initializeIBM2();
        for i in xrange(5):
            print("Running %d-th iteration" % (i+1));
            self.iterateIBM2();
            
        print("IBM2 Training finished ...");
        
    def initializeIBM2(self):
        print("IBM2 Initialization started ...");
        sentenceNo = 0
        # http://docs.python.org/2/library/re.html
        
        # 1 is added for NULL word
        for sentenceNo in xrange(len(self.filesManagement1.sentences)):
            sys.stdout.write("\rsentence %d" % (sentenceNo));
            sentence1 = self.filesManagement1.sentences[sentenceNo];
            sentence2 = self.filesManagement2.sentencesNulled[sentenceNo];
            m = len(sentence1);
            l = len(sentence2)-1; # neutralize NULL
            for i in xrange(m):
                for j in xrange(l+1):
                    # T params are already loaded
                    # self.t[word1][word2] = 1/words2No;
                    self.q[j][i][l][m] = 1/(l+1);
        print("");

        # debug
        self.insightParamsQ(2, 3, 3, 3)
        print("IBM2 Initialization finished ...");
        
    def insightParamsQ(self, jCount, iCount, lCount, mCount):
        print("Insigt on Q params ...");
        for j in xrange(jCount):
            if(not self.q.has_key(j)): continue
            for i in xrange(iCount):
                if(not self.q[j].has_key(j)): continue
                for l in xrange(lCount):
                    if(not self.q[j][i].has_key(l)): continue
                    for m in xrange(mCount):
                        if(not self.q[j][i][l].has_key(m)): continue
                        val = self.q[j][i][l][m];
                        print("\tq[%d,%d,%d,%d] = %e" % (j, i, l, m, val));
        
    def iterateIBM2(self):
        print("IBM2 Iteration started ...");
        self.c3 = TranslatorTContainer.defaultTree();
        self.c4 = TranslatorTContainer.defaultTree();
        
        # clear Cs
        print("\tClearing C parameters ...");
        for sentenceNo in xrange(len(self.filesManagement1.sentences)):
            sys.stdout.write("\rsentence %d" % (sentenceNo));
            sentence1 = self.filesManagement1.sentences[sentenceNo];
            sentence2 = self.filesManagement2.sentencesNulled[sentenceNo];
            m = len(sentence1);
            l = len(sentence2)-1; # neutralize NULL
            for i in xrange(m):
                for j in xrange(l+1):
                    self.c3[i][l][m] = 0;
                    self.c4[j][i][l][m] = 0;
        print("");

        # updating Cs
        print("\tUpdating C parameters ...");
        for sentenceNo in xrange(len(self.filesManagement1.sentences)):
            sys.stdout.write("\rsentence %d" % (sentenceNo));
            sentence1 = self.filesManagement1.sentences[sentenceNo];
            sentence2 = self.filesManagement2.sentencesNulled[sentenceNo];
            m = len(sentence1);
            l = len(sentence2)-1; # neutralize NULL
            for i in xrange(m):
                deltaDiv = 0;
                for j in xrange(l+1):
                    #if(not self.t.has_key(sentence1[i]) or not self.t[sentence1[i]].has_key(sentence2[j])):
                    #    print("deltaDiv: Missing T value (word1:%s, word2:%s)" % ( sentence1[i], sentence2[j] ))
                    deltaDiv += self.q[j][i][l][m] * self.t[sentence1[i]][sentence2[j]]; 

                for j in xrange(l+1):
                    #if(not self.t.has_key(sentence1[i]) or not self.t[sentence1[i]].has_key(sentence2[j])):
                    #    print("delta: Missing T value (word1:%s, word2:%s)" % ( sentence1[i], sentence2[j] ))
                    delta = ( self.q[j][i][l][m] * self.t ) / deltaDiv;
                    self.c3[i][l][m] += delta;
                    self.c4[j][i][l][m] += delta;
        print("");

        # updating Qs
        print("\tUpdating Q parameters ...");
        for sentenceNo in xrange(len(self.filesManagement1.sentences)):
            sys.stdout.write("\rsentence %d" % (sentenceNo));
            sentence1 = self.filesManagement1.sentences[sentenceNo];
            sentence2 = self.filesManagement2.sentencesNulled[sentenceNo];
            m = len(sentence1);
            l = len(sentence2)-1; # neutralize NULL
            for i in xrange(m):
                for j in xrange(l+1):
                    self.q[j][i][l][m] = self.c4[j][i][l][m] / self.c3[i][l][m];
        print("");

        # debug
        self.insightParamsQ(2, 3, 3, 3);

        print("IBM2 Iteration finished ...");

    def alignAndSaveIBM2(self, filesManagement1, filesManagement2, fileout):
        self.filesManagement1 = filesManagement1;
        self.filesManagement2 = filesManagement2;
        self.fileout = fileout;

        print("IBM2 Aligning and saving started ...");
        
        try:
            self.file = codecs.open(self.fileout, encoding="utf-8", mode="w")
        except Exception:
            print("%s: %s, %s: %s" %(self.__class__.__name__, "storing T params", "Error accessing storage file", self.fileout))
            sys.exit(1)
            
        for sentenceNo in xrange(len(self.filesManagement1.sentences)):
            sys.stdout.write("\rsentence %d" % (sentenceNo));
            sentence1 = self.filesManagement1.sentences[sentenceNo];
            sentence2 = self.filesManagement2.sentencesNulled[sentenceNo];
            m = len(sentence1);
            l = len(sentence2)-1; # neutralize NULL
            for i in xrange(m):
                aMaxVal = 0;
                aMaxIndex = 0;
                for j in xrange(l+1):
                    a = self.q[j][i][l][m] * self.t[sentence1[i]][sentence2[j]];
                    if(a > aMaxVal):
                        aMaxVal = a;
                        aMaxIndex = j;
                self.file.write(" %d %d %d\n" % ((sentenceNo+1), aMaxIndex, (i+1)));
        print("");

        self.file.close();
                

        print("IBM2 Aligning and saving finished ...");
        
    def loadParamsIBM2(self, filenameParams):
        self.filenameParams = filenameParams;

        
        print("IBM2 Loading params started ...");

        print("\tLoading Q params started (%s)..." % (self.filenameParams));
        self.q = TranslatorTContainer.defaultTree();

        try:
            self.file = codecs.open(self.filenameParams, encoding="utf-8", mode="r")
        except Exception:
            print("%s: %s, %s: %s" %(self.__class__.__name__, "storing T params", "Error accessing storage file", self.filenameParams))
            sys.exit(1)
            

        lineNo = 0
        # http://docs.python.org/2/library/re.html
        
        for line in self.file:
            lineNo=lineNo+1;
            
            (j, i, l, m, val) = line.split();
            self.q[int(j)][int(i)][int(l)][int(m)] = float(val);

        self.file.close();

        print("\tLoading Q params finished ...");
        # debug
        self.insightParamsQ(2, 3, 3, 3);


        print("IBM2 Loading params finished ...");
                
    def saveParamsIBM2(self, filenameParams):
        self.filenameParams = filenameParams;
        print("IBM2 Saving params started ...");

        print("\tSaving Q params started ...");

        try:
            self.file = codecs.open(self.filenameParams, encoding="utf-8", mode="w")
        except Exception:
            print("%s: %s, %s: %s" %(self.__class__.__name__, "storing T params", "Error accessing storage file", self.filenameParams))
            sys.exit(1)
            
        for j, hash2 in self.q.items():
            for i, hash3 in hash2.items():
                for l, hash4 in hash3.items():
                    for m, qVal in hash4.items():
                        self.file.write("%d %d %d %d %e\n" % (j, i, l, m, qVal));

        self.file.close();
        print("\tSaving Q params finished ...");

        print("IBM2 Saving params finished ...");