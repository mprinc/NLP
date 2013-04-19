#!/usr/bin/python

# Necessary to avoid rounding on integer numbers
from __future__ import division

import argparse

from nlp.parser.ParsingPreprocessing import ParsingPreprocessing
from nlp.parser.ParsingCounts import ParsingCounts;
from nlp.parser.ParserReadCounts import ParserReadCounts;
from nlp.parser.ParserCKY import ParserCKY;
from nlp.parser.ParserPiContext import ParserPiContext;

print("PCFG parsing started ...");

parser = argparse.ArgumentParser(description='PCFG Parser (NLP Coursera Homework Homework 2)');
parser.add_argument('--phase', '-p', action='store',help='Phase of gene tagging');
parser.add_argument('--filein', '-fin', action='store',help='Input file name');
parser.add_argument('--filecounts', '-fcounts', action='store',help='Counts file name');
parser.add_argument('--fileout', '-fout', action='store',help='Output file name');
args = parser.parse_args();

if not args.phase:
    print "ERROR: You should provide a --phase parameter\n";
    parser.print_help();
    exit(0);
print("Phase: " + args.phase);

if(args.phase == 'preprocess_rare'):
    if(not args.filein):
        print "ERROR: You should provide --filein parameter\n";
        exit(0);

    if(not args.fileout):
        print "ERROR: You should provide --fileout parameter\n";
        exit(0);
    print("Preprocessing for rare words started");
    parsingPreprocessing = ParsingPreprocessing();
    parsingPreprocessing.load(args.filein);
    parsingPreprocessing.save(args.fileout);
    print("Preprocessing for rare words finished");

if(args.phase == 'cky'):
    if(not args.filein):
        print "ERROR: You should provide --filein parameter\n";
        exit(0);

    if(not args.fileout):
        print "ERROR: You should provide --fileout parameter\n";
        exit(0);
    print("Parsing with CKY started");
    parsingCounts = ParsingCounts()
    countsReader = ParserReadCounts();
    parser = ParserCKY();

    countsReader.load(args.filecounts, parsingCounts);
    parser.parse(args.filein, parsingCounts);
    parser.save(args.fileout);

    print("Parsing with CKY finished");

print("PCFG parsing finished");
exit(0);