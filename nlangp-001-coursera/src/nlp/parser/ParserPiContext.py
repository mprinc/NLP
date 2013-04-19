# Necessary to avoid rounding on integer numbers
from __future__ import division
from nlp.parser.ParserRule import ParserRule

class ParserPiContext(object):
    def __init__(self):
        self.rule = ParserRule();
        self.rule = None;
        self.pi = -1.0;
        self.s = -1;
        
    def __str__(self):
        rule = self.rule;
        if(not isinstance(rule, ParserRule)):
            rule = ("Very strange, rule is not of type ParserRule, but %s, value is: %s" % (rule.__class__.__name__, str(rule)));
        return ("pi:%e, s:%d, rule:(%s)" % (self.pi, self.s, rule));