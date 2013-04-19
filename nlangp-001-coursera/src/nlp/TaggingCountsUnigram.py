from __future__ import division

from collections import defaultdict

def defaultTree():
    return defaultdict(defaultTree);

class TaggingCountsUnigram(object):
    def __init__(self):
        self.words = [];
        self.tags = [];
        
        self.wordsHash = defaultTree(); # [var_word] = True/False
        self.tagssHash = defaultTree(); # [var_tag] = True/False
        
        self.emissionCountMax = defaultTree(); # [var_word] = var_tag
        self.emissionCount = defaultTree(); # [var_word][var_tag] = freq
        self.wordTagCount = defaultTree(); # [var_word][var_tag] = var_count
        self.nonterminalsCount = defaultTree(); # [var_tag_1] = var_count
        self.bigramsCount = defaultTree();  # [var_tag_1][var_tag_2] = var_count
        self.binaryRulesCount = defaultTree(); # [var_tag_1][var_tag_2][var_tag_3] = var_count
        
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
        