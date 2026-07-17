import unittest
import flow_draw.data_io.json_io as json_io
from flow_draw.data_io.json_io import Primitive, Array, Objason
import flow_draw.batch.process.unit_operations.uo_agitation as agit
import flow_draw.batch.process.unit_operations.unit_operation as uo
import flow_draw.trait_def.trait_def as trdef
import flow_draw.materials.materials as mats
import flow_draw.batch.process.unit_operations.uo_charging as chgng
import flow_draw.batch.process.unit_operations.uo_sampling as smplng
import flow_draw.batch.process.unit_operations.uo_cip as cip
import flow_draw.data_io.process_io as pio


class TestIO_00000_basic_func(unittest.TestCase):
    def test_0000_singleprop(self):
        print('--------------------')
        inner1 = json_io.Primitive(prim_type='string',
                                   key='primitive_1',
                                   description='description for inner 1',
                                   nullable=True)
        output = inner1.asEntity()
        for line in output:
            print(line)
        print('--------------------')
        inner2 = json_io.Primitive(prim_type='string',
                                   key='primitive_2',
                                   enum=['enum1', 'enum2', 'enum3'],
                                   description='description for inner 2')
        output = inner2.asEntity()
        for line in output:
            print(line)
        print('--------------------')
        inner3 = json_io.Primitive(prim_type="number",
                                   key='primitive_3',
                                   enum=[3.14, 2.718, 0.0],
                                   description='description for inner 3')
        output = inner3.asEntity()
        for line in output:
            print(line)
        print('--------------------')
        inner4 = json_io.Primitive(prim_type='integer',
                                   key='primitive_4',
                                   const=5,
                                   description='description for inner 4')
        output = inner4.asEntity()
        for line in output:
            print(line)
        print('--------------------')
        inner5 = json_io.Primitive(prim_type='string',
                                   key='primitive_5',
                                   const='const 5',
                                   description='description for inner 5')
        output = inner5.asEntity()
        for line in output:
            print(line)
        print('--------------------')
        arr = json_io.Array(key='test_array',
                            description='array for test',
                            content=[inner1, inner2, inner3, inner4, inner5])
        output = arr.asEntity()
        for line in output:
            print(line)
        print('--------------------')
        arr2 = json_io.Array(key='test_array_2',
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
        obj = json_io.Objason(key='test_if_then_else',
                              props=[inner1],
                              description="Test object for if-then-else")
        obj.if_then_else(prop=inner1.key,
                         val_if=['にく', 'やさい'],
                         props_then=[inner2],
                         props_else=[inner3])
        output = obj.asType()
        for line in output:
            print(line)
        print('--------------------')       

        obj = json_io.Tuple(key='tuple_test',
                            content=[inner1, inner2, inner3],
                            description='I am a tuple.')
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






class Test_10000_unit_ops(unittest.TestCase, trdef.GetMats):
    def setUp(self):
        self.mats_df = mats.Materials.generate_mats_df()
        self.mats_df = mats.Materials.add_to_mats_df(mats_df=self.mats_df,
                                                       material="test mat 1",
                                                       main_star=True,
                                                       mw = 18.01,
                                                       density=1.00,
                                                       conc_assay=99.999,
                                                       kg_main=2.00,
                                                       remark="Actually, I'm water.")
        self.mats_df = mats.Materials.add_to_mats_df(mats_df=self.mats_df,
                                                       material="test mat 2",
                                                       main_star=False,
                                                       mw = 46.07,
                                                       density=0.789,
                                                       conc_assay=94.0,
                                                       remark="Actually, I'm ethanol.")
        self.mats_inst = mats.Materials(self.mats_df)
        return super().setUp()
    
    def get_mats(self) -> mats.Materials:
        return self.mats_inst
    
    def test_10000_charging_json(self):
        test_json:Objason = chgng.Charging.get_json_schema(caller=self)
        list_str_json = test_json.asType()
        print()
        print('----------------------')
        for line in list_str_json:
            print(line)
        print('----------------------')
        self.assertTrue(True)

    def test_11000_sampling_json(self):
        test_json:Objason = smplng.Sampling.get_json_schema(caller=self)
        list_str_json = test_json.asType()
        print()
        print('----------------------')
        for line in list_str_json:
            print(line)
        print('----------------------')
        self.assertTrue(True)

    def test_12000_cip_json(self):
        test_json:Objason = cip.CIP.get_json_schema(caller=self)
        list_str_json = test_json.asType()
        print()
        print('----------------------')
        for line in list_str_json:
            print(line)
        print('----------------------')
        self.assertTrue(True)


    

class Test_20000_proc_json(unittest.TestCase, trdef.GetMats):
    def setUp(self):
        self.mats_df = mats.Materials.generate_mats_df()
        self.mats_df = mats.Materials.add_to_mats_df(mats_df=self.mats_df,
                                                       material="test mat 1",
                                                       main_star=True,
                                                       mw = 18.01,
                                                       density=1.00,
                                                       conc_assay=99.999,
                                                       kg_main=2.00,
                                                       remark="Actually, I'm water.")
        self.mats_df = mats.Materials.add_to_mats_df(mats_df=self.mats_df,
                                                       material="test mat 2",
                                                       main_star=False,
                                                       mw = 46.07,
                                                       density=0.789,
                                                       conc_assay=94.0,
                                                       remark="Actually, I'm ethanol.")
        self.mats_inst = mats.Materials(self.mats_df)
        return super().setUp()
    
    def get_mats(self) -> mats.Materials:
        return self.mats_inst

    def test_20000_proc_comp_json(self):
        list_ops: list[type[uo.UnitOperation]] = [chgng.Charging, agit.Agitation, cip.CIP, smplng.Sampling]
        inst_pio = pio.ProcessIO(batch_name="test_batch", process_name="test_process", num_unit_op=4)
        print()
        print("==========================")
        json_str = inst_pio.json_uo(caller=self, list_uo=list_ops)
        # print()
        # print("==========================")
        # print(json_str)
        print("==========================")
        print(f"len(json_str)=={len(json_str)}; {json_str.count('\n')} lines")
        
        print("==========================")

        self.assertTrue(True)







def suite_json_test():
    suite = unittest.TestSuite()
    #suite.addTest(TestIO_00000_basic_func('test_0000_singleprop'))
    #suite.addTest(Test_10000_unit_ops('test_10000_charging_json'))
    #suite.addTest(TestIO_00000_basic_func('test_uo_agitation'))
    #suite.addTest(Test_10000_unit_ops("test_12000_cip_json"))
    suite.addTest(Test_20000_proc_json("test_20000_proc_comp_json"))
    return suite
            


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite_json_test())
