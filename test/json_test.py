import unittest
import flow_draw.data_io.json_io as json_io
import flow_draw.batch.process.unit_operations.uo_agitation as agit


class TestIO(unittest.TestCase):
    # def test_singleprop(self):
    #     print('--------------------')
    #     inner1 = json_io.JSONentry(property_name="inner prop 1",
    #                                   data_type="string",
    #                                   description="this is an inner property",
    #                                   required=True)
    #     output=inner1.toJSON()
    #     for line in output:
    #         print(line)
    #     print('--------------------')

    #     inner2 = json_io.JSONentry(property_name='inner prop 2',
    #                                data_type='integer',
    #                                enum_opt=[1, 2, 3, 4, 5],
    #                                description='selection from a list of option',
    #                                required=True
    #                                )
    #     output = inner2.toJSON()
    #     for line in output:
    #         print(line)
    #     self.assertTrue(True)
    #     print('--------------------')

    #     outer = json_io.JSONentry(property_name='outer',
    #                               data_type='object',
    #                               content=[inner1, inner2],
    #                               description='outer object')
    #     output = outer.toJSON()
    #     for line in output:
    #         print(line)
    #     print('--------------------')    

        
    #     arr_obj = json_io.JSONentry(property_name='arr of objects',
    #                                 data_type='array',
    #                                 content=outer,
    #                                 description='an array of objects',
    #                                 )
    #     output = arr_obj.toJSON()
    #     for line in output:
    #         print(line)
    #     print('--------------------')
    #     self.assertTrue(True)


    def test_singleprop(self):
        print('--------------------')
        inner1 = json_io.Primitive(prim_type='string',
                                   key='primitive 1',
                                   description='description for inner 1')
        output = inner1.asEntity()
        for line in output:
            print(line)
        print('--------------------')
        inner2 = json_io.Primitive(prim_type='string',
                                   key='primitive 2',
                                   enum=['enum1', 'enum2', 'enum3'],
                                   description='description for inner 2')
        output = inner2.asEntity()
        for line in output:
            print(line)
        print('--------------------')
        inner3 = json_io.Primitive(prim_type="number",
                                   key='primitive 3',
                                   enum=[3.14, 2.718, 0.0],
                                   description='description for inner 3')
        output = inner3.asEntity()
        for line in output:
            print(line)
        print('--------------------')
        inner4 = json_io.Primitive(prim_type='integer',
                                   key='primitive 4',
                                   const=5,
                                   description='description for inner 4')
        output = inner4.asEntity()
        for line in output:
            print(line)
        print('--------------------')
        inner5 = json_io.Primitive(prim_type='string',
                                   key='primitive 5',
                                   const='const 5',
                                   description='description for inner 5')
        output = inner5.asEntity()
        for line in output:
            print(line)
        print('--------------------')
        arr = json_io.Array(key='test array',
                            description='array for test',
                            content=[inner1, inner2, inner3, inner4, inner5])
        output = arr.asEntity()
        for line in output:
            print(line)
        print('--------------------')
        arr2 = json_io.Array(key='test array 2',
                            description='array for test',
                            content=inner1)
        output = arr2.asEntity()
        for line in output:
            print(line)
        print('--------------------')        
        obj = json_io.Objason(key='test obj',
                              props=[inner1, inner2, inner3, inner4, inner5, arr2],
                              description="description for object")
        output = obj.asEntity()
        for line in output:
            print(line)
        print('--------------------')                        

        self.assertTrue(True)

    def test_uo_agitation(self):
        json_agit = agit.Agitation.get_json_schema()
        for line in json_agit.asEntity():
            print(line)
        self.assertTrue(True)

        
def suite_json_test():
    suite = unittest.TestSuite()
    suite.addTest(TestIO('test_uo_agitation'))
    return suite
            


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite_json_test())
