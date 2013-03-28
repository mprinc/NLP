#!/usr/bin/python

# Necessary to avoid rounding on integer numbers
from __future__ import division

import argparse

from nlp.TaggingPreprocessing import TaggingPreprocessing
from nlp.TaggingCountsUnigram import TaggingCountsUnigram
from nlp.TaggingCountsViterbi import TaggingCountsViterbi
from nlp.ReadCounts import ReadCounts
from nlp.TaggerUnigram import TaggerUnigram
from nlp.TaggerViterbi import TaggerViterbi

print("Gene Tagging started ...");

parser = argparse.ArgumentParser(description='Gene Tagging (NLP Coursera Homework W1)');
parser.add_argument('--phase', '-p', action='store',help='Phase of gene tagging'); #, default='tag1');
parser.add_argument('--filein', '-fin', action='store',help='Input file name');
parser.add_argument('--filecounts', '-fcounts', action='store',help='Counts file name');
parser.add_argument('--fileout', '-fout', action='store',help='Output file name');
args = parser.parse_args();

'''
# Testing words classification
words = ['CopA', '#a1', 'alL', 'ALL', '111', 'aLL', '1aL'];
for word in words:
    print word;
    wordClass = TaggingPreprocessing.getRareWordClass(word);
    print wordClass;
exit(0);
'''
withClasses = True;

if not args.phase:
    print "ERROR: You should provide a --phase parameter\n";
    parser.print_help();
    exit(0);
print("Phase: " + args.phase);

if(args.phase == 'preprocess_unigram'):
    if(not args.filein):
        print "ERROR: You should provide --filein parameter\n";
        exit(0);

    if(not args.fileout):
        print "ERROR: You should provide --fileout parameter\n";
        exit(0);
        
    taggingPreprocessing = TaggingPreprocessing()
    taggingPreprocessing.load(args.filein);
    taggingPreprocessing.findRareWordsClasses(False);
    taggingPreprocessing.saveUnigram(args.fileout);

if(args.phase == 'preprocess_viterbi'):
    if(not args.filein):
        print "ERROR: You should provide --filein parameter\n";
        exit(0);

    if(not args.fileout):
        print "ERROR: You should provide --fileout parameter\n";
        exit(0);
        
    taggingPreprocessing = TaggingPreprocessing()
    taggingPreprocessing.load(args.filein);
    taggingPreprocessing.findRareWordsClasses(False);
    taggingPreprocessing.saveViterbi(args.fileout, False);

if(args.phase == 'preprocess_viterbi_c'):
    if(not args.filein):
        print "ERROR: You should provide --filein parameter\n";
        exit(0);

    if(not args.fileout):
        print "ERROR: You should provide --fileout parameter\n";
        exit(0);
        
    taggingPreprocessing = TaggingPreprocessing()
    taggingPreprocessing.load(args.filein);
    taggingPreprocessing.findRareWordsClasses(withClasses);
    taggingPreprocessing.saveViterbi(args.fileout, withClasses);

if(args.phase == 'tag_unigram'):
    if(not args.filein):
        print "ERROR: You should provide --filein parameter\n";
        exit(0);

    if(not args.filecounts):
        print "ERROR: You should provide --filecounts parameter\n";
        exit(0);
        
    if(not args.fileout):
        print "ERROR: You should provide --fileout parameter\n";
        exit(0);
        
    taggingCountsUnigram = TaggingCountsUnigram()
    reader = ReadCounts();
    taggerUnigram = TaggerUnigram()

    reader.load(args.filecounts, taggingCountsUnigram);
    taggerUnigram.getEmissionParameters(taggingCountsUnigram);
    taggerUnigram.tag(args.filein, args.fileout);    

if(args.phase == 'tag_viterbi'):
    if(not args.filein):
        print "ERROR: You should provide --filein parameter\n";
        exit(0);

    if(not args.filecounts):
        print "ERROR: You should provide --filecounts parameter\n";
        exit(0);
        
    if(not args.fileout):
        print "ERROR: You should provide --fileout parameter\n";
        exit(0);
        
    taggingCountsUnigram = TaggingCountsUnigram();
    taggingCountsViterbi = TaggingCountsViterbi(taggingCountsUnigram);
    reader = ReadCounts();
    taggerUnigram = TaggerUnigram();
    taggerViterbi = TaggerViterbi();

    reader.load(args.filecounts, taggingCountsUnigram);
    
    taggerUnigram.getEmissionParameters(taggingCountsUnigram);
    taggingCountsViterbi.calculateTagsSet();

    taggerViterbi.getEmissionParameters(taggingCountsUnigram, taggingCountsViterbi);
    taggerViterbi.tag(args.filein, args.fileout, False);    

if(args.phase == 'tag_viterbi_c'):
    if(not args.filein):
        print "ERROR: You should provide --filein parameter\n";
        exit(0);

    if(not args.filecounts):
        print "ERROR: You should provide --filecounts parameter\n";
        exit(0);
        
    if(not args.fileout):
        print "ERROR: You should provide --fileout parameter\n";
        exit(0);
        
    taggingCountsUnigram = TaggingCountsUnigram();
    taggingCountsViterbi = TaggingCountsViterbi(taggingCountsUnigram);
    reader = ReadCounts();
    taggerUnigram = TaggerUnigram();
    taggerViterbi = TaggerViterbi();

    reader.load(args.filecounts, taggingCountsUnigram);
    
    taggerUnigram.getEmissionParameters(taggingCountsUnigram);
    taggingCountsViterbi.calculateTagsSet();

    taggerViterbi.getEmissionParameters(taggingCountsUnigram, taggingCountsViterbi);
    taggerViterbi.tag(args.filein, args.fileout, withClasses);

print("Gene Tagging finished");
exit(0);