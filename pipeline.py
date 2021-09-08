import sys
import traceback
import time
from enum import Enum
import yaml

## @brief The config file to load the dynamic Pipeline from
#
config = "pipeline.YAML"

## @brief Map of declared global Object instances in `pipeline.YAML`
#
INSTANCES = dict()
## @brief Map of declared global Variables in `pipeline.YAML`
#
VARS = dict()

def parseYAML(file ="pipeline.YAML", callback=None):
    '''!
    @brief parse a YAML file
    
    @param file path to the YAML file to read from
    @param callback callback function to be executed on the error, if an error occurs
    @except YAMLERROR triggers error on malformed/unsafe YAML
    @returns dict : the parsed contents of the file or None if could not be parsed
    '''
    res = None
    with open(file, 'r') as stream:
        try:
            res = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            if callback is None:
                print(exc)
            else:
                callback(exc)

    return res

class PipelineTracker:
    '''!
    @brief Tracks pipeline status for a given Pipeline Artifact

    Stored alongside a Pipeline Artifact in Pipeline class' Pipeline::exec
    @see Pipeline::exec
    '''
    def __init__(self):
        '''
        @brief Constructor for Pipeline Trakcer
        '''
        self.return_value = None
        self.exec = None
        self.malformed = False
    
    def getReturnValue(self):
        '''!
        @brief Gets the return value of the associated Artifact stored in this tracker
        @see Pipeline::exec
        '''
        return self.return_value
    
    def getExecStatus(self):
        '''!
        @brief Gets the exec status of this tracker
        '''
        return self.exec
    
    def getMalformed(self):
        '''!
        @brief Gets whether or not the associated Artifact is malformed
        '''
        return self.malformed

    def setReturnValue(self, value):
        '''!
        @brief Sets the return value from the associated Artifact 
        
        @param value: the return value of the associated Artifact
        '''
        self.return_value = value
    
    def setExecStatus(self, exec):
        '''!
        @brief Sets the exec status of the associated Artifact of this tracker

        @param exec the exec status of the associated Artifact of this tracker
        '''
        self.exec = exec
    
    def setMalformed(self, malformed):
        '''!
        @brief Sets whether or not associated Artifact is Malformed

        @param malformed : boolean representing whether or not the artifact is malformed
        '''
        self.malformed = malformed


class PipelineStatus(Enum):
    '''!
    @brief enumerator class for all of dynamic pipeline return statuses
    '''
    OK = 0
    WARNING = 1
    CRITICAL = 2

    def __repr__(self):
        '''!
        @brief String representation of the PipelineStatus
        @returns str : string representation of Pipeline status
        '''
        if self.value == 0 : return "Successful!"
        if self.value == 1 : return "Executed with warnings."
        if self.value == 2 : return "Failed!"

        return "Placeholder status"

    def __str__(self):
        '''!
        @brief String Conversion of the Pipeline Status
        @returns str : string conversion of Pipeline status
        '''
        return repr(self)
    
    def out(self):
        '''!
        @brief Output some string representation of the PipelineStatus
        '''
        return repr(self)

class Artifact:
    '''!
    @brief An Artifact represents a unitary workload to be executed by the 
    Pipeline
    '''

    def __init__(self, procs = [], background = False, *args):
        '''!
        @brief Constructor of a Pipeline Artifact
        
        @param procs : List of string representations of processes declared in config file
        @param background : whether or not it is a background process
        @param args: optional args to be passed to some procs
        '''
        self.status = PipelineTracker()
    
    def execute(self):
        '''!
        @brief Execute the processes of the Artifact
        '''
        pass
    
    def compile():
        '''!
        @brief 'Compile' the shell, module, or dynamic python code declared in the
        config file for this Artifact
        '''


    def compilePython(code):
        '''!
        @brief Loads dynamic string representing python code into python executable code

        This is the function that is used to load/execute strings `python`/`py`/`python3`/`py3`
        tags in the pipeline.YAML config file
        @param code str
        '''
    
    def compileShell(code):
        '''!
        @brief Loads dynamic string representation of shell code into python executable code
        '''

class ConcurrentArtifact(Artifact):
    '''!
    @brief A Concurrent Artifact represents a parallelized - concurrent workload
    to be executed by the Pipeline
    '''

    def __init__(self, procs = [], background = False, *args):
        '''!
        @brief  Constructor of a Pipeline Concurrent Artifact

        @param procs : List of string representations of processes declared in config file
        @param background : whether or not it is a background process
        @param args: optional args to be passed to some procs
        '''
        super.__init__(self, procs = [], background = False, *args)
        

    def execute(self):
        '''!
        @brief Execute the concurrent processes of the Artifact
        '''
        # Method must be overloaded from parent
        pass


class Pipeline:
    '''!
    @brief Dynamic python automation pipeline object


    Organizes the execution of the YAML config file into 'Artifacts'
    which can be regular or multi-threaded workloads
    '''

    def __init__(self):
        '''!
        @brief Pipeline constructor
        '''
        ## @brief Controls whether or not the output of the pipeline is mirrored in stdout
        #
        self.verbose = False
        ## @brief Start time of the pipeline
        #
        self.startTime = str(time.time())
        ## @brief Output log name
        #
        self.outputLog = 'pipeline_' + self.startTime + '.log' 
        ## @brief Map of background processes: proc name -> List[compiled py/shell code]
        #
        self.backgroundProcs = dict() 
        ## @brief zipped list of pipeline artifacts and their associated trackers
        #
        self._exec = [] # zipped list of artifacts and their Pipeline Tracker

    
    def write_log(self, msg):
        '''!
        @brief Wrapper for writing pipeline output to a log
        '''
        if(not self.logfile):
            self.logfile = 'pipeline_' + self.startTime + '.log'
        
        msg = str(msg)
        f_log = open(self.logfile, 'a')
        f_log.write(msg)
        if self.verbose : print(msg)
        f_log.close()
    
    def log(func, *args):
        '''!
        @brief Logging/error handling decorator for pipeline methods
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
        '''!
        @brief Loads a pipeline to execute from a YAML file called 'pipeline.YAML' by default
        but this can be overriden when you construct the actual Pipeline.

        @throws yaml.YAMLError : if the .YAML file is malformed
        @returns dict: dict loaded 
        '''
        

    def _constructPipeline(self):
        '''!
        @brief load and form the pipeline after loading the YAML config file
        '''
    
    
    