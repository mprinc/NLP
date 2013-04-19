# Necessary to avoid rounding on integer numbers
from __future__ import division

import sys
import re

from ParsingCounts import ParsingCounts

class ParserReadCounts(object):
    def __init__(self):
        self.filenameIn = "";
        self.parsingCounts = ParsingCounts();

    def load(self, filenameIn, parsingCounts):
        self.filenameIn = filenameIn
        self.parsingCounts = parsingCounts
        print("Reading");
        try:
            self.file = open(self.filenameIn)
        except Exception:
            print "[ParsingCounts:load]: problem opening file filenameIn = ", self.filenameIn
            sys.exit(1)
            
        lineNo = 0
        # http://docs.python.org/2/library/re.html
        rex_nonterminal = re.compile(r'^\s*(\d+)\s+NONTERMINAL\s+(\S+)\s*$') # 17 NONTERMINAL NP
        rex_binaryrule = re.compile(r'^\s*(\d+)\s+BINARYRULE\s+(\S+)\s+(\S+)\s+(\S+)\s*$') # 918 BINARYRULE NP DET NOUN
        rex_unaryrule = re.compile(r'^\s*(\d+)\s+UNARYRULE\s+(\S+)\s+(\S+)\s*$') # 8 UNARYRULE NP+NOUN place
        
        for line in self.file:
            lineNo=lineNo+1;

            match = rex_nonterminal.search(line)
            if match:
                var_count = int(match.group(1));
                var_non_terminal = match.group(2);
                #if(lineNo < 20):
                #    print("NONTERMINAL: count: %d, non-terminal: %s" % (var_count, var_non_terminal));
                self.parsingCounts.nonterminalsCount[var_non_terminal] = int(var_count);
                self.parsingCounts.nonTerminals[var_non_terminal] = True;
                continue

            match = rex_binaryrule.search(line)
            if match:
                var_count = int(match.group(1));
                var_non_terminal_1 = match.group(2)
                var_non_terminal_2 = match.group(3)
                var_non_terminal_3 = match.group(4)
                #print "Unigram: count:" + var_count + ", tag_1: " + var_tag_1
                self.parsingCounts.binaryRulesCount[var_non_terminal_1][var_non_terminal_2][var_non_terminal_3] = int(var_count);
                self.parsingCounts.nonTerminals[var_non_terminal_1] = True;
                self.parsingCounts.nonTerminals[var_non_terminal_2] = True;
                self.parsingCounts.nonTerminals[var_non_terminal_3] = True;
                continue;

            match = rex_unaryrule.search(line)
            if match:
                var_count = int(match.group(1));
                var_non_terminal = match.group(2)
                var_terminal = match.group(3)
                #print "Bigram: count:" + var_count + ", tag_1: " + var_tag_1 + ", tag_2: " + var_tag_2
                self.parsingCounts.unaryRulesCount[var_non_terminal][var_terminal] = int(var_count);
                self.parsingCounts.nonTerminals[var_non_terminal] = True;
                self.parsingCounts.terminals[var_terminal] = True;
                continue

            if not match:
                print str(lineNo)+":"+line
                continue

        #print ("Search nonterminalsCount['VP+VERBP']: %d" % (self.parsingCounts.nonterminalsCount['VP+VERB'])); # 254 NONTERMINAL VP+VERB
        #print ("Search binaryRulesCount['SQ']['VERB']['VP']: %d" % (self.parsingCounts.binaryRulesCount['SQ']['VERB']['VP'])); # 63 BINARYRULE SQ VERB VP
        #print ("Search unaryRulesCount['.']['_RARE_']: %d" % (self.parsingCounts.unaryRulesCount['.']['_RARE_'])); # 7 UNARYRULE . _RARE_
        
        for non_terminal in self.parsingCounts.unaryRulesCount.keys():
            for terminal in self.parsingCounts.unaryRulesCount[non_terminal].keys():
                self.parsingCounts.qUnaryRulesCount[non_terminal][terminal] = self.parsingCounts.unaryRulesCount[non_terminal][terminal] \
                    / self.parsingCounts.nonterminalsCount[non_terminal];

        for non_terminal_1 in self.parsingCounts.binaryRulesCount.keys():
            for non_terminal_2 in self.parsingCounts.binaryRulesCount[non_terminal_1].keys():
                for non_terminal_3 in self.parsingCounts.binaryRulesCount[non_terminal_1][non_terminal_2].keys():
                    self.parsingCounts.qBinaryRulesCount[non_terminal_1][non_terminal_2][non_terminal_3] \
                        = self.parsingCounts.binaryRulesCount[non_terminal_1][non_terminal_2][non_terminal_3] \
                        / self.parsingCounts.nonterminalsCount[non_terminal_1];
    