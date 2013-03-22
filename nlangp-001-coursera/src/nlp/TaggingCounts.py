from collections import defaultdict

def defaultTree():
    return defaultdict(defaultTree);

class TaggingCounts(object):
    def __init__(self):
        self.words = [];
        self.tags = [];
        
        self.wordsHash = defaultTree(); # [var_word] = True/False
        self.tagssHash = defaultTree(); # [var_tag] = True/False
        
        self.emissionCountMax = defaultTree(); # [var_word] = var_tag
        self.emissionCount = defaultTree(); # [var_word][var_tag] = freq
        self.wordTagCount = defaultTree(); # [var_word][var_tag] = var_count
        self.unigramsCount = defaultTree(); # [var_tag_1] = var_count
        self.bigramsCount = defaultTree();  # [var_tag_1][var_tag_2] = var_count
        self.trigramsCount = defaultTree(); # [var_tag_1][var_tag_2][var_tag_3] = var_count