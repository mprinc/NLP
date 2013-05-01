# Necessary to avoid rounding on integer numbers
from __future__ import division

import sys;
import re;
import json;

# TODO: Check about __getitem__ method
# If i do:
#     p = ParserPiContainer();
#     p[0] = 5;
# python should report: TypeError: 'ParserPiContainer' object has no attribute '__getitem__'

from collections import defaultdict;

class ParserPiContainer(object):
    @staticmethod
    def defaultTree():
        return defaultdict(ParserPiContainer.defaultTree);


    def __init__(self, iSize=1, jSize=1):
        self.iSize = iSize;
        self.jSize = jSize;
        self.piArray = [None]*self.iSize;
        for i in range(self.iSize):
            self.piArray[i] = [None]*self.jSize;
            for j in range(self.jSize):
                self.piArray[i][j] = ParserPiContainer.defaultTree();

    def get(self, i, j, X):
        #print("[ParserPiContainer::get] Pi(%d, %d, %s) requested" % (i, j, X));
        if(i<0 or i >= self.iSize):
            print("[ParserPiContainer::get] Error: i dimension is wrong. Asked %d and max possible is: %d" % (i, self.iSize));
            return None;
        if(j<0 or j >= self.jSize):
            print("[ParserPiContainer::get] Error: j dimension is wrong. Asked %d and max possible is: %d, i=%d" % (j, self.jSize, i));
            return None;
        piIJArray = self.piArray[i][j];
        #print("[ParserPiContainer::get] piIJArray = %s" % (str(piIJArray)));
        if(not piIJArray.has_key(X)):
            print("[ParserPiContainer::get] Error: X dimension is wrong. Asked for '%s'to get under (%d,%d) location but it is not stored there" % (X, i, j));            
            return None;
        return piIJArray[X];
        
    def getPi(self, i, j, X):
        piContent = self.get(i, j, X);
        if(isinstance(piContent, ParserPiContainer)):
            return None;
        return piContent.pi;
        
    def setPi(self, i, j, X, pi):
        piContent = self.get(i, j, X);
        if(isinstance(piContent, ParserPiContainer)):
            return None;
        piContent.pi = pi;
        
    def create(self, i, j, X, val):
        ##if(i != j):
        ##    print("i=%d,j=%d" %(i,j));
        #print("[ParserPiContainer::create] Pi(%d, %d, %s) requested" % (i, j, X));
        if(i<0 or i >= self.iSize):
            print("[ParserPiContainer::create] Error: i dimension is wrong. Asked %d and max possible is: %d" % (i, self.iSize));
            raise Exception("[ParserPiContainer::create] Error: i dimension is wrong. Asked %d and max possible is: %d" % (i, self.iSize));
            return None;
        if(j<0 or j >= self.jSize):
            print("[ParserPiContainer::create] Error: j dimension is wrong. Asked %d and max possible is: %d (i=%d)" % (j, self.jSize, i));
            raise Exception("[ParserPiContainer::create] Error: j dimension is wrong. Asked %d and max possible is: %d" % (j, self.iSize));
            return None;
        piIJArray = self.piArray[i][j];
        #print("[ParserPiContainer::create] piIJArray = %s" % (str(piIJArray)));
        if(piIJArray.has_key(X)):
            print("[ParserPiContainer::create] Error: X dimension is wrong. Asked for '%s'to create under (%d,%d) location but it is already stored there" % (X, i, j));            
            raise Exception("[ParserPiContainer::create] Error: X dimension is wrong. Asked for '%s'to create under (%d,%d) location but it is already stored there" % (X, i, j))
            return None;
        piIJArray[X] = val;
        return val;
        
    def delete(self, i, j, X):
        #print("[ParserPiContainer::delete] Pi(%d, %d, %s) requested" % (i, j, X));
        if(i<0 or i >= self.iSize):
            print("[ParserPiContainer::delete] Error: i dimension is wrong. Asked %d and max possible is: %d" % (i, self.iSize));
            return None;
        if(j<0 or j >= self.jSize):
            print("[ParserPiContainer::delete] Error: j dimension is wrong. Asked %d and max possible is: %d" % (j, self.jSize));
            return None;
        piIJArray = self.piArray[i][j];
        #print("[ParserPiContainer::delete] piIJArray = %s" % (str(piIJArray)));
        if(not piIJArray.has_key(X)):
            print("[ParserPiContainer::delete] Error: X dimension is wrong. Asked for '%s' to delete under (%d,%d) location but it is not stored there" % (X, i, j));            
            return None;
        val = piIJArray[X];
        del piIJArray[X];
        return val;
        
    def set(self, i, j, X, val):
        #print("[ParserPiContainer::set] Pi(%d, %d, %s) requested" % (i, j, X));
        if(i<0 or i >= self.iSize):
            print("[ParserPiContainer::set] Error: i dimension is wrong. Asked %d and max possible is: %d" % (i, self.iSize));
            return None;
        if(j<0 or j >= self.jSize):
            print("[ParserPiContainer::set] Error: j dimension is wrong. Asked %d and max possible is: %d" % (j, self.jSize));
            return None;
        piIJArray = self.piArray[i][j];
        #print("[ParserPiContainer::set] piIJArray = %s" % (str(piIJArray)));
        if(not piIJArray.has_key(X)):
            print("[ParserPiContainer::set] Error: X dimension is wrong. Asked for '%s'to set under (%d,%d) location but it is not stored there" % (X, i, j));            
            return None;
        piIJArray[X] = val;
        return val;        