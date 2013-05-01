# Necessary to avoid rounding on integer numbers
from __future__ import division

from collections import defaultdict;

class TranslatorTContainer(object):
    @staticmethod
    def defaultTree():
        return defaultdict(TranslatorTContainer.defaultTree);


    def __init__(self):
        self.t = TranslatorTContainer.defaultTree();

    def get(self, i, j, X):
        #print("[TranslatorTContainer::get] Pi(%d, %d, %s) requested" % (i, j, X));
        if(i<0 or i >= self.iSize):
            print("[TranslatorTContainer::get] Error: i dimension is wrong. Asked %d and max possible is: %d" % (i, self.iSize));
            return None;
        if(j<0 or j >= self.jSize):
            print("[TranslatorTContainer::get] Error: j dimension is wrong. Asked %d and max possible is: %d, i=%d" % (j, self.jSize, i));
            return None;
        piIJArray = self.piArray[i][j];
        #print("[TranslatorTContainer::get] piIJArray = %s" % (str(piIJArray)));
        if(not piIJArray.has_key(X)):
            print("[TranslatorTContainer::get] Error: X dimension is wrong. Asked for '%s'to get under (%d,%d) location but it is not stored there" % (X, i, j));            
            return None;
        return piIJArray[X];
        
    def getPi(self, i, j, X):
        piContent = self.get(i, j, X);
        if(isinstance(piContent, TranslatorTContainer)):
            return None;
        return piContent.pi;
        
    def setPi(self, i, j, X, pi):
        piContent = self.get(i, j, X);
        if(isinstance(piContent, TranslatorTContainer)):
            return None;
        piContent.pi = pi;
        
    def create(self, i, j, X, val):
        ##if(i != j):
        ##    print("i=%d,j=%d" %(i,j));
        #print("[TranslatorTContainer::create] Pi(%d, %d, %s) requested" % (i, j, X));
        if(i<0 or i >= self.iSize):
            print("[TranslatorTContainer::create] Error: i dimension is wrong. Asked %d and max possible is: %d" % (i, self.iSize));
            raise Exception("[TranslatorTContainer::create] Error: i dimension is wrong. Asked %d and max possible is: %d" % (i, self.iSize));
            return None;
        if(j<0 or j >= self.jSize):
            print("[TranslatorTContainer::create] Error: j dimension is wrong. Asked %d and max possible is: %d (i=%d)" % (j, self.jSize, i));
            raise Exception("[TranslatorTContainer::create] Error: j dimension is wrong. Asked %d and max possible is: %d" % (j, self.iSize));
            return None;
        piIJArray = self.piArray[i][j];
        #print("[TranslatorTContainer::create] piIJArray = %s" % (str(piIJArray)));
        if(piIJArray.has_key(X)):
            print("[TranslatorTContainer::create] Error: X dimension is wrong. Asked for '%s'to create under (%d,%d) location but it is already stored there" % (X, i, j));            
            raise Exception("[TranslatorTContainer::create] Error: X dimension is wrong. Asked for '%s'to create under (%d,%d) location but it is already stored there" % (X, i, j))
            return None;
        piIJArray[X] = val;
        return val;
        
    def delete(self, i, j, X):
        #print("[TranslatorTContainer::delete] Pi(%d, %d, %s) requested" % (i, j, X));
        if(i<0 or i >= self.iSize):
            print("[TranslatorTContainer::delete] Error: i dimension is wrong. Asked %d and max possible is: %d" % (i, self.iSize));
            return None;
        if(j<0 or j >= self.jSize):
            print("[TranslatorTContainer::delete] Error: j dimension is wrong. Asked %d and max possible is: %d" % (j, self.jSize));
            return None;
        piIJArray = self.piArray[i][j];
        #print("[TranslatorTContainer::delete] piIJArray = %s" % (str(piIJArray)));
        if(not piIJArray.has_key(X)):
            print("[TranslatorTContainer::delete] Error: X dimension is wrong. Asked for '%s' to delete under (%d,%d) location but it is not stored there" % (X, i, j));            
            return None;
        val = piIJArray[X];
        del piIJArray[X];
        return val;
        
    def set(self, i, j, X, val):
        #print("[TranslatorTContainer::set] Pi(%d, %d, %s) requested" % (i, j, X));
        if(i<0 or i >= self.iSize):
            print("[TranslatorTContainer::set] Error: i dimension is wrong. Asked %d and max possible is: %d" % (i, self.iSize));
            return None;
        if(j<0 or j >= self.jSize):
            print("[TranslatorTContainer::set] Error: j dimension is wrong. Asked %d and max possible is: %d" % (j, self.jSize));
            return None;
        piIJArray = self.piArray[i][j];
        #print("[TranslatorTContainer::set] piIJArray = %s" % (str(piIJArray)));
        if(not piIJArray.has_key(X)):
            print("[TranslatorTContainer::set] Error: X dimension is wrong. Asked for '%s'to set under (%d,%d) location but it is not stored there" % (X, i, j));            
            return None;
        piIJArray[X] = val;
        return val;        