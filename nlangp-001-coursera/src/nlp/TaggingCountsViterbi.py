from __future__ import division

from collections import defaultdict

from TaggingCountsUnigram import TaggingCountsUnigram

def defaultTree():
    return defaultdict(defaultTree);

class TaggingCountsViterbi(object):
    TAG_START = '*';
    TAG_STOP = 'STOP';
    
    WORD_START = 'WORD-START';
    WORD_STOP = 'WORD-STOP';
    WORD_STOP_CHECK = '';

    def __init__(self, taggerUnigram):
        self.taggerUnigram = taggerUnigram;
        # No need for smoothing: https://class.coursera.org/nlangp-001/forum/thread?thread_id=342
        self.mleTrigram = defaultdict(defaultTree); # [var_tag_1][var_tag_2] = freq
        self.tags_1 = [];
        self.tags_k = [];
        self.tags_n_1 = [];
        
        # Sentence dependent params
        self.sentence_pi = defaultdict(defaultTree); # [k][var_tag_1][var_tag_2] = freq
        self.sentence_words_original = [];
        self.sentence_words_final = [];
        self.sentence_tags = [];
        
    def calculateTagsSet(self):
        self.tags_1 = [TaggingCountsViterbi.TAG_START];
        self.tags_k = self.taggerUnigram.tags[:];
        self.tags_n_1 = (self.taggerUnigram.tags[:]);
        self.tags_n_1.append(TaggingCountsViterbi.TAG_STOP);

    def getTagSet(self, k, isLast):
        if(k<1): return self.tags_1;
        elif(not isLast): return self.tags_k;
        else: return self.tags_n_1;

    def getPiOr0(self, k, tagk_1, tagk):
        if(not self.sentence_pi.has_key(k)):
            return 0;
        if(not self.sentence_pi[k].has_key(tagk_1)):
            return 0;
        if(not self.sentence_pi[k][tagk_1].has_key(tagk)):
            return 0;
        return self.sentence_pi[k][tagk_1][tagk];
        
    def getMLETrigramOr0(self, tag1, tag2, tag3):
        if(not self.mleTrigram.has_key(tag1)):
            return 0;
        if(not self.mleTrigram[tag1].has_key(tag2)):
            return 0;
        if(not self.mleTrigram[tag1][tag2].has_key(tag3)):
            return 0;
        return self.mleTrigram[tag1][tag2][tag3];

    def initSentence(self):
        self.sentence_pi = defaultdict(defaultTree);
        self.sentence_pi[0][TaggingCountsViterbi.TAG_START][TaggingCountsViterbi.TAG_START] = 1;