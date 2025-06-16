import argparse;import os;import sys
class options():
    def __init__(self):self.parser=argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter);self.initialized=False
    def initialize(self):self.initialized=True
    def getparse(self,test_flag=False):return self.opt if hasattr(self,'opt')else(self.initialize()or setattr(self,'opt',self.parser.parse_args())or self.opt)
#code may be free and open source, but it will cost your time :P
