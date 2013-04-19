from __future__ import division

import sys
import re
import json;

from collections import defaultdict;

def defaultTree():
    return defaultdict(defaultTree);

class ParsingPreprocessing(object):
    RARE_WORD = "_RARE_";
    RARE_COUNT = 5;

    @staticmethod
    def WordNormalize(word):
        word = word.lower();
        return word;

    def __init__(self):
        self.filenameIn = "";
        self.filenameOut = "";
        self.sentenceTrees = [];
        self.wordsCount = defaultTree();
        self.wordsRare = defaultTree();

    def load(self, filenameIn):
        self.filenameIn = filenameIn
        print("Preprocessing reading file (%s) started ..." % (self.filenameIn));

        self.sentenceTrees = [];
        self.wordsCount = defaultTree();
        self.wordsRare = defaultTree();

        try:
            self.file = open(self.filenameIn)
        except Exception:
            print ("[BukvikParser:parseFile]: problem opening file filenameIn %s" % (self.filenameIn));
            sys.exit(1)
        
        # loading sentence trees and building word occurence counts
        lineNo = 0;
        for line in self.file:
            lineNo=lineNo+1;

            tree = json.loads(line);
            self.sentenceTrees.append(tree);

            self.innerParseLoad(tree);

        print("Preprocessing reading finished ...");

    def innerParseLoad(self, tree):
        #treeRoot = tree[0];
        #print("Tree rootTree: %s, Len:%d" % (str(treeRoot), len(treeRoot)));
        treeLeft = tree[1];


        isUnaryRule = False;
        treeRight = None;
        branchesNo = len(tree)-1;
        if(branchesNo == 1):
            isUnaryRule = True;
        else:
            treeRight = tree[2];
        if(isUnaryRule):
            word = treeLeft;
            print ("Word found: %s" % (word));
            if(not self.wordsCount.has_key(word)):
                self.wordsCount[word] = 0;
            self.wordsCount[word] = self.wordsCount[word] + 1;

        else:
            self.innerParseLoad(treeLeft);
            self.innerParseLoad(treeRight);

    def save(self, filenameOut):
        self.filenameOut = filenameOut;
        print("Preprocessing saving started ...");
        try:
            self.file = open(self.filenameOut, "w")
        except Exception:
            print ("[ParsingPreprocessing:save]: problem opening file (%s) for saving" % (self.filenameIn));
            sys.exit(1)

        # loading sentence trees and building word occurence counts
        lineNo = 0;
        print "Saving sentences";
        for sentenceTree in self.sentenceTrees:
            lineNo=lineNo+1;

            self.innerParseSave(sentenceTree);
            
            sentenceTreeStr = json.dumps(sentenceTree, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, \
                                         indent=None, separators=None, encoding="windows-1251", default=None, sort_keys=False);
            #sentenceTreeStr = str(sentenceTree);
            #sentenceTreeStr = sentenceTreeStr.replace("'", '"');
            self.file.write(sentenceTreeStr + "\n");
            
        self.file.close();
        print("Preprocessing saving finished ...");

    def innerParseSave(self, tree):
        #treeRoot = tree[0];
        #print("Tree rootTree: %s, Len:%d" % (str(treeRoot), len(treeRoot)));
        treeLeft = tree[1];

        isUnaryRule = False;
        treeRight = None;
        branchesNo = len(tree)-1;
        if(branchesNo == 1):
            isUnaryRule = True;
        else:
            treeRight = tree[2];
        if(isUnaryRule):
            word = treeLeft;
            #print ("Word found: %s" % (word));
            if(self.wordsCount.has_key(word) and self.wordsCount[word] < ParsingPreprocessing.RARE_COUNT):
                print("Rare (%d) word found: %s" %(self.wordsCount[word], word))
                tree[1] = ParsingPreprocessing.RARE_WORD;
        else:
            self.innerParseSave(treeLeft);
            self.innerParseSave(treeRight);