# Necessary to avoid rounding on integer numbers
from __future__ import division

class ParserRule(object):
    TYPE_UNKNOWN = 0;
    TYPE_UNARY = 1;
    TYPE_BINARY = 2;

    def __init__(self):
        self.type = ParserRule.TYPE_UNKNOWN;
        self.weight = None;
        self.X = None;

        # binary
        self.Y = None;
        self.Z = None;

        # unary
        self.terminal = None;

    def __str__(self):
        if(self.type == ParserRule.TYPE_UNARY):
            return ("UNARY rule: X:'%s', terminal:'%s', weight:%s" % (self.X, self.terminal, str(self.weight)));
        elif(self.type == ParserRule.TYPE_BINARY):
            return ("BINARY rule: X:'%s', Y:'%s', Z:'%s', weight:%e" % (self.X, self.Y, self.Z, self.weight));
        else:
            return ("UNKNOWN TYPE rule: X:'%s', Y:'%s', Z:'%s', terminal:'%s', weight:%s" % (str(self.X), str(self.Y), str(self.Z), str(self.terminal), str(self.weight)));
        