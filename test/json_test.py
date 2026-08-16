import unittest
import json
import flow_draw.data_io.json_io as json_io
from flow_draw.data_io.json_io import Primitive, Array, Objason
import flow_draw.data_io.flowsheet as fsht
import flow_draw.batch.process.unit_operations.uo_agitation as agit
import flow_draw.batch.process.unit_operations.unit_operation as uo
import flow_draw.trait_def.trait_def as trdef

import flow_draw.batch.process.unit_operations.uo_charging as chgng
import flow_draw.batch.process.unit_operations.uo_sampling as smplng
import flow_draw.batch.process.unit_operations.uo_cip as cip
import flow_draw.batch.process.unit_operations.uo_evaporation as evap
import flow_draw.batch.process.unit_operations.uo_filtration as filt
import flow_draw.batch.process.unit_operations.uo_filter_setup as filtsup
import flow_draw.batch.process.unit_operations.uo_placeholder as plchldr
import flow_draw.batch.process.unit_operations.uo_inert_replacement as inert
import flow_draw.batch.process.unit_operations.uo_line_clearance as lnclear
import flow_draw.batch.process.unit_operations.uo_phase_discharge as phdisch
import flow_draw.batch.process.unit_operations.uo_temp_control as tempctrl
import flow_draw.batch.process.process as proc
import flow_draw.data_io.process_io as pio
import flow_draw.batch.process.unit_operations.uo_drying as drying
import json
from flow_draw.materials.materials import Materials as mats

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
        self.mats_df = mats.generate_mats_df()
        self.mats_df = mats.add_to_mats_df(mats_df=self.mats_df,
                                                       material="test mat 1",
                                                       main_star=True,
                                                       mw = 18.01,
                                                       density=1.00,
                                                       conc_assay=99.999,
                                                       kg_main=2.00,
                                                       remark="Actually, I'm water.")
        self.mats_df = mats.add_to_mats_df(mats_df=self.mats_df,
                                                       material="test mat 2",
                                                       main_star=False,
                                                       mw = 46.07,
                                                       density=0.789,
                                                       conc_assay=94.0,
                                                       remark="Actually, I'm ethanol.")
        self.mats_inst = mats(self.mats_df)
        return super().setUp()
    
    def get_mats(self) -> mats:
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
        self.mats_df = mats.generate_mats_df()
        self.mats_df = mats.add_to_mats_df(mats_df=self.mats_df,
                                                       material="test mat 1",
                                                       main_star=True,
                                                       mw = 18.01,
                                                       density=1.00,
                                                       conc_assay=99.999,
                                                       kg_main=2.00,
                                                       remark="Actually, I'm water.")
        self.mats_df = mats.add_to_mats_df(mats_df=self.mats_df,
                                                       material="test mat 2",
                                                       main_star=False,
                                                       mw = 46.07,
                                                       density=0.789,
                                                       conc_assay=94.0,
                                                       remark="Actually, I'm ethanol.")
        self.mats_inst = mats(self.mats_df)
        return super().setUp()
    
    def get_mats(self) -> mats:
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
        schema_obj = json.loads(json_str)
        print(type(schema_obj))
        print(schema_obj)
        print("==========================")

        self.assertTrue(True)



