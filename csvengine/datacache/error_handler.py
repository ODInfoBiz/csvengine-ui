'''
Created on Dec 14, 2015

@author: jumbrich
'''
from _collections import defaultdict
import traceback
class ErrorHandler():

    exceptions=defaultdict(long)

    DEBUG=True

    @classmethod
    def handleError(cls, log, msg=None, exception=None, **kwargs):
        name=type(exception).__name__
        cls.exceptions[name] +=1
        
        if ErrorHandler.DEBUG:
            print(traceback.format_exc())

        log.error(msg, exctype=type(exception), excmsg=exception.message, **kwargs)
    
    @classmethod
    def printStats(cls):
        if len(cls.exceptions)==0:
            print "No exceptions handled"
        else:
            print "\n -------------------------"
            print "  Numbers of Exceptions:"
            for exc, count in cls.exceptions.iteritems():
                print " ",exc, count
            print " -------------------------"