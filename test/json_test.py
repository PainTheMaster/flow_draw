import unittest
import json
import flow_draw.data_io.json_io as json_io
from flow_draw.data_io.json_io import Primitive, Array, Objason
import flow_draw.data_io.flowsheet as fsht
import flow_draw.batch.process.unit_operations.uo_agitation as agit
import flow_draw.batch.process.unit_operations.unit_operation as uo
import flow_draw.trait_def.trait_def as trdef
import flow_draw.materials.materials as mats
import flow_draw.batch.process.unit_operations.uo_charging as chgng
import flow_draw.batch.process.unit_operations.uo_sampling as smplng
import flow_draw.batch.process.unit_operations.uo_cip as cip
import flow_draw.batch.process.unit_operations.uo_evaporation as evap
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

    def test_12001_agit_json(self):
        test_json:Objason = agit.Agitation.get_json_schema(caller=self)
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



class Test_21000_input_json(unittest.TestCase, trdef.GetMats):
    def setUp(self):
        flowsheet = fsht.Flowsheet()

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
        self.mats_df = mats.Materials.add_to_mats_df(mats_df=self.mats_df,
                                                     material="super cleaning solvet",
                                                     main_star=False,
                                                     density=0.789,
                                                     conc_assay=100.0,
                                                     remark="I'm a clenaing solvent")
        self.mats_inst = mats.Materials(self.mats_df)

        self.sampling = smplng.Sampling(flowsheet=flowsheet, operation_seq=2, edit_comment="test sampling")
        self.agit_obj = agit.Agitation(flowsheet=flowsheet, operation_seq=3, edit_comment="test agit")
        self.chgng_obj = chgng.Charging(caller=self, flow_sheet=flowsheet, operation_seq=4, edit_comment="test charging")
        self.cip_obj = cip.CIP(caller=self, flowsheet=flowsheet, operation_seq=5, edit_comment="Example edit comment for CIP")
        self.evap_obj = evap.Evaporation(caller=self, flowsheet=flowsheet, operation_seq=6, edit_comment="test evaporation")
        return super().setUp()
    
    def get_mats(self) -> mats.Materials:
        return self.mats_inst

    def test_21000_sampling_json_read(self):
        json_str:str ="""
                    {
                    "Seq_Nr": 3,
                    "Unit_Operation": "sampling",
                    "Edit_Comment": "Added IPC criterion for conversion.",
                    "Pre-comment": "Collect samples before proceeding to the next step.",
                    "Post-comment": "Record results in the batch record.",
                    "json_array_samples": [
                        {
                        "Sample_Name": "Reaction Mixture",
                        "Category": "Both",
                        "json_arr_monit": [
                            {
                            "Monit_Item_High_Level": "Residual Solvent",
                            "json_array_monit_items": [
                                {
                                "Monit_Rec_Title": "THF",
                                "Monit_Rec_Unit": "ppm"
                                },
                                {
                                "Monit_Rec_Title": "EtOH",
                                "Monit_Rec_Unit": "ppm"
                                }
                            ]
                            },
                            {
                            "Monit_Item_High_Level": "Purity",
                            "json_array_monit_items": [
                                {
                                "Monit_Rec_Title": "HPLC Purity",
                                "Monit_Rec_Unit": "%"
                                }
                            ]
                            }
                        ],
                        "json_array_ipc_items": [
                            {
                            "IPC_Rec_Title": "Conversion",
                            "IPC_Rec_Unit": "%",
                            "IPC_Criteria": ">=99.5"
                            },
                            {
                            "IPC_Rec_Title": "Impurity A",
                            "IPC_Rec_Unit": "%",
                            "IPC_Criteria": "<=0.20"
                            }
                        ]
                        },
                        {
                        "Sample_Name": "Filtrate",
                        "Category": "Monitoring",
                        "json_arr_monit": [
                            {
                            "Monit_Item_High_Level": "Appearance",
                            "json_array_monit_items": [
                                {
                                "Monit_Rec_Title": "Color",
                                "Monit_Rec_Unit": null
                                }
                            ]
                            }
                        ],
                        "json_array_ipc_items": null
                        },
                        {
                        "Sample_Name": "Wet Cake",
                        "Category": "IPC",
                        "json_arr_monit": null,
                        "json_array_ipc_items": [
                            {
                            "IPC_Rec_Title": "Moisture",
                            "IPC_Rec_Unit": "%",
                            "IPC_Criteria": "<=5.0"
                            }
                        ]
                        }
                    ]
                    }

        """
        json_obj = json.loads(json_str)
        print()
        print("==================")
        print(json_obj)
        print("==================")
        self.sampling.load_from_json_dict(json_obj)
        print(f'operation_seq: {self.sampling.operation_seq}')
        print(f'edit_comment: {self.sampling.edit_comment}')
        print(f'pre_comment: {self.sampling.pre_comment}')
        print(f'post_comment: {self.sampling.post_comment}')
        print("--------------------")
        print(f'len(self.list_samples): {len(self.sampling.list_samples)}')
        for sample in self.sampling.list_samples:
            print("--------------------")
            print(f'sample_seq: {sample.sample_seq}')
            print(f'name: {sample.name}')
            print(f'category: {sample.category}')
            print(f'content_ipc_criteria: {sample.content_ipc_criteria}')
            print(f'content_monit_items: {sample.content_monit_items}')
            print(f'rec_ipc_item_name: {sample.rec_ipc_item_name}')
            print(f'rec_ipc_unit: {sample.rec_ipc_unit}')
            print(f'rec_monit_item_name: {sample.rec_monit_item_name}')
            print(f'rec_monit_unit: {sample.rec_monit_unit}')
            print(f'sample_comment: {sample.sample_comment}')
            print("--------------------")

        self.assertTrue(True)


    def test_21001_agitation_json_read(self):
        json_str:str ="""
            {
                "Seq_Nr": 1,
                "Unit_Operation": "agitation",
                "Edit_Comment": null,
                "Pre-comment": "Maintain homogeneous suspension.",
                "Post-comment": "Confirm dissolution before proceeding.",
                "Specification": "Specific RPM",
                "Rotation_(rpm)": 250,
                "Ti_min_(deg-C)": 20.0,
                "Ti_max_(deg-C)": 25.0,
                "Minimum_time": 30,
                "Maximum_time": 60,
                "Time_unit": "min",
                "Dissolution_check": "Yes"
            }
        """
        json_obj = json.loads(json_str)
        print()
        print("==================")
        print(json_obj)
        print("==================")
        self.agit_obj.load_from_json_dict(json_obj)
        print(f'operation_seq: {self.agit_obj.operation_seq}')
        print(f'edit_comment: {self.agit_obj.edit_comment}')
        print(f'pre_comment: {self.agit_obj.pre_comment}')
        print(f'post_comment: {self.agit_obj.post_comment}')
        print()
        print(f'spec_agit: {self.agit_obj.spec_agit}')
        print(f'rpm: {self.agit_obj.rpm}')
        print(f'Ti_min: {self.agit_obj.Ti_min}')
        print(f'Ti_max: {self.agit_obj.Ti_max}')
        print(f'time_min: {self.agit_obj.time_min}')
        print(f'time_max: {self.agit_obj.time_max}')
        print(f'time_unit: {self.agit_obj.time_unit}')
        print(f'dissolution_check: {self.agit_obj.dissolution_check}')

        self.assertTrue(True)
    
    def test_21002_charging_json_read(self):
        json_str:str ="""
            {
                "Seq_Nr": 2,
                "Unit_Operation": "charging",
                "Edit_Comment": "test all constraints",
                "Pre-comment": "Slowly add reagent",
                "Post-comment": "Verify temperature remains stable",
                "arr_charging_input_entry": [
                    {
                    "Material_Name": "test mat 1",
                    "Metrics_Value": 1.0,
                    "Metrics_Unit": "equiv",
                    "Permissible_Error(%)": 1.0,
                    "Charging_Method": "powder_port",
                    "Time_Control": "Time_control_with_minimum_and_maximum",
                    "Minimum_Time(min)": 15,
                    "Maximum_Time(min)": 30,
                    "Temp_Control": "Temp_control_with_minimum_and_maximum",
                    "Minimum_Temp(deg-C)": 20,
                    "Maximum_Temp(deg-C)": 25
                    },
                    {
                    "Material_Name": "test mat 2",
                    "Metrics_Value": 2.5,
                    "Metrics_Unit": "v/w",
                    "Permissible_Error(%)": 5.0,
                    "Charging_Method": "press_vessel",
                    "Time_Control": "Time_control_with_maximum",
                    "Minimum_Time(min)": null,
                    "Maximum_Time(min)": 10,
                    "Temp_Control": "Temp_control_with_maximum",
                    "Minimum_Temp(deg-C)": null,
                    "Maximum_Temp(deg-C)": 30
                    }
                ]
            }
        """
        json_obj = json.loads(json_str)
        print()
        print("==================")
        print(json_obj)
        print("==================")
        self.chgng_obj.load_from_json_dict(json_obj)
        print(f'operation_seq: {self.chgng_obj.operation_seq}')
        print(f'edit_comment: {self.chgng_obj.edit_comment}')
        print(f'pre_comment: {self.chgng_obj.pre_comment}')
        print(f'post_comment: {self.chgng_obj.post_comment}')
        print()
        for charging in self.chgng_obj.inputs:
            print('---------------------')
            print(f'material_name: {charging.material_name}')
            print(f'metrics_unit: {charging.metrics_unit}')
            print(f'metrics_val: {charging.metrics_val}')
            print(f'error_pct: {charging.error_pct}')
            print(f'qty_kg: {charging.qty_kg}')
            print(f'error_kg: {charging.error_kg}')
            print(f'method: {charging.method}')
            print(f'time_control: {charging.time_control}')
            print(f'time_min: {charging.time_min}')
            print(f'time_max: {charging.time_max}')
            print(f'temp_control: {charging.temp_control}')
            print(f'temp_min: {charging.temp_min}')
            print(f'temp_max: {charging.temp_max}')

        self.assertTrue(True)

    def test_21003_cip_json_out(self):
        json_schema:Objason = cip.CIP.get_json_schema(caller=self)
        output=json_schema.asType()
        for line in output:
            print(line)

    def test_21004_cip_json_read(self):
        str_json = """
                {
                    "Seq_Nr": 5,
                    "Unit_Operation": "cip",
                    "Edit_Comment": "Cleaning after batch completion",
                    "Pre-comment": "Flush system before cleaning",
                    "Post-comment": "Verify cleanliness before next operation",
                    "arr_unit_cip": [
                        {
                        "CIP_target": "reaction vessel",
                        "Cleaning_solvent": "super cleaning solvet",
                        "solvent_QTY_(kg)": 250,
                        "Via": "filter dryer"
                        },
                        {
                        "CIP_target": "filter dryer",
                        "Cleaning_solvent": "test mat 2",
                        "solvent_QTY_(kg)": 75.5,
                        "Via": null
                        }
                    ]
                }
                """
        json_dict = json.loads(str_json)
        print()
        print("=================")
        print(json_dict)
        print("=================")

        self.cip_obj.load_from_json_dict(json_dict=json_dict)
        print(f'operation_seq: {self.cip_obj.operation_seq}')
        print(f'edit_comment: {self.cip_obj.edit_comment}')
        print(f'pre_comment: {self.cip_obj.pre_comment}')
        print(f'post_comment: {self.cip_obj.post_comment}')
        for unit_cp in self.cip_obj.cip_operations:
            print('------------------')
            print(f'target: {unit_cp.target}')
            print(f'solvent: {unit_cp.solvent}')
            print(f'qty_kg: {unit_cp.qty_kg}')
            print(f'via: {unit_cp.via}')
            print('------------------')

    def test_21005_evaporation_json_out(self):
        json_schema:Objason = evap.Evaporation.get_json_schema(caller=self)
        output=json_schema.asType()
        for line in output:
            print(line)

    def test_21006_evaporation_json_read(self):
        str_json = """{
                        "Tj_min": 40,
                        "Tj_max": 60,
                        "Condenser_brine_temp_min": -10,
                        "Condenser_brine_temp_max": 0,
                        "Pressure_control": "Specific_pressure",
                        "Press_min": 20,
                        "Press_max": 50,
                        "Press_unit": "kPaA",
                        "Agitation_spec": "Specific_RPM",
                        "Agitation(rpm)": 150,
                        "End_spec_min(v/w)": 0.8,
                        "End_spec_max(v/w)": 1.0,
                        "End_guideline_min(v/w)": null,
                        "End_guideline_max(v/w)": null
                    }"""
        json_dict = json.loads(str_json)
        print()
        print("=================")
        print(json_dict)
        print("=================")
        #evap_obj = evap.Evaporation(caller=self, flowsheet=self.flowsheet, operation_seq=1, edit_comment="test evaporation")
        self.evap_obj.load_from_json_dict(json_dict=json_dict)
        print(f'operation_seq: {self.evap_obj.operation_seq}')
        print(f'edit_comment: {self.evap_obj.edit_comment}')
        print(f'Tj_min: {self.evap_obj.Tj_min}')
        print(f'Tj_max: {self.evap_obj.Tj_max}')
        print(f'Tbr_min: {self.evap_obj.Tbr_min}')
        print(f'Tbr_max: {self.evap_obj.Tbr_max}')
        print(f'P_ctrl: {self.evap_obj.P_ctrl}')
        print(f'P_min: {self.evap_obj.P_min}')
        print(f'P_max: {self.evap_obj.P_max}')
        print(f'P_unit: {self.evap_obj.P_unit}')
        print(f'agit_spec: {self.evap_obj.agit_spec}')
        print(f'agit_rpm: {self.evap_obj.agit_rpm}')
        print(f'end_vw_spec_min: {self.evap_obj.end_vw_spec_min}')
        print(f'end_vw_spec_max: {self.evap_obj.end_vw_spec_max}')
        print(f'end_vw_guide_min: {self.evap_obj.end_vw_guide_min}')
        print(f'end_vw_guide_max: {self.evap_obj.end_vw_guide_max}')

def suite_json_test():
    suite = unittest.TestSuite()
    #suite.addTest(TestIO_00000_basic_func('test_0000_singleprop'))
    #suite.addTest(Test_10000_unit_ops('test_10000_charging_json'))
    #suite.addTest(TestIO_00000_basic_func('test_uo_agitation'))
    #suite.addTest(Test_10000_unit_ops("test_12000_cip_json"))
    #suite.addTest(Test_10000_unit_ops("test_10000_charging_json"))
    #suite.addTest(Test_20000_proc_json("test_20000_proc_comp_json"))
    #suite.addTest(Test_10000_unit_ops("test_12001_agit_json"))
    # suite.addTest(Test_21000_input_json("test_21000_sampling_json_read"))
    #suite.addTest(Test_21000_input_json("test_21001_agitation_json_read"))
    #suite.addTest(Test_21000_input_json("test_21002_charging_json_read"))
    #suite.addTest(Test_21000_input_json("test_21004_cip_json_read"))
    #suite.addTest(Test_21000_input_json("test_21005_evaporation_json_out"))
    suite.addTest(Test_21000_input_json("test_21006_evaporation_json_read"))
    return suite
            


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite_json_test())