class Test_21000_input_json(unittest.TestCase, trdef.GetMats):
    def setUp(self):
        flowsheet = fsht.Flowsheet()

        self.mats_df = mats.generate_mats_df()
        self.mats_df = mats.add_to_mats_df(mats_df=self.mats_df,
                                                       material="test mat 1",
                                                       main_star=True,
                                                       mw = 18.01,
                                                       density=1.00,
                                                       conc_assay=99.999,
                                                       kg_main=2.00,
                                                       remark="Actually, I'm water.")
        self.mats_df = mats.add_to_mats_df(mats_df=self.mats_df,
                                                       material="test mat 2",
                                                       main_star=False,
                                                       mw = 46.07,
                                                       density=0.789,
                                                       conc_assay=94.0,
                                                       remark="Actually, I'm ethanol.")
        self.mats_df = mats.add_to_mats_df(mats_df=self.mats_df,
                                                     material="super cleaning solvet",
                                                     main_star=False,
                                                     density=0.789,
                                                     conc_assay=100.0,
                                                     remark="I'm a clenaing solvent")
        self.mats_inst = mats(self.mats_df)

        self.sampling = smplng.Sampling(flowsheet=flowsheet, operation_seq=2, edit_comment="test sampling")
        self.agit_obj = agit.Agitation(flowsheet=flowsheet, operation_seq=3, edit_comment="test agit")
        self.chgng_obj = chgng.Charging(caller=self, flowsheet=flowsheet, operation_seq=4, edit_comment="test charging")
        self.cip_obj = cip.CIP(caller=self, flowsheet=flowsheet, operation_seq=5, edit_comment="Example edit comment for CIP")
        self.evap_obj = evap.Evaporation(caller=self, flowsheet=flowsheet, operation_seq=6, edit_comment="test evaporation")
        self.filt_obj = filt.Filtration(caller=self, flowsheet=flowsheet, operation_seq=7, edit_comment='Test for filtration JSON I/O')
        self.filtsup_obj = filtsup.FiltSetup(caller=self, flowsheet=flowsheet, operation_seq=8, edit_comment='Test for filter setup JSON I/O')
        self.drying_obj = drying.Drying(caller=self, flowsheet=flowsheet, operation_seq=9, edit_comment='Test for drying JSON I/O')
        return super().setUp()
    
    def get_mats(self) -> mats:
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

        print(f'end_volume_spec_min: {self.evap_obj.end_volume_spec_min}')
        print(f'end_volume_spec_max: {self.evap_obj.end_volume_spec_max}')
        print(f'end_volume_guide_min: {self.evap_obj.end_volume_guide_min}')
        print(f'end_volume_guide_max: {self.evap_obj.end_volume_guide_max}')

    def test_21007_filtration_json_out(self):
        json_obj:Objason = filt.Filtration.get_json_schema(caller=self)
        json_str = json_obj.asType()
        for line in json_str:
            print(line)

    def test_21008_filtration_json_read(self):
        str_json = """{
                        "Seq_Nr": 3,
                        "Unit_Operation": "filtration",
                        "Edit_Comment": "Pressure range based on batch record.",
                        "Pre-comment": "Verify filter integrity before use.",
                        "Post-comment": "Record final filtrate volume.",
                        "Filtering Equipment": "Pall Supor EKV Filter",
                        "Tj set point": 20.0,
                        "Filt P_min": 50.0,
                        "Filt P_max": 150.0,
                        "Pressure Unit": "kPa",
                        "Need_integrity_test": true
                    }"""
        json_dict = json.loads(str_json)
        print()
        print("=================")
        print(json_dict)
        print("=================")
        self.filt_obj.load_from_json_dict(json_dict=json_dict)
        print(f'operation_seq: {self.filt_obj.operation_seq}')
        print(f'edit_comment: {self.filt_obj.edit_comment}')
        print(f'pre_comment: {self.filt_obj.pre_comment}')
        print(f'post_comment: {self.filt_obj.post_comment}')
        print(f'equipment: {self.filt_obj.equipment}')
        print(f'Tj_setpoint: {self.filt_obj.Tj_setpoint}')
        print(f'press_min: {self.filt_obj.press_min}')
        print(f'press_max: {self.filt_obj.press_max}')
        print(f'pressure_unit: {self.filt_obj.unit_press}')
        print(f'integ_test: {self.filt_obj.integ_test}')

    def test_21009_filter_setup_json_out(self):
        json_obj:Objason = filtsup.FiltSetup.get_json_schema(caller=self)
        json_str = json_obj.asType()
        for line in json_str:
            print(line)
        self.assertTrue(True)

    def test21010_filter_setup_json_read(self):
        str_json = """{
                    "Seq_Nr": 3,
                    "Unit_Operation": "filter_setup",
                    "Edit_Comment": null,
                    "Pre-comment": "ろ過機の組立前に、フィルタークロスの外観検査を実施すること。",
                    "Post-comment": null,
                    "Equipment": "F-201",
                    "Filter_cloth_type": "PPクロス（100メッシュ)",
                    "Number_cloth": 2,
                    "Bag_filter_type": "PPバグフィルター 5μm",
                    "App_press_leak_test": 0.2,
                    "Permiss_press_leak_test": 0.02,
                    "Time_leak_test": 10,
                    "Pressure_unit": "MPa"
                    }"""
        json_dict = json.loads(str_json)
        print()
        print("=================")
        print(json_dict)
        print("=================")
        self.filtsup_obj.load_from_json_dict(json_dict=json_dict)
        """
        FYI...
        def load_from_json_dict(self, json_dict: dict[str, any]):
            super().load_from_json_dict(json_dict)
            self.equip_id = json_dict[hedr_equip]
            self.filter_cloth_type = json_dict[hedr_filter_cloth]
            self.num_filter_cloths = json_dict[hedr_num_filter]
            self.bag_filter_type = json_dict[hedr_bag_filter]
            self.press_leak_test = json_dict[hedr_press_leak_test]
            self.press_drop_leak_test = json_dict[hedr_press_drop_leak_test]
            self.time_leak_test = json_dict[hedr_time_leak_test]
            self.unit_press = json_dict[hedr_press_unit]
        """

        print(f'operation_seq: {self.filtsup_obj.operation_seq}')
        print(f'edit_comment: {self.filtsup_obj.edit_comment}')
        print(f'pre_comment: {self.filtsup_obj.pre_comment}')
        print(f'post_comment: {self.filtsup_obj.post_comment}')
        print(f'equip_id: {self.filtsup_obj.equip_id}')
        print(f'filter_cloth_type: {self.filtsup_obj.filter_cloth_type}')
        print(f'num_filter_cloths: {self.filtsup_obj.num_filter_cloths}')
        print(f'bag_filter_type: {self.filtsup_obj.bag_filter_type}')
        print(f'press_leak_test: {self.filtsup_obj.press_leak_test}')
        print(f'press_drop_leak_test: {self.filtsup_obj.press_drop_leak_test}')
        print(f'time_leak_test: {self.filtsup_obj.time_leak_test}')
        print(f'unit_press: {self.filtsup_obj.unit_press}') 

        self.assertTrue(True)

    def test_21011_drying_json_out(self):
        json_obj:Objason = drying.Drying.get_json_schema(caller=self)
        json_str = json_obj.asType()
        for line in json_str:
            print(line)
        self.assertTrue(True)

    def test_21012_drying_json_read(self):
        str_json = """
        {
                        "Seq_Nr": 12,
                        "Unit_Operation": "drying",
                        "Edit_Comment": "Drying conditions taken from the flowsheet rev.3, section 4.2.",
                        "Pre-comment": "Confirm that the cake washing is complete and the mother liquor line is closed before starting the vacuum.",
                        "Post-comment": "Break the vacuum with nitrogen before discharging the dried product.",
                        "Tj_ctrl_cat": "Tj_ctrl_spec",
                        "Tj_low_drying": 40.0,
                        "Tj_high_drying": 50.0,
                        "Tbr_low": -20.0,
                        "Tbr_high": -10.0,
                        "mode_vac": "range",
                        "pres_low": 0.001,
                        "pres_high": 0.008,
                        "rpm_min": 1.0,
                        "rpm_max": 5.0,
                        "intermission_drying": "Yes",
                        "list_test_drying": [
                            {
                            "test_cat": "ipc",
                            "test_item": "Loss on drying",
                            "test_tgt_criterion": 0.5,
                            "test_unit": "%"
                            },
                            {
                            "test_cat": "ipc",
                            "test_item": "Residual n-hexane",
                            "test_tgt_criterion": 290,
                            "test_unit": "ppm"
                            },
                            {
                            "test_cat": "monit_with_tgt",
                            "test_item": "Water content (KF)",
                            "test_tgt_criterion": 0.2,
                            "test_unit": "%"
                            },
                            {
                            "test_cat": "monit_no_tgt",
                            "test_item": "Appearance of the dried cake",
                            "test_tgt_criterion": null,
                            "test_unit": null
                            }
                        ]
                    }
                    """
        json_dict = json.loads(str_json)
        self.drying_obj.load_from_json_dict(json_dict=json_dict)
        print('====================')
        print(f'operation_seq: {self.drying_obj.operation_seq}')
        print(f'edit_comment: {self.drying_obj.edit_comment}')
        print(f'pre_comment: {self.drying_obj.pre_comment}')
        print(f'post_comment: {self.drying_obj.post_comment}')
        print(f'Tj_ctrl_cat: {self.drying_obj.Tj_ctrl_cat}')
        print(f'Tj_low: {self.drying_obj.Tj_low}')
        print(f'Tj_high: {self.drying_obj.Tj_high}')
        print(f'Tbr_low: {self.drying_obj.Tbr_low}')
        print(f'Tbr_high: {self.drying_obj.Tbr_high}')
        print(f'mode_vac: {self.drying_obj.mode_vac}')
        print(f'pres_low: {self.drying_obj.pres_low}')
        print(f'pres_high: {self.drying_obj.pres_high}')
        print(f'rpm_min: {self.drying_obj.rpm_min}')
        print(f'rpm_max: {self.drying_obj.rpm_max}')
        print(f'intermission: {self.drying_obj.intermission}')
        print('<tests>')
        for test in self.drying_obj.list_ipc:
            print('--------------------')
            print(f'  test_cat: {test.test_cat}')
            print(f'  test_item: {test.test_item}')
            print(f'  test_tgt_criterion: {test.test_val_tgt_criterion}')
            print(f'  test_unit: {test.test_unit_val}')
        for test in self.drying_obj.list_monit_with_tgt:
            print('--------------------')
            print(f'  test_cat: {test.test_cat}')
            print(f'  test_item: {test.test_item}')
            print(f'  test_tgt_criterion: {test.test_val_tgt_criterion}')
            print(f'  test_unit: {test.test_unit_val}')
        for test in self.drying_obj.list_monit_no_tgt:
            print('--------------------')
            print(f'  test_cat: {test.test_cat}')
            print(f'  test_item: {test.test_item}')
            print(f'  test_tgt_criterion: {test.test_val_tgt_criterion}')
            print(f'  test_unit: {test.test_unit_val}')
        self.assertTrue(True)

