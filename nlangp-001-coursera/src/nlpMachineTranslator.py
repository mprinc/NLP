#!/usr/bin/python

# Necessary to avoid rounding on integer numbers
from __future__ import division

import argparse

from nlp.translation.FilesManagement import FilesManagement;
from nlp.translation.TranslatorTrainer import TranslatorTrainer

print("Machine Translating started ...");

parser = argparse.ArgumentParser(description='PCFG Parser (NLP Coursera Homework Homework 2)');
parser.add_argument('--phase', '-p', action='store',help='Phase of gene tagging');
parser.add_argument('--fileLang1in', '-finL1', action='store',help='Input file name');
parser.add_argument('--fileLang2in', '-finL2', action='store',help='Second Input file name');
parser.add_argument('--fileinAlignIn', '-finAlign', action='store',help='Second Input file name');
parser.add_argument('--fileparams', '-fparams', action='store',help='Params file name');
parser.add_argument('--fileout', '-fout', action='store',help='Output file name');
args = parser.parse_args();

if not args.phase:
    print "ERROR: You should provide a --phase parameter\n";
    parser.print_help();
    exit(0);
print("Phase: " + args.phase);

if(args.phase == 'trainIBM1'):
    if(not args.fileLang1in):
        print "ERROR: You should provide --fileLang1in parameter\n";
        exit(0);

    if(not args.fileLang2in):
        print "ERROR: You should provide --fileLang2in parameter\n";
        exit(0);

    if(not args.fileout):
        print "ERROR: You should provide --fileout parameter\n";
        exit(0);
    print("Training started");
    filesManagement1 = FilesManagement();
    filesManagement1.load(args.fileLang1in);

    filesManagement2 = FilesManagement();
    filesManagement2.load(args.fileLang2in);
    
    trainer = TranslatorTrainer();
    trainer.trainIBM1(filesManagement1, filesManagement2);
    trainer.saveParamsIBM1(args.fileout);
    trainer.loadParamsIBM1(args.fileout);

    #filesManagement1.save(args.fileout);
    #filesManagement2.save(args.fileout);
    
    print("Training finished");

if(args.phase == 'alignIBM1'):
    if(not args.fileLang1in):
        print "ERROR: You should provide --fileLang1in parameter\n";
        exit(0);

    if(not args.fileLang2in):
        print "ERROR: You should provide --fileLang2in parameter\n";
        exit(0);

    if(not args.fileparams):
        print "ERROR: You should provide --fileparams parameter\n";
        exit(0);

    if(not args.fileout):
        print "ERROR: You should provide --fileout parameter\n";
        exit(0);
    print("Training started");
    
    filesManagement1 = FilesManagement();
    filesManagement1.load(args.fileLang1in);

    filesManagement2 = FilesManagement();
    filesManagement2.load(args.fileLang2in);
    
    trainer = TranslatorTrainer();
    trainer.loadParamsIBM1(args.fileparams);
    trainer.alignAndSaveIBM1(filesManagement1, filesManagement2, args.fileout);

    print("Training finished");


print("Machine Translating finished");
exit(0);