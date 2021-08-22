import sys
import traceback
import time
from enum import Enum

def parseYAML():
    '''
    parse a YAML file
    '''

    return

class PipelineStatus(Enum):
    '''
    enumerator class for all of dynamic pipeline return statuses
    '''
    OK = 0
    WARNING = 1
    CRITICAL = 2

    def __repr__(self):
        '''
        
        '''
        pass

    def __str__(self):
        '''
        
        '''
        pass

class PipelineArtifact:
    '''

    '''

    def __init__(self):
        '''
        
        '''
        pass


class Pipeline:
    '''
    Dynamic pipeline:
        
    '''

    def __init__(self, verbose = True):
        '''
        Initialize a dynamic execution pipeline
        '''
        self.verbose = verbose
        self.startTime = str(time.time())
        self.outputLog = 'pipeline_' + self.startTime + '.log' 
    
    def write_log(self, msg):
        if(not self.logfile):
            self.logfile = 'pipeline_' + self.startTime + '.log'
        
        msg = str(msg)
        f_log = open(self.logfile, 'a')
        f_log.write(msg)
        if self.verbose : print(msg)
        f_log.close()
    
    def log(func, *args):
        '''
        Decorator for pipeline methods
        '''
        def wrap(self, *args):
            '''
            Wrapper that his this object as a scope
            '''
            def new_func(*args, **kwargs):
                '''
                Modified function call
                '''
                try:
                    res = func(*args, **kwargs)
                    if res : self.write_log(res)
                    return res
                except:
                    e = sys.exc_info()
                    self.write_log('\t' + 'Failed : ')
                    self.write_log('\t\t' + repr(e))
                    self.write_log('\t\t' + traceback.format_exc())
        

    def Load_from_YAML(self):
        '''
        Loads a pipeline to execute from a YAML file

        '''
        try:
            f = open('./pipeline.YAML')
        except:
            e = sys.exc_info()

            sys.exit()
            pass
        pass