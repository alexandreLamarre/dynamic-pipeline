import unittest
import importlib
import pipeline

class TestPipeline(unittest.TestCase):
    def test_parseYAML(self):
        '''!
        @brief Tests parse .YAML file method pipeline.parseYAML
        '''
        #empty YAML
        res = pipeline.parseYAML("tests/parseYAML/test0.YAML")
        assert(res is None)
        #single map YAML
        res = pipeline.parseYAML("tests/parseYAML/test1.YAML")
        assert(type(res) == dict)
        assert(type(res['hello-world']) == bool)
        assert(res['hello-world'] == True)

        #single list YAML
        res = pipeline.parseYAML("tests/parseYAML/test2.YAML")
        assert(type(res) == dict)
        assert(type(res['sample-list']) == list)
        assert(len(res['sample-list']) == 3)
        assert(res['sample-list'] == ["one", "two", "three"])

        res = pipeline.parseYAML("tests/parseYAML/test3.YAML")
        assert(type(res) == dict)
        assert(type(res['sample-nested-list']['one']) == list and type(res['sample-nested-list']['two']) == list)
        assert(res['hello-world'] == 'octo')
        assert(res['sample-nested-list']['one'] == ['uno', 'dos', 'tres'])
        assert(res['sample-nested-list']['two'] == ['quatro', 'cinqo', 'sixte'])

        res = pipeline.parseYAML("tests/parseYAML/test4.YAML")
        assert(res['piped-input'] == '\' def hello(): print("Hello world!") hello() \'')  

        res = pipeline.parseYAML("tests/parseYAML/test5.YAML")
        assert(res['empty'] is None)
        assert(res['empty2'] is None)

    def testPipelineStatus(self):
        '''!
        @brief Tests PipelineStatus Object
        '''
        pipeStat = pipeline.PipelineStatus(0)
        assert(pipeStat== pipeline.PipelineStatus.OK)
        assert(repr(pipeStat) == "Successful!")
        assert(repr(pipeStat) == str(pipeStat) and str(pipeStat) == pipeStat.out())

        pipeStat = pipeline.PipelineStatus(1)
        assert(pipeStat == pipeline.PipelineStatus.WARNING)
        assert(repr(pipeStat) == "Executed with warnings.")
        assert(repr(pipeStat) == str(pipeStat) and str(pipeStat) == pipeStat.out())

        pipeStat = pipeline.PipelineStatus(2)
        assert(pipeStat == pipeline.PipelineStatus.CRITICAL)
        assert(repr(pipeStat) == "Failed!")
        assert(repr(pipeStat) == str(pipeStat) and str(pipeStat) == pipeStat.out())

    def testPipelineTracker(self):
        '''!
        @brief Tests PipelineTracker Object
        '''
        pipeTracker = pipeline.PipelineTracker()
        assert(pipeTracker.return_value is None)
        assert(pipeTracker.exec is None)
        assert(not pipeTracker.malformed)
        assert(pipeTracker.getReturnValue() is None)
        assert(pipeTracker.getExecStatus() is None)
        assert(not pipeTracker.getExecStatus())

        pipeTracker.setReturnValue(0)
        assert(pipeTracker.getReturnValue() == 0)
        pipeTracker.setExecStatus("Exited with status 0.")
        assert(pipeTracker.getExecStatus() == "Exited with status 0.")
        pipeTracker.setMalformed(True)
        assert(pipeTracker.getMalformed())
    
    def testMisc(self):
        '''!
        @brief test miscellanious python interactions
        '''
        code = '5'
        func = eval('lambda:' + code)
        res = func()
        assert(res == 5)
        # code = ("def hello():\n"
        #     '\treturn "Hello World!"\n'
        #     'print(hello())')
        # print(repr(code))
        # func = eval('lambda:' + code)


if __name__ == "__main__":
    unittest.main()