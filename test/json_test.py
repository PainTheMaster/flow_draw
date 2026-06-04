import unittest
import flow_draw.data_io.json_io as json_io


class TestIO(unittest.TestCase):
    def test_singleprop(self):
        inner1 = json_io.JSONentry(property_name="inner prop 1",
                                      data_type="string",
                                      description="this is an inner property")
        output=inner1.toJSON()
        for line in output:
            print(line)

        inner2 = json_io.JSONentry(property_name='inner prop 2',
                                   data_type='integer',
                                   enum_opt=[1, 2, 3, 4, 5],
                                   description='selection from a list of option'
                                   )
        output = inner2.toJSON()
        for line in output:
            print(line)
        self.assertTrue(True)

        
    
            


if __name__ == "__main__":
    unittest.main()