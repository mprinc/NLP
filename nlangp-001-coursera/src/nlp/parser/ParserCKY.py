from __future__ import division

import sys
import re
import json;

from collections import defaultdict;

from ParsingCounts import ParsingCounts;
from nlp.parser.ParserPiContext import ParserPiContext;
from nlp.parser.ParserPiContainer import ParserPiContainer;
from nlp.parser.ParsingPreprocessing import ParsingPreprocessing;
from nlp.parser.ParserRule import ParserRule

def defaultTree():
    return defaultdict(defaultTree);

class ParserCKY(object):

    @staticmethod
    def WordNormalize(word):
        #word = word.lower();
        return word;

    def __init__(self):
        self.filenameIn = "";
        self.parsingCounts = ParsingCounts();
        self.piContainer = ParserPiContainer();
        self.sentencesJson = [];

    def initForSentence(self, words):
        print("[ParserCKY::init] initializing CKY parser");
        
        wordsNo = len(words);
        self.piContainer = ParserPiContainer(wordsNo, wordsNo);

        ''' testing
        wordsNo = 5;
        words = ["this", "is", "really", "Great", "thing"];
        self.piContainer = ParserPiContainer(wordsNo, wordsNo);
        self.piContainer.get(-1, 4, "N");
        self.piContainer.get(1, 6, "S");
        self.piContainer.get(3, 3, "S");
        val = self.piContainer.get(3, 3, "S");
        print("[ParserCKY::init] pi(%d,%d,%s)=%s" % (3, 3, "S", val));            
        self.piContainer.set(3, 3, "S", 5);
        self.piContainer.create(3, 3, "S", 5);
        self.piContainer.create(3, 3, "S", 8);
        val = self.piContainer.get(3, 3, "S");
        print("[ParserCKY::init] pi(%d,%d,%s)=%s" % (3, 3, "S", val));            
        self.piContainer.set(3, 3, "S", 888);
        val = self.piContainer.get(3, 3, "S");
        print("[ParserCKY::init] pi(%d,%d,%s)=%s" % (3, 3, "S", val));
        val = self.piContainer.delete(3, 3, "S");
        '''

        print("[ParserCKY::init] words = %s" % (words));
        #for X in self.parsingCounts.qUnaryRulesCount.keys():
        #    print("X: %s" %(X));

        for i in range(wordsNo):
            for X in self.parsingCounts.nonTerminals.keys():
                    piContext = ParserPiContext();
                    piContext.rule = ParserRule();
                    piContext.rule.type = ParserRule.TYPE_UNARY;
                    piContext.rule.X= X;
                    piContext.rule.terminal = None;
                    piContext.rule.weight = 0;
                    piContext.pi= 0;
                    piContext.s= i;

                    word = words[i];
                    if(self.parsingCounts.qUnaryRulesCount.has_key(X) and self.parsingCounts.qUnaryRulesCount[X].has_key(word)):
                        piContext.pi = self.parsingCounts.qUnaryRulesCount[X][word];
                        piContext.rule.terminal = word;
                        piContext.rule.weight = piContext.pi;
                        #print("[ParserCKY::init] AHA! pi(%d,%d,'%s')=%s, X->xi = '%s'->'%s'" % (i, i, X, piContext.pi, X, word));
                    
                    self.piContainer.create(i, i, X, piContext);
        '''
        val = self.piContainer.get(3, 3, "ADJ");
        print("[ParserCKY::init] pi(%d,%d,'%s')=%s" % (3, 3, "ADJ", val));
        '''

    def parseSentence(self, sentence):
        wordsNo = len(sentence);
        rule = ParserRule();

        for l in range(1, wordsNo):
            for i in range(wordsNo-l):
                j = i+l;
                #print("\tProcessing agains words:%s" %(sentence[i:j+1]));

                overallMaxX = None;
                overallMaxPi = 0;
                overallMaxS = -1;
                overallMaxPiContext = ParserPiContext();
                overallMaxPiContext = None;
                overallMaxRule = ParserRule();
                overallMaxRule = None;
                for X in self.parsingCounts.nonTerminals.keys():
                #for X in self.parsingCounts.qBinaryRulesCount.keys():
                    maxPi = 0;
                    maxS = -1;
                    maxRule = ParserRule();
                    maxRule = None;

                    rules = self.parsingCounts.getAllRulesForNonTerminal(X);
                    #if(len(rules)<=0):
                    #    print("\tNo rules fo NT:%s" %(X));

                    #print("\tProcessing NT:'%s' agains words:%s" %(X, sentence[i:j+1]));
                    for rule in rules:
                        #print("\t\tProcessing for NT:'%s' is: %s" %(X, rule));
                        Y = rule.Y;
                        Z = rule.Z;
                        q = rule.weight;
                        if(i == j):
                            #print ("i = j = %d" % (i));
                            exit();
                        for s in range(i, j): # i..(j-1)
                            #print("\t\t\ti=%d, s=%d, j=%d" %(i, s, j));
                            piLeft = self.piContainer.getPi(i, s, Y);
                            #if(piLeft > 0):
                                #print("\t\tProcessing for NT:'%s' is: %s" %(X, rule));
                                #print("\t\t\tYes: piLeft: %e, i=%d, s=%d, j=%d" %(piLeft, i, s, j));
                                #piContextLeft = self.piContainer.get(i, s, Y);
                                #print("\t\t\tYes: piContextLeft: %s" %(piContextLeft));
                            piRight = self.piContainer.getPi(s+1, j, Z);
                            #if(piRight > 0):
                                #print("\t\tProcessing for NT:'%s' is: %s" %(X, rule));
                                #print("\t\t\tYes: piRight: %e, i=%d, s=%d, j=%d" %(piRight, i, s, j));
                                #piContextRight = self.piContainer.get(s+1, j, Z);
                                #print("\t\t\tpiContextRight: %s" %(piContextRight));
                            pi = q * piLeft * piRight;
                            if(pi >= maxPi):
                                maxPi = pi;
                                maxS = s;
                                maxRule = rule;

                    piContext = ParserPiContext();
                    piContext.rule = maxRule;
                    piContext.pi = maxPi;
                    piContext.s = maxS;

                    #if(maxPi>0):
                    #    print("\tMax pi (X=%s, i=%d,j=%d)= %e, piContext=(%s)" % (X, i,j,maxPi,piContext));

                    val = self.piContainer.create(i, j, X, piContext);

                    if(val == None): exit();
                    if(maxPi >= overallMaxPi):
                        overallMaxX = X;
                        overallMaxPi = maxPi;
                        overallMaxS = maxS;
                        overallMaxRule = maxRule;
                        overallMaxPiContext = piContext;
                    if(overallMaxPiContext.pi != overallMaxPi):
                        print("(overallMaxPiContext.pi != overallMaxPi) = (%e != %e)" ^((overallMaxPiContext.pi, overallMaxPi)));
                        exit();
                #if(overallMaxPi > 0):
                #    print("\toverall max pi (overallMaxX=%s, i=%d,j=%d =>%s)= %e, piContext=(%s)" % (overallMaxX, i,j,sentence[i:j+1],overallMaxPi,overallMaxPiContext));
                #else:
                #    print("\t No overall max pi for the interval (i=%d,j=%d =>%s)" % (i,j,sentence[i:j+1]));

        piContext = self.piContainer.get(0, wordsNo-1, 'SBARQ');
        if(piContext.pi <= 0):
            print("Probability of sentence is <= 0 %s" % (sentence));

    def generateJson(self, sentence, start, end, rootNonTerminal, depth, rootJson):
        piContext = self.piContainer.get(start, end, rootNonTerminal);

        if(not isinstance(piContext, ParserPiContext)):
            print("we cannot continue, since piContext is wrong");
            exit(-1);

        rule = piContext.rule;
        if(isinstance(rule, ParserRule)):
            if(rule.type == ParserRule.TYPE_BINARY):
                rootLeft = [];
                rootRight = [];
                rootJson.append(rule.X);
                rootJson.append(rootLeft);
                rootJson.append(rootRight);                
                self.generateJson(sentence, start, piContext.s, rule.Y, depth+1, rootLeft);
                self.generateJson(sentence, piContext.s+1, end, rule.Z, depth+1, rootRight);
            elif(rule.type == ParserRule.TYPE_UNARY):
                rootJson.append(rule.X);
                rootJson.append(
                                # sorry boy, we need a real world, not _RARE_
                                #rule.terminal
                                sentence[start]
                                );
        else:
            print("we cannot continue, since rule is wrong");
            exit(-1);
        
    def describeTree(self, sentence, start, end, rootNonTerminal, depth):
        piContext = self.piContainer.get(start, end, rootNonTerminal);
        inlineStr = "";
        for i in range(depth):
            inlineStr = inlineStr + " | ";

        print("%s(%d,%d) %s, root:'%s' PI context: %s" %(inlineStr, start, end, sentence[start:end+1], rootNonTerminal, piContext));
        if(not isinstance(piContext, ParserPiContext)):
            print("%swe cannot continue, since piContext is wrong" %(inlineStr));
            return;
        rule = piContext.rule;
        if(isinstance(rule, ParserRule)):
            if(rule.type == ParserRule.TYPE_BINARY):
                self.describeTree(sentence, start, piContext.s, rule.Y, depth+1);
                self.describeTree(sentence, piContext.s+1, end, rule.Z, depth+1);
        else:
            print("%swe cannot continue, since rule is wrong" %(inlineStr));

    def describeTreeNice(self, sentence, start, end, rootNonTerminal, depth):
        piContext = self.piContainer.get(start, end, rootNonTerminal);

        inlineStr = "";
        for i in range(depth):
            inlineStr = inlineStr + " | ";

        if(not isinstance(piContext, ParserPiContext)):
            print("%swe cannot continue, since piContext is wrong" %(inlineStr));
            return;

        rule = piContext.rule;
        if(isinstance(rule, ParserRule)):
            if(rule.type == ParserRule.TYPE_BINARY):
                print("%s(%d,%d) <%s> -> <%s>, <%s>" %(inlineStr, start, end, rule.X, rule.Y, rule.Z));
                self.describeTreeNice(sentence, start, piContext.s, rule.Y, depth+1);
                self.describeTreeNice(sentence, piContext.s+1, end, rule.Z, depth+1);
            elif(rule.type == ParserRule.TYPE_UNARY):
                print("%s(%d,%d) <%s> -> [%s]" %(inlineStr, start, end, rule.X, rule.terminal));                
        else:
            print("%swe cannot continue, since rule is wrong" %(inlineStr));
        
    def parse(self, filenameIn, parsingCounts):
        self.filenameIn = filenameIn
        self.parsingCounts = parsingCounts;

        print("[ParserCKY::parse] Parsing file (%s) started ..." % (self.filenameIn));

        self.sentenceTrees = [];
        self.wordsCount = defaultTree();
        self.wordsRare = defaultTree();
        self.sentences = [];        
        self.sentencesJson = [];

        try:
            self.file = open(self.filenameIn);
        except Exception:
            print ("[ParserCKY:parse]: problem opening file filenameIn %s" % (self.filenameIn));
            sys.exit(1)

        # loading sentence trees and building word occurence counts
        lineNo = 0;
        for line in self.file:
            lineNo=lineNo+1;

            sentence = line.split();
            
            print("");

            print("Sentence original: %s" % (sentence));
            sentenceRare = sentence[:];
            for i, word in enumerate(sentenceRare):
                if(not self.parsingCounts.terminals.has_key(word)):
                    sentenceRare[i] = ParsingPreprocessing.RARE_WORD;
            print("Sentence replaced rare words: %s" % (sentenceRare));
    

            self.sentences.append(sentence);
            print("Processing line: %d" %(lineNo));
            self.initForSentence(sentenceRare);
            self.parseSentence(sentenceRare);

            wordsNo = len(sentence);
            #self.describeTreeNice(sentence, 0, wordsNo-1, 'SBARQ', 0);
            sentenceJson = [];
            self.generateJson(sentence, 0, wordsNo-1, 'SBARQ', 0, sentenceJson);
            self.sentencesJson.append(sentenceJson);
            print("Json: %s" % (sentenceJson));

        print("[ParserCKY:parse]: Preprocessing reading finished ...");

    def save(self, filenameOut):
        self.filenameOut = filenameOut;
        print("Parser saving started ...");
        try:
            self.file = open(self.filenameOut, "w")
        except Exception:
            print ("[ParserCKY:save]: problem opening file (%s) for saving" % (self.filenameIn));
            sys.exit(-1);

        # loading sentence trees and building word occurence counts
        lineNo = 0;
        print "Saving sentences";
        for sentenceJson in self.sentencesJson:
            lineNo=lineNo+1;

            sentenceJsonStr = json.dumps(sentenceJson, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, \
                                         indent=None, separators=None, encoding="windows-1251", default=None, sort_keys=False);
            self.file.write(sentenceJsonStr + "\n");
            
        self.file.close();
        print("Parser saving finished ...");