class Test_30000_json_proc_output(unittest.TestCase):
    def setUp(self):
        self.mats_df = mats.generate_mats_df()
        self.mats_df = mats.add_to_mats_df(mats_df=self.mats_df,
                                                       material="test mat 1",
                                                       main_star=True,
                                                       mw = 18.01,
                                                       density=1.00,
                                                       conc_assay=99.999,
                                                       kg_main=2.00,
                                                       remark="Actually, I'm water.")
        self.mats_df = mats.add_to_mats_df(mats_df=self.mats_df,
                                                       material="test mat 2",
                                                       main_star=False,
                                                       mw = 46.07,
                                                       density=0.789,
                                                       conc_assay=94.0,
                                                       remark="Actually, I'm ethanol.")
        self.mats_inst = mats(self.mats_df)
        self.obj_proc = proc.Process(batch_name="json_test_batch", process_name="json_test_process", num_uo=4)
        self.obj_proc.mats_data = self.mats_inst
        self.list_uo = [chgng.Charging,
                        smplng.Sampling,
                        cip.CIP,
                        agit.Agitation,
                        evap.Evaporation,
                        filtsup.FiltSetup,
                        filt.Filtration,
                        plchldr.Placeholder,
                        inert.InertReplacement,
                        lnclear.LineClearance,
                        phdisch.PhaseDisch,
                        tempctrl.TempControl,
                        drying.Drying
                        ]
        return super().setUp()

    def test_30000_json_uo(self):

        dict_json_uo = self.obj_proc.data_input.json_uo(caller=self.obj_proc, list_uo=self.list_uo)
        print()
        print('----------------------')
        print(dict_json_uo)
        print('----------------------')
        with open("uo.json", "w", encoding="utf-8") as f:
            json.dump(dict_json_uo, f, ensure_ascii=False, indent=1)
        self.assertTrue(True)



