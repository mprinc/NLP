from __future__ import division

from collections import defaultdict
from nlp.parser.ParserRule import ParserRule

def defaultTree():
    return defaultdict(defaultTree);

class ParsingCounts(object):
    def __init__(self):
        self.nonterminalsCount = defaultTree(); # [var_non_terminal] = var_count
        self.binaryRulesCount = defaultTree(); # [var_non_terminal_1][var_non_terminal_2][var_non_terminal_3] = var_count
        self.unaryRulesCount = defaultTree();  # [var_non_terminal][var_terminal] = var_count
        self.qBinaryRulesCount = defaultTree(); # [var_non_terminal_1][var_non_terminal_2][var_non_terminal_3] = freq
        self.qUnaryRulesCount = defaultTree();  # [var_non_terminal][var_terminal] = freq
        self.nonTerminals = defaultTree();  # [var_non_terminal] = True
        self.terminals = defaultTree();  # [var_non_terminal] = True

    def getAllRulesForNonTerminal(self, X):
        rules = [];
        if(self.qBinaryRulesCount.has_key(X)):
            for Y in self.qBinaryRulesCount[X].keys():
                for Z in self.qBinaryRulesCount[X][Y].keys():
                    rule = ParserRule();
                    rule.type = ParserRule.TYPE_BINARY;
                    rule.X = X;
                    rule.Y = Y;
                    rule.Z = Z;
                    rule.weight = self.qBinaryRulesCount[X][Y][Z];

                    rules.append(rule);
        return rules;
        
    def getEmissionCountOr0(self, word, tag):
        if(not self.emissionCount.has_key(word)):
            return 0;
        if(not self.emissionCount[word].has_key(tag)):
            return 0;
        return self.emissionCount[word][tag];
        
    def getTrigramCountOr0(self, tag1, tag2, tag3):
        if(not self.binaryRulesCount.has_key(tag1)):
            return 0;
        if(not self.binaryRulesCount[tag1].has_key(tag2)):
            return 0;
        if(not self.binaryRulesCount[tag1][tag2].has_key(tag3)):
            return 0;
        return self.binaryRulesCount[tag1][tag2][tag3];   