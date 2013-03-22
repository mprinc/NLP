#!/usr/bin/python

# Necessary to avoid rounding on integer numbers
from __future__ import division

import argparse

from nlp.TaggingPreprocessing import TaggingPreprocessing
from nlp.TaggingCounts import TaggingCounts
from nlp.ReadCounts import ReadCounts

print("Gene Tagging started ...");

parser = argparse.ArgumentParser(description='Gene Tagging (NLP Coursera Homework W1)');
parser.add_argument('--phase', '-p', action='store',help='Phase of gene tagging'); #, default='tag');
parser.add_argument('--filein', '-fin', action='store',help='Input file name');
parser.add_argument('--filecounts', '-fcounts', action='store',help='Counts file name');
parser.add_argument('--fileout', '-fout', action='store',help='Output file name');
args = parser.parse_args();

if not args.phase:
    print "ERROR: You should provide --phase parameter\n";
    parser.print_help();
    exit(0);

print("Phase: " + args.phase);
if(args.phase == 'preprocess'):
    if(not args.filein):
        print "ERROR: You should provide --filein parameter\n";
        exit(0);

    if(not args.fileout):
        print "ERROR: You should provide --fileout parameter\n";
        exit(0);
        
    taggingPreprocessing = TaggingPreprocessing()
    taggingPreprocessing.load(args.filein);
    taggingPreprocessing.findRareWords();
    taggingPreprocessing.save(args.fileout);

if(args.phase == 'tag'):
    if(not args.filein):
        print "ERROR: You should provide --filein parameter\n";
        exit(0);

    if(not args.filecounts):
        print "ERROR: You should provide --filecounts parameter\n";
        exit(0);
        
    if(not args.fileout):
        print "ERROR: You should provide --fileout parameter\n";
        exit(0);
        
    taggingCounts = TaggingCounts()
    reader = ReadCounts();
    # relative to the current execution folder
    reader.load(args.filecounts, taggingCounts);
    reader.getEmissionParameters(taggingCounts);
    reader.tag(args.filein, args.fileout, taggingCounts);    

print("Gene Tagging finished");
exit(0);