import unittest
import importlib
import pipeline


class TestPipeline(unittest.TestCase):
    def test_parseYAML(self):
        #empty YAML
        res = pipeline.parseYAML("tests/test0.yaml")
        assert(res is None)
        #single map YAML
        res = pipeline.parseYAML("tests/test1.yaml")
        assert(type(res) == dict)
        assert(type(res['hello-world']) == bool)
        assert(res['hello-world'] == True)

        #single list YAML
        res = pipeline.parseYAML("tests/test2.yaml")
        assert(type(res) == dict)
        assert(type(res['sample-list']) == list)
        assert(len(res['sample-list']) == 3)
        assert(res['sample-list'] == ["one", "two", "three"])

        res = pipeline.parseYAML("tests/test3.yaml")
        assert(type(res) == dict)
        assert(type(res['sample-nested-list']['one']) == list and type(res['sample-nested-list']['two']) == list)
        assert(res['hello-world'] == 'octo')
        assert(res['sample-nested-list']['one'] == ['uno', 'dos', 'tres'])
        assert(res['sample-nested-list']['two'] == ['quatro', 'cinqo', 'sixte'])
        

if __name__ == "__main__":
    unittest.main()