class Test_40000_json_ai_interface(unittest.TestCase, trdef.GetMats):
    def setUp(self):
        self.mats_df = mats.generate_mats_df()
        self.mats_df = mats.add_to_mats_df(mats_df=self.mats_df,
                                                       material="H-Ala-Glu-GlyOMe",
                                                       main_star=True,
                                                       mw = 200,
                                                       density=1.00,
                                                       conc_assay=99.999,
                                                       kg_main=0.200,
                                                       remark="")
        self.mats_df = mats.add_to_mats_df(mats_df=self.mats_df,
                                                       material="Fmoc-Gly-OH",
                                                       main_star=False,
                                                       mw = 100,
                                                       density=1.00,
                                                       conc_assay=94.0,
                                                       remark="")
        self.mats_df = mats.add_to_mats_df(mats_df=self.mats_df,
                                                    material="dichloromethane",
                                                    main_star=False,
                                                    mw = 84.93,
                                                    density=1.33,
                                                    conc_assay=99.0,
                                                    remark="")
        self.mats_df = mats.add_to_mats_df(mats_df=self.mats_df,
                                                    material="1-hydroxy-7-azabenzotriazole",
                                                    main_star=False,
                                                    mw = 136.114,
                                                    density=0.973,
                                                    conc_assay=98.0,
                                                    remark="")
        self.mats_df = mats.add_to_mats_df(mats_df=self.mats_df,
                                                    material="conc NaHCO3",
                                                    main_star=False,
                                                    mw = 18,
                                                    density=1.0,
                                                    conc_assay=9.6,
                                                    remark="")
        self.mats_df = mats.add_to_mats_df(mats_df=self.mats_df,
                                                    material="conc NaCl",
                                                    main_star=False,
                                                    mw = 18,
                                                    density=1.0,
                                                    conc_assay=26,
                                                    remark="")
        self.mats_df = mats.add_to_mats_df(mats_df=self.mats_df,
                                                    material="Hexane",
                                                    main_star=False,
                                                    mw = 86.18,
                                                    density=0.67,
                                                    conc_assay=95,
                                                    remark="")             
        self.mats_inst = mats(self.mats_df)

        self.obj_proc = proc.Process(batch_name="ai_test_batch", process_name="ai_test_process", num_uo=4)
        self.obj_proc.mats_data = self.mats_inst

        return super().setUp()
    
    def get_mats(self) -> mats:
        return self.mats_inst

    def test_40000_load_proc_details(self):
        self.obj_proc.ai_load_process_details()
        self.assertTrue(True)



def suite_json_test():
    suite = unittest.TestSuite()
    # suite.addTest(Test_21000_input_json("test_21000_sampling_json_read"))
    #suite.addTest(Test_21000_input_json("test_21001_agitation_json_read"))
    #suite.addTest(Test_21000_input_json("test_21002_charging_json_read"))
    #suite.addTest(Test_21000_input_json("test_21004_cip_json_read"))
    #suite.addTest(Test_21000_input_json("test_21005_evaporation_json_out"))
    # suite.addTest(Test_21000_input_json("test_21006_evaporation_json_read"))
    #suite.addTest(Test_21000_input_json('test_21007_filtration_json_out'))
    #suite.addTest(Test_21000_input_json('test_21008_filtration_json_read'))
    #suite.addTest(Test_21000_input_json('test_21009_filter_setup_json_out'))
    # suite.addTest(Test_21000_input_json('test21010_filter_setup_json_read'))
    #suite.addTest(Test_30000_json_ai_interface('test_30000_load_proc_details'))
    #suite.addTest(Test_21000_input_json('test_21011_drying_json_out'))
    #suite.addTest(Test_21000_input_json('test_21012_drying_json_read'))
    suite.addTest(Test_30000_json_proc_output('test_30000_json_uo'))

    return suite
            


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite_json_test())
