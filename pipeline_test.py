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

    def testPipelineStatus(self):
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

if __name__ == "__main__":
    unittest.main()