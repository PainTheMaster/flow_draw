import unittest
import pandas as pd
import flow_draw.definitions as defs
import flow_draw.batch.batch as batch
import flow_draw.batch.process.process as proc
import flow_draw.batch.process.unit_operations.unit_operation as uo_module
import flow_draw.batch.process.unit_operations.uo_charging as chgng
import flow_draw.batch.process.unit_operations.uo_placeholder as plchldr
import flow_draw.batch.process.unit_operations.uo_line_clearance as lnclnc
import flow_draw.batch.process.unit_operations.uo_innert_replacement as innert
import flow_draw.batch.process.unit_operations.uo_temp_control as tempr
import flow_draw.batch.process.unit_operations.uo_agitation as agit
import flow_draw.batch.process.unit_operations.uo_settling as stlng
import flow_draw.batch.process.unit_operations.uo_phase_discharge as phdisch
import flow_draw.batch.process.unit_operations.uo_evaporation as evap
import flow_draw.batch.process.unit_operations.uo_cip as cip
import flow_draw.batch.process.unit_operations.uo_transfer as trsf
import flow_draw.batch.process.unit_operations.uo_filtration as filt
import flow_draw.batch.process.unit_operations.uo_sampling as smplng
import flow_draw.data_io.flowsheet  as fsht
import flow_draw.materials.materials as mats
import flow_draw.trait_def.trait_def as trdef
import os

class SaltyWaterFlow(unittest.TestCase):
    def setUp(self):
        return super().setUp()
    
    def test0000_OutputFlow(self):
        batch_name = "flowtest000"
        proc_name = "salt_water"
        tst_proc = proc.Process(batch_name=batch_name, process_name=proc_name,num_uo=1, comment="comment for proc")
        tst_proc.mats_data = mats.Materials(df_mats=PurchaseMaterials())
        tst_chgng = chgng.Charging(caller=tst_proc,
                                    flow_sheet=tst_proc.flowsheet,
                                    operation_seq=1,
                                    num_subitems=2,
                                    edit_comment="put salt and water")
        tst_proc.seq_uo.append(tst_chgng)
        tst_proc.seq_uo[0].load_params_from_df(SetChgngForSaltWater())
        tst_proc.seq_uo[0].output_unit_operation()
        tst_proc.flowsheet.save("test000_SaltWaterOutputFlow.xlsx")
        self.assertTrue(True)

    def test0001_Batch(self):
        wrong_batch_name = "wrong_batch_name"
        right_batch_name = "right_batch_name"
        proc_name = "salt_water"
        test_batch = batch.Batch()
        test_batch.batch_name = wrong_batch_name
        test_batch.num_procs = 3
        test_df = prep_batch_test_df(batch_name=right_batch_name, proc_name=proc_name, num_uo=1)
        test_batch.load_outline(test_df)
        sample_proc = test_batch.list_proc[0]
        result:bool = ((test_batch.batch_comment=="Batch comment") and
                       (test_batch.num_procs==1) and
                       (len(test_batch.list_proc)==1) and
                       (sample_proc.batch_name==right_batch_name) and
                       (sample_proc.process_name==proc_name))
        self.assertTrue(result)

def PurchaseMaterials() -> pd.DataFrame:
    dict_NaCl = {defs.hedr_io_mats_mat: "NaCl",
                 defs.hedr_io_mats_main: defs.itm_io_mats_desig_star,
                 defs.hedr_io_mats_mw: 58.44,
                 defs.hedr_io_mats_dnsty: 2.17,
                 defs.hedr_io_mats_concasy: 100.0,
                 defs.hedr_io_mats_kgmain: 1.00,
                 defs.hedr_io_mats_remark: "table salt"}

    dict_Water = {defs.hedr_io_mats_mat: "Water",
                 defs.hedr_io_mats_main: None,
                 defs.hedr_io_mats_mw: 18.01,
                 defs.hedr_io_mats_dnsty: 1.00,
                 defs.hedr_io_mats_concasy: 100.0,
                 defs.hedr_io_mats_kgmain: None,
                 defs.hedr_io_mats_remark: None}
    
    df_mats = pd.DataFrame([dict_NaCl, dict_Water])
    return df_mats


def SetChgngForSaltWater() -> pd.DataFrame:
    dict_input1 = {defs.hedr_cmn_io_dtil_seq : "1",
                    defs.hedr_cmn_io_dtil_uo : defs.tag_uo_charging,
                    defs.hedr_cmn_io_dtil_edt_cmnt : "put salt and water",
                    defs.hedr_cmn_io_dtil_precmnt : "Too much salt is harm",
                    defs.hedr_cmn_io_dtil_postcmnt : "Take care of your kidney",
                    defs.hedr_uo_chgng_mat : "NaCl",
                    defs.hedr_uo_chgng_mtrcs_val : 1.0,
                    defs.hedr_uo_chgng_mtrcs_unit : defs.opt_uo_chgng_mtrcs_eq,
                    defs.hedr_uo_chgng_errperm : 5.0,
                    defs.hedr_uo_chgng_method : defs.opt_uo_chgng_method_pwdr,
                    defs.hedr_uo_chgng_timctrl : defs.opt_uo_chgng_timctrl_none,
                    defs.hedr_uo_chgng_timmin : None,
                    defs.hedr_uo_chgng_timmax : None,
                    defs.hedr_uo_chgng_tempctrl : defs.opt_uo_chgng_temprctrl_none,
                    defs.hedr_uo_chgng_tempmin : None,
                    defs.hedr_uo_chgng_tempmax : None}
    
    dict_input2 = {defs.hedr_cmn_io_dtil_seq : "1",
                    defs.hedr_cmn_io_dtil_uo : defs.tag_uo_charging,
                    defs.hedr_cmn_io_dtil_edt_cmnt : "put salt and water",
                    defs.hedr_cmn_io_dtil_precmnt : "Water is dangerous.",
                    defs.hedr_cmn_io_dtil_postcmnt : "Don't dive in.",
                    defs.hedr_uo_chgng_mat : "Water",
                    defs.hedr_uo_chgng_mtrcs_val : 10.0,
                    defs.hedr_uo_chgng_mtrcs_unit : defs.opt_uo_chgng_mtrcs_vol,
                    defs.hedr_uo_chgng_errperm : 10.0,
                    defs.hedr_uo_chgng_method : defs.opt_uo_chgng_method_shower,
                    defs.hedr_uo_chgng_timctrl : defs.opt_uo_chgng_timctrl_min,
                    defs.hedr_uo_chgng_timmin : "1 hr",
                    defs.hedr_uo_chgng_timmax : None,
                    defs.hedr_uo_chgng_tempctrl : defs.opt_uo_chgng_temprctrl_min_max,
                    defs.hedr_uo_chgng_tempmin : 4.0,
                    defs.hedr_uo_chgng_tempmax :100.0 }
    df_input = pd.DataFrame([dict_input1, dict_input2])
    return df_input


def prep_batch_test_df(batch_name:str=None, proc_name:str=None, num_uo:int =0)-> pd.DataFrame:
    dict0: dict[str, list[str|int]] ={defs.hedr_io_batch_value:[batch_name,
                                    "Batch comment",
                                    proc_name,
                                    num_uo,
                                    "Remark for process-1",
                                    None,
                                    num_uo,
                                    "Remark for process-2"]}
    
    idx=[defs.item_io_batch_batch_name,
        defs.item_io_batch_batch_remark,
        defs.item_io_batch_proc_name_stem.format(1),
        defs.item_io_batch_proc_count_uo_stem.format(1),
        defs.item_io_batch_proc_remark_stem.format(1),
        defs.item_io_batch_proc_name_stem.format(2),
        defs.item_io_batch_proc_count_uo_stem.format(2),
        defs.item_io_batch_proc_remark_stem.format(2)]

    test_df = pd.DataFrame(dict0, index=idx)
    print("in prep_test_df(): test_df")
    print(test_df)
    print("==========\n")
    # test_df.index = test_df[0]
    # print("in prep_test_df(): test_df re-indexed")
    # print(test_df)
    # print("==========\n")
    # print("len(test_df): ", len(test_df))
    # print("==========\n")
    return test_df


class UnitOperationOutputTest(unittest.TestCase):
    def setUp(self):

        return super().setUp()

    def test_1001_placeholder(self):
        sheet = fsht.Flowsheet()
        uo_instance = plchldr.Placeholder(flowsheet=sheet, operation_seq=1, num_subitems=1)
        uo_instance.pre_comment='Test 1001 precomment\nTest1001 additional precomment (line-2)'
        uo_instance.num_lines = 0
        uo_instance.post_comment='Test 1001 postcomment'
        uo_instance.output_unit_operation()
        sheet.save(filename='Test1001_flowsheet_out.xlsx')
        self.assertTrue(True)

    def test_1002_line_clearance(self):
        sheet = fsht.Flowsheet()
        uo_instance = lnclnc.LineClearance(flowsheet=sheet, operation_seq=2)
        uo_instance.sop = "TEST SOP"
        uo_instance.output_unit_operation()
        sheet.save(filename='Test1002_flowsheet_out.xlsx')
        self.assertTrue(True)

    def test_1003_innert_replace(self):
        sheet = fsht.Flowsheet()
        uo_instance = innert.InnertReplacement(flowsheet=sheet, operation_seq=3)
        uo_instance.innert_gas=defs.opt_uo_innert_gas_Ar
        uo_instance.neg_pressure = -0.08
        uo_instance.num_repeat = 2
        uo_instance.output_unit_operation()
        sheet.save(filename='Test1003_flowsheet_out.xlsx')
        self.assertTrue(True)

    def test_1004_temp_ctrl_prog_mode(self):
        sheet = fsht.Flowsheet()
        uo_instance = tempr.TempControl(flowsheet=sheet, operation_seq=1)
        uo_instance.ctrl_mode = tempr.opt_mode_prog
        uo_instance.Ti_sp = 10.0
        uo_instance.time_val_prog = 1.0
        uo_instance.time_unit_prog = defs.tag_flow_cmn_time_unit_hour
        uo_instance.Ti_limit_low = 5.0
        uo_instance.Ti_limit_high = 15.0
        uo_instance.Tj_limit_high = 30.0
        uo_instance.Tj_limit_low = 0.0

        uo_instance.output_unit_operation()
        sheet.save(filename="Test1004_temp_prog_mode.xlsx")
        self.assertTrue(True)

    def test_1005_temp_ctrl_TiTj_mode(self):
        sheet = fsht.Flowsheet()
        uo_instance = tempr.TempControl(flowsheet=sheet, operation_seq=1)
        uo_instance.ctrl_mode = tempr.opt_mode_TiTj
        uo_instance.pre_comment = "Pre-comment line-1\nPreComment line-2"
        uo_instance.Ti_sp = 30.0
        uo_instance.time_unit_prog = defs.tag_flow_cmn_time_unit_hour
        uo_instance.Tj_limit_low = 20.0
        uo_instance.Tj_limit_high = 35.0
        
        uo_instance.Ti_limit_low = 25.0
        uo_instance.Ti_limit_high = 35.0
        
        uo_instance.Ti_tgt_low = 27.5
        uo_instance.Ti_tgt_high = 32.5

        uo_instance.endpoint_check = True

        print(uo_module.list_unit_ops)

        uo_instance.output_unit_operation()
        sheet.save(filename="Test1005_temp_TiTj_mode.xlsx")
        self.assertTrue(True)
        
    def test_1006_temp_ctrl_Tj_mode(self):
        sheet = fsht.Flowsheet()
        uo_instance = tempr.TempControl(flowsheet=sheet, operation_seq=1)
        uo_instance.ctrl_mode = tempr.opt_mode_Tj
        uo_instance.pre_comment = "Pre-comment line-1\nPreComment line-2"
        uo_instance.Ti_sp = 30.0

        uo_instance.Tj_sp = 30.0
        
        # uo_instance.Ti_limit_low = 25.0
        # uo_instance.Ti_limit_high = 35.0
        
        # uo_instance.Ti_tgt_low = 27.5
        # uo_instance.Ti_tgt_high = 30.0

        uo_instance.endpoint_check = True

        # print(uo_module.list_unit_ops)

        uo_instance.output_unit_operation()
        sheet.save(filename="Test1006_tempr_Tj_mode.xlsx")
        self.assertTrue(True)


    def test_1007_temp_ctrl_Ti_mode(self):
        sheet = fsht.Flowsheet()
        uo_instance = tempr.TempControl(flowsheet=sheet, operation_seq=1)
        uo_instance.ctrl_mode = tempr.opt_mode_Ti
        uo_instance.pre_comment = "Pre-comment line-1\nPreComment line-2"
        uo_instance.Ti_sp = 40.0

        uo_instance.Tj_sp = 30.0
        
        uo_instance.Ti_limit_low = 35.0
        uo_instance.Ti_limit_high = 45.0
        
        uo_instance.Ti_tgt_low = 37.5
        uo_instance.Ti_tgt_high = 42.5

        uo_instance.endpoint_check = True

        # print(uo_module.list_unit_ops)

        uo_instance.output_unit_operation()
        sheet.save(filename="Test1007_tempr_Ti_mode.xlsx")
        self.assertTrue(True)

    def test_1008_agit_full(self):
        sheet = fsht.Flowsheet()
        uo_instance = agit.Agitation(flowsheet=sheet, operation_seq=1)
        uo_instance.time_min = 1.0
        uo_instance.time_max = 1.0
        uo_instance.time_unit = agit.tag_flow_cmn_time_unit_hour
        uo_instance.Ti_min = 35.0 
        uo_instance.Ti_max = 45.0
        uo_instance.spec_agit = agit.opt_spec_guide
        uo_instance.rpm = 80.0
        uo_instance.dissolution_check = True

        print(uo_module.list_unit_ops)

        uo_instance.output_unit_operation()
        sheet.save(filename="Test1008_agitation_full.xlsx")
        self.assertTrue(True)

    def test_1009_agit_minimal(self):
        sheet = fsht.Flowsheet()
        uo_instance = agit.Agitation(flowsheet=sheet, operation_seq=1)
        uo_instance.spec_agit = agit.opt_spec_guide
        uo_instance.rpm = 80.0

        print(uo_module.list_unit_ops)

        uo_instance.output_unit_operation()
        sheet.save(filename="Test1009_agitation_minimal.xlsx")
        self.assertTrue(True)


    def test_1010_settling_full(self):
        sheet = fsht.Flowsheet()
        uo_instance = stlng.Settling(flowsheet=sheet, operation_seq=1)
        uo_instance.time_min = 1.0
        uo_instance.time_max = 1.0
        uo_instance.time_unit = stlng.opt_time_unit_second
        uo_instance.Ti_min = 20.0
        uo_instance.Ti_max = 30.0

        print(uo_module.list_unit_ops)

        uo_instance.output_unit_operation()
        sheet.save(filename="Test1010_settling_full.xlsx")
        self.assertTrue(True)

    def test_1011_settling_minimal(self):
        sheet = fsht.Flowsheet()
        uo_instance = stlng.Settling(flowsheet=sheet, operation_seq=1)

        print(uo_module.list_unit_ops)

        uo_instance.output_unit_operation()
        sheet.save(filename="Test1011_settling_minimal.xlsx")
        self.assertTrue(True)
    
    def test_1012_phase_disch_full(self):
        sheet = fsht.Flowsheet()
        uo_instance = phdisch.PhaseDisch(flowsheet=sheet, operation_seq=10)
        uo_instance.pre_comment = "Pre-comment-1\nPre-comment-2"
        uo_instance.post_comment = "Post comennt"
        uo_instance.origin = 'RV_ORIG'
        uo_instance.via = 'Multiplexer'
        uo_instance.destin.append('Destin tank 1')
        uo_instance.destin.append('Destin tank 2')

        print(uo_module.list_unit_ops)

        uo_instance.output_unit_operation()
        sheet.save(filename="Test1012_phase_disch_full.xlsx")
        self.assertTrue(True)


    def test_1013_phase_disch_med(self):
        sheet = fsht.Flowsheet()
        uo_instance = phdisch.PhaseDisch(flowsheet=sheet, operation_seq=11)

        uo_instance.destin.append('Destin tank')


        print(uo_module.list_unit_ops)

        uo_instance.output_unit_operation()
        sheet.save(filename="Test1013_phase_disch_med.xlsx")
        self.assertTrue(True)


    def test_1014_phase_disch_minimal(self):
        sheet = fsht.Flowsheet()
        uo_instance = phdisch.PhaseDisch(flowsheet=sheet, operation_seq=11)

        print(uo_module.list_unit_ops)

        uo_instance.output_unit_operation()
        sheet.save(filename="Test1014_phase_disch_minimal.xlsx")
        self.assertTrue(True)


class AgitationTest2000(unittest.TestCase, trdef.GetMats):
    def __init__(self, methodName = "runTest"):
        self.mats: mats.Materials = None
        super().__init__(methodName)
    def setUp(self):
        mats_df = mats.Materials.generate_mats_df()
        mats_df = mats.Materials.add_to_mats_df(mats_df=mats_df,
                                      material="ぎゅうにく",
                                      main_star=True,
                                      mw=100.0,
                                      density=1.1,
                                      conc_assay=90.0,
                                      kg_main=2.0,
                                      remark="残り10%は普通の肉が混入。何の肉かは聞いてはいけない。")
        mats_df = mats.Materials.add_to_mats_df(mats_df=mats_df,
                                      material="たまねぎ",
                                      mw=50.0,
                                      density=0.9,
                                      conc_assay=100.0,
                                      remark="淡路島産")
        mats_df = mats.Materials.add_to_mats_df(mats_df=mats_df,
                                      material="スパイス",
                                      mw=10.0,
                                      density=0.8,
                                      conc_assay=100.0,
                                      remark="これは上物のブツだぜ。")
        print("testprint")
        print(mats_df)       
        self.mats = mats.Materials(df_mats = mats_df)
        self.sheet = fsht.Flowsheet()

        return super().setUp()
    
    def get_mats(self)-> mats.Materials:
        return self.mats
    
    # def test_pretest_2000(self):
    #     evap_instance:evap.Evaporation = evap.Evaporation(caller=self,
    #                                                       flowsheet=self.sheet,
    #                                                       operation_seq=1,
    #                                                       num_subitems=1,
    #                                                       edit_comment=None)
    #     evap_instance.

    #     self.assertTrue(True)

    def test_full_dataset_2000(self):
        test_df=evap.Evaporation.generate_test_df(precomment="precomment for test 2000",
                                                  postcomment="postcomment for test 2000",
                                                  Tj_min=50.0,
                                                  Tj_max=100.0,
                                                  Tbr_min=-25,
                                                  Tbr_max=5,
                                                  press_ctrl=evap.opt_press_ctrl_specific,
                                                  press_min=0.0,
                                                  press_max=1.0,
                                                  unit_press=evap.opt_press_unit_kPaA,
                                                  agit_spec=evap.opt_agit_spec_guide,
                                                  agit_rpm=30.0,
                                                  vw_spec_min=10,
                                                  vw_spec_max=15.0,
                                                  vw_guide_min=11.0,
                                                  vw_guide_max=12.0)
        print(test_df)
        evap_instance:evap.Evaporation = evap.Evaporation(caller=self,
                                                          flowsheet=self.sheet,
                                                          operation_seq=1,
                                                          num_subitems=1,
                                                          edit_comment=None)
        evap_instance.load_params_from_df(df=test_df)
        evap_instance.output_unit_operation()
        self.sheet.save("Test_2000_evap_flowsheet.xlsx")
        self.assertTrue(True)



    def test_2001_press_discrepancy(self):
        test_df=evap.Evaporation.generate_test_df(precomment="precomment for test 2001",
                                                  postcomment="postcomment for test 2001",
                                                  Tj_min=50.0,
                                                  Tj_max=100.0,
                                                  Tbr_min=-25,
                                                  Tbr_max=5,
                                                  press_ctrl=evap.opt_press_ctrl_specific,
                                                  #press_min=0.0,
                                                  #press_max=1.0,
                                                  unit_press=evap.opt_press_unit_kPaA,
                                                  agit_spec=evap.opt_agit_spec_guide,
                                                  agit_rpm=30.0,
                                                  vw_spec_min=10,
                                                  vw_spec_max=15.0,
                                                  vw_guide_min=11.0,
                                                  vw_guide_max=12.0)
        print(test_df)
        evap_instance:evap.Evaporation = evap.Evaporation(caller=self,
                                                          flowsheet=self.sheet,
                                                          operation_seq=1,
                                                          num_subitems=1,
                                                          edit_comment=None)
        #evap_instance.load_params_from_df(df=test_df)
        # evap_instance.output_unit_operation()
        # self.sheet.save("Test_2001_evap_flowsheet.xlsx")
        with self.assertRaises(expected_exception=ValueError):
            evap_instance.load_params_from_df(df=test_df)
    

    def test_2002_no_press_unit(self):
        test_df=evap.Evaporation.generate_test_df(precomment="precomment for test 2002",
                                                  postcomment="postcomment for test 2002",
                                                  Tj_min=50.0,
                                                  Tj_max=100.0,
                                                  Tbr_min=-25,
                                                  Tbr_max=5,
                                                  press_ctrl=evap.opt_press_ctrl_specific,
                                                  press_min=0.0,
                                                  press_max=1.0,
                                                  #unit_press=evap.opt_press_unit_kPaA,
                                                  agit_spec=evap.opt_agit_spec_guide,
                                                  agit_rpm=30.0,
                                                  vw_spec_min=10,
                                                  vw_spec_max=15.0,
                                                  vw_guide_min=11.0,
                                                  vw_guide_max=12.0)
        print(test_df)
        evap_instance:evap.Evaporation = evap.Evaporation(caller=self,
                                                          flowsheet=self.sheet,
                                                          operation_seq=1,
                                                          num_subitems=1,
                                                          edit_comment=None)
        #evap_instance.load_params_from_df(df=test_df)
        # evap_instance.output_unit_operation()
        # self.sheet.save("Test_2001_evap_flowsheet.xlsx")
        with self.assertRaises(expected_exception=ValueError):
            evap_instance.load_params_from_df(df=test_df)
            

    def test_2003_no_evap_endpoint(self):
        test_df=evap.Evaporation.generate_test_df(precomment="precomment for test 2003",
                                                  postcomment="postcomment for test 2003",
                                                  Tj_min=50.0,
                                                  Tj_max=100.0,
                                                  Tbr_min=-25,
                                                  Tbr_max=5,
                                                  press_ctrl=evap.opt_press_ctrl_specific,
                                                  press_min=0.0,
                                                  press_max=1.0,
                                                  unit_press=evap.opt_press_unit_kPaA,
                                                  agit_spec=evap.opt_agit_spec_guide,
                                                  agit_rpm=30.0,
                                                  #vw_spec_min=10,
                                                  #vw_spec_max=15.0,
                                                  #vw_guide_min=11.0,
                                                  #vw_guide_max=12.0
                                                  )
        print(test_df)
        evap_instance:evap.Evaporation = evap.Evaporation(caller=self,
                                                          flowsheet=self.sheet,
                                                          operation_seq=1,
                                                          num_subitems=1,
                                                          edit_comment=None)
        #evap_instance.load_params_from_df(df=test_df)
        # evap_instance.output_unit_operation()
        # self.sheet.save("Test_2001_evap_flowsheet.xlsx")
        evap_instance.load_params_from_df(df=test_df)
        with self.assertRaises(expected_exception=ValueError):
            evap_instance.output_unit_operation()


    def test_2004_minimum_datasets(self):
        test_df=evap.Evaporation.generate_test_df(#precomment="precomment for test 2004",
                                                  #postcomment="postcomment for test 2004",
                                                  Tj_min=50.0,
                                                  #Tj_max=100.0,
                                                  #Tbr_min=-25,
                                                  Tbr_max=5,
                                                  #press_ctrl=evap.opt_press_ctrl_specific,
                                                  #press_min=0.0,
                                                  #press_max=1.0,
                                                  #unit_press=evap.opt_press_unit_kPaA,
                                                  #agit_spec=evap.opt_agit_spec_guide,
                                                  #agit_rpm=30.0,
                                                  #vw_spec_min=10,
                                                  #vw_spec_max=15.0,
                                                  #vw_guide_min=11.0,
                                                  vw_guide_max=12.0
                                                  )
        print(test_df)
        evap_instance:evap.Evaporation = evap.Evaporation(caller=self,
                                                          flowsheet=self.sheet,
                                                          operation_seq=1,
                                                          num_subitems=1,
                                                          edit_comment=None)
        evap_instance.load_params_from_df(df=test_df)
        evap_instance.output_unit_operation()
        self.sheet.save("Test_2004_evap_flowsheet.xlsx")
        self.assertTrue(True)



class CIPTest3000(unittest.TestCase, trdef.GetMats):
    def __init__(self, methodName = "runTest"):
        self.mats: mats.Materials = None
        super().__init__(methodName)
    def setUp(self):
        mats_df = mats.Materials.generate_mats_df()
        mats_df = mats.Materials.add_to_mats_df(mats_df=mats_df,
                                      material="ぎゅうにく",
                                      main_star=True,
                                      mw=100.0,
                                      density=1.1,
                                      conc_assay=90.0,
                                      kg_main=2.0,
                                      remark="残り10%は普通の肉が混入。何の肉かは聞いてはいけない。")
        mats_df = mats.Materials.add_to_mats_df(mats_df=mats_df,
                                      material="たまねぎ",
                                      mw=50.0,
                                      density=0.9,
                                      conc_assay=100.0,
                                      remark="淡路島産")
        mats_df = mats.Materials.add_to_mats_df(mats_df=mats_df,
                                      material="スパイス",
                                      mw=10.0,
                                      density=0.8,
                                      conc_assay=100.0,
                                      remark="これは上物のブツだぜ。")
        print("testprint")
        print(mats_df)       
        self.mats = mats.Materials(df_mats = mats_df)
        self.sheet = fsht.Flowsheet()
    
    def get_mats(self)->mats.Materials:
        return self.mats

    def test_3000_full_datasets(self):
        test_df=cip.CIP.generate_test_df(precomment="Pre-comment for test-3000",
                                         postcomment="Post-comment for test-3000",
                                         cip_tgt="大きな釜",
                                         solvent="H2O",
                                         qty_kg=10,
                                         via="multiplexer")
        cip.CIP.add_to_test_df(df=test_df,
                               cip_tgt="大きな釜",
                               solvent="MeOH",
                               qty_kg=15,
                               via="multiplexer")
                                                  
        print(test_df)
        cip_instance:cip.CIP = cip.CIP(caller=self,
                                       flowsheet=self.sheet,
                                       operation_seq=1,
                                       num_subitems=2,
                                       edit_comment=None)
        cip_instance.load_params_from_df(df=test_df)
        cip_instance.output_unit_operation()
        self.sheet.save("Test_3000_cip_flowsheet.xlsx")
        self.assertTrue(True)

    def test_3001_minimum_datasets(self):
        test_df=cip.CIP.generate_test_df(precomment="Pre-comment for test-3000",
                                         postcomment="Post-comment for test-3000",
                                         cip_tgt="大きな釜",
                                         solvent="H2O",
                                         qty_kg=10)
                                         #via="multiplexer"
        cip.CIP.add_to_test_df(df=test_df,
                               cip_tgt="大きな釜",
                               solvent="MeOH",
                               qty_kg=15)
                               #via="multiplexer")
                                                  
        print(test_df)
        cip_instance:cip.CIP = cip.CIP(caller=self,
                                       flowsheet=self.sheet,
                                       operation_seq=1,
                                       num_subitems=2,
                                       edit_comment=None)
        cip_instance.load_params_from_df(df=test_df)
        cip_instance.output_unit_operation()
        self.sheet.save("Test_3001_cip_flowsheet.xlsx")
        self.assertTrue(True)


class TransfTest4100(unittest.TestCase, trdef.UniversalTrait):
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)

    def setUp(self):
        self.flowsheet = fsht.Flowsheet()

    def test_4100_fullset(self):
        test_inst_1=trsf.Transfer(caller=self,
                                  flowsheet=self.flowsheet,
                                  operation_seq=1,
                                  num_subitems=1)
        test_df_1 = trsf.Transfer.generate_test_df(operation=trsf.opt_operation_setup,
                                                 origin="Setup test origin",
                                                 via="Setup test waypoint",
                                                 destination="Setup test destination",
                                                 filter="Setup test filter")
        test_inst_1.load_params_from_df(test_df_1)

        test_inst_2 = trsf.Transfer(caller=self,
                                    flowsheet=self.flowsheet,
                                    operation_seq=2,
                                    num_subitems=1)
        test_df_2 = trsf.Transfer.generate_test_df(operation=trsf.opt_operation_transfer,
                                                   origin="Transf test origin",
                                                   via="Transf test waypoint",
                                                   destination="Transf test destination",
                                                   filter="Transf test filt")
        test_inst_2.load_params_from_df(test_df_2)

        test_inst_1.output_unit_operation()
        test_inst_2.output_unit_operation()
        self.flowsheet.save("Test_4100_setup_transf_fullset.xlsx")
        self.assertTrue(True)
    
    def test_4101_no_via(self):
        test_inst_1=trsf.Transfer(caller=self,
                                  flowsheet=self.flowsheet,
                                  operation_seq=1,
                                  num_subitems=1)
        test_df_1 = trsf.Transfer.generate_test_df(operation=trsf.opt_operation_setup,
                                                 origin="Setup test origin",
                                                 #via="Setup test waypoint",
                                                 destination="Setup test destination",
                                                 filter="Setup test filter")
        test_inst_1.load_params_from_df(test_df_1)

        test_inst_2 = trsf.Transfer(caller=self,
                                    flowsheet=self.flowsheet,
                                    operation_seq=2,
                                    num_subitems=1)
        test_df_2 = trsf.Transfer.generate_test_df(operation=trsf.opt_operation_transfer,
                                                   origin="Transf test origin",
                                                   #via="Transf test waypoint",
                                                   destination="Transf test destination",
                                                   filter="Transf test filt")
        test_inst_2.load_params_from_df(test_df_2)

        test_inst_1.output_unit_operation()
        test_inst_2.output_unit_operation()
        self.flowsheet.save("Test_4101_setup_transf_no_via.xlsx")
        self.assertTrue(True)

       
    def test_4102_minimum(self):
        test_inst_1=trsf.Transfer(caller=self,
                                  flowsheet=self.flowsheet,
                                  operation_seq=1,
                                  num_subitems=1)
        test_df_1 = trsf.Transfer.generate_test_df(operation=trsf.opt_operation_setup,
                                                #  origin="Setup test origin",
                                                #  via="Setup test waypoint",
                                                 destination="Setup test destination"
                                                #  filter="Setup test filter"
                                                 )
        test_inst_1.load_params_from_df(test_df_1)

        test_inst_2 = trsf.Transfer(caller=self,
                                    flowsheet=self.flowsheet,
                                    operation_seq=2,
                                    num_subitems=1)
        test_df_2 = trsf.Transfer.generate_test_df(operation=trsf.opt_operation_transfer,
                                                #    origin="Transf test origin",
                                                #    via="Transf test waypoint",
                                                   destination="Transf test destination"
                                                #    filter="Transf test filt"
                                                )
        test_inst_2.load_params_from_df(test_df_2)

        test_inst_1.output_unit_operation()
        test_inst_2.output_unit_operation()
        self.flowsheet.save("Test_4102_setup_transf_minimum.xlsx")
        self.assertTrue(True)

    def test_4103_err_no_operation(self):
        test_inst_1=trsf.Transfer(caller=self,
                                flowsheet=self.flowsheet,
                                operation_seq=1,
                                num_subitems=1)
        test_df_1 = trsf.Transfer.generate_test_df(#operation=trsf.opt_operation_setup
                                                #  origin="Setup test origin",
                                                #  via="Setup test waypoint",
                                                destination="Setup test destination"
                                                #  filter="Setup test filter"
                                                )
        
        with self.assertRaises(expected_exception=ValueError):
            test_inst_1.load_params_from_df(test_df_1)
    
    def test_4104_err_no_destin(self):
        test_inst_1=trsf.Transfer(caller=self,
                                flowsheet=self.flowsheet,
                                operation_seq=1,
                                num_subitems=1)
        test_df_1 = trsf.Transfer.generate_test_df(#operation=trsf.opt_operation_setup
                                                #  origin="Setup test origin",
                                                #  via="Setup test waypoint",
                                                destination="Setup test destination"
                                                #  filter="Setup test filter"
                                                )       
        
        with self.assertRaises(expected_exception=ValueError):
            test_inst_1.load_params_from_df(test_df_1)
    


        # with self.assertRaises(expected_exception=ValueError):
        #     evap_instance.output_unit_operation()

class FiltTest4200(unittest.TestCase, trdef.UniversalTrait):
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)

    def setUp(self):
        self.flowsheet = fsht.Flowsheet()
    
    def test_4201_filt_full(self):
        test_inst = filt.Filtration(caller=self,
                                    flowsheet=self.flowsheet,
                                    operation_seq=1,
                                    num_subitems=1)
        df = filt.Filtration.generate_test_df(equipment="test_4201_FD",
                                              Tj=25,
                                              P_min=100,
                                              P_max=100,
                                              P_unit=filt.opt_hedr_press_kPa,
                                              integ_test=filt.opt_integ_test_yes)
        test_inst.load_params_from_df(df)
        test_inst.output_unit_operation()
        self.flowsheet.save("Test_4201_filt_full.xlsx")
        self.assertTrue(True)

    def test_4202_filt_p_max(self):
        test_inst = filt.Filtration(caller=self,
                                    flowsheet=self.flowsheet,
                                    operation_seq=1,
                                    num_subitems=1)
        df = filt.Filtration.generate_test_df(equipment="test_4210_FD",
                                              Tj=25,
                                            #   P_min=100,
                                              P_max=100,
                                              P_unit=filt.opt_hedr_press_kPa,
                                              integ_test=filt.opt_integ_test_yes)
        test_inst.load_params_from_df(df)
        test_inst.output_unit_operation()
        self.flowsheet.save("Test_4202_filt_p_max.xlsx")
        self.assertTrue(True)

    def test_4203_filt_min(self):
        test_inst = filt.Filtration(caller=self,
                                    flowsheet=self.flowsheet,
                                    operation_seq=1,
                                    num_subitems=1)
        df = filt.Filtration.generate_test_df(equipment="test_4210_FD")
                                            #   Tj=25,
                                            #   P_min=100,
                                            #   P_max=100,
                                            #   P_unit=filt.opt_hedr_press_kPa,
                                            #   integ_test=filt.opt_integ_test_yes)
        test_inst.load_params_from_df(df)
        test_inst.output_unit_operation()
        self.flowsheet.save("Test_4203_filt_minimum.xlsx")
        self.assertTrue(True)

    
    def test_4204_no_equip(self):
        test_inst = filt.Filtration(caller=self,
                                    flowsheet=self.flowsheet,
                                    operation_seq=1,
                                    num_subitems=1)
        df = filt.Filtration.generate_test_df(#equipment="test_4210_FD"
                                              Tj=25,
                                              P_min=100,
                                              P_max=100,
                                              P_unit=filt.opt_hedr_press_kPa,
                                              integ_test=filt.opt_integ_test_yes)
        
        with self.assertRaises(expected_exception=ValueError):
            test_inst.load_params_from_df(df)
    
    def test_4205_no_p_unit(self):
        test_inst = filt.Filtration(caller=self,
                                    flowsheet=self.flowsheet,
                                    operation_seq=1,
                                    num_subitems=1)
        df = filt.Filtration.generate_test_df(equipment="test_4210_FD",
                                              Tj=25,
                                              P_min=100,
                                              P_max=100,
                                            #   P_unit=filt.opt_hedr_press_kPa,
                                              integ_test=filt.opt_integ_test_yes)
        
        with self.assertRaises(expected_exception=ValueError):
            test_inst.load_params_from_df(df)


class SamplingTest4300(unittest.TestCase, trdef.UniversalTrait):
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)

    def setUp(self):
        self.flowsheet = fsht.Flowsheet()
    
    def test_4301_full(self):
        test_inst = smplng.Sampling(caller=self,
                                    flowsheet=self.flowsheet,
                                    operation_seq=6,
                                    num_subitems=2)
        df = smplng.Sampling.generate_test_df(sample_name="test sample 1",
                                              sampling_cat=smplng.opt_sampling_cat_both,
                                              ipc_criteria="残原料1:≦0.5%\n残原料2≦0.5%",
                                              ipc_rec_titles="残原料1\n残原料2",
                                              ipc_rec_units="%\n%",
                                              monit_items="酸性度\n結晶形",
                                              monit_rec_items="酸性度\n結晶形",
                                              monit_rec_units="%\n",
                                              sample_comment="This is a comment for sample test 4301-1.")
        smplng.Sampling.add_to_test_df(df=df,
                                       sample_name="test sample 2",
                                       sampling_cat=smplng.opt_sampling_cat_both,
                                       ipc_criteria="残原料1:≦0.1%\n残原料2≦0.1%",
                                       ipc_rec_titles="残原料1\n残原料2",
                                       ipc_rec_units="%\n%",
                                       monit_items="酸性度2\n結晶形2",
                                       monit_rec_items="酸性度2\n結晶形2",
                                       monit_rec_units="%\n",
                                       sample_comment="This is a comment for sample test 4301-2.")
        test_inst.load_params_from_df(df=df)
        test_inst.output_unit_operation()
        self.flowsheet.save("Test_4301_sampling_full.xlsx")
        self.assertTrue(True)

    def test_4302_ipc_only(self):
        test_inst = smplng.Sampling(caller=self,
                                    flowsheet=self.flowsheet,
                                    operation_seq=6,
                                    num_subitems=1)
        df = smplng.Sampling.generate_test_df(sample_name="test sample 1",
                                              sampling_cat=smplng.opt_sampling_cat_ipc,
                                              ipc_criteria="残原料1:≦0.5%",
                                              ipc_rec_titles="残原料1",
                                              ipc_rec_units="%",
                                              sample_comment="This is a comment for sample test 4302.")
        test_inst.load_params_from_df(df=df)
        test_inst.output_unit_operation()
        self.flowsheet.save("Test_4302_ipc_only.xlsx")
        self.assertTrue(True)
    
    def test_4303_monit_only(self):
        test_inst = smplng.Sampling(caller=self,
                                    flowsheet=self.flowsheet,
                                    operation_seq=6,
                                    num_subitems=2)
        df = smplng.Sampling.generate_test_df(sample_name="test sample 1",
                                              sampling_cat=smplng.opt_sampling_cat_monit,
                                              monit_items="酸性度",
                                              monit_rec_items="pH",
                                              monit_rec_units="",
                                              sample_comment="This is a comment for sample test 4303.")
        test_inst.load_params_from_df(df=df)
        test_inst.output_unit_operation()
        self.flowsheet.save("Test_4303_monit_only.xlsx")
        self.assertTrue(True)

    def test_4304_noname_err(self):
        test_inst = smplng.Sampling(caller=self,
                                    flowsheet=self.flowsheet,
                                    operation_seq=6,
                                    num_subitems=1)
        df = smplng.Sampling.generate_test_df(#sample_name="test sample 1",
                                              sampling_cat=smplng.opt_sampling_cat_monit,
                                              monit_items="酸性度",
                                              monit_rec_items="pH",
                                              monit_rec_units="",
                                              sample_comment="This is a comment for sample test 4304.")
        with self.assertRaises(expected_exception=ValueError):
            test_inst.load_params_from_df(df=df)
        
    def test_4305_no_ipc_crteria(self):
        test_inst = smplng.Sampling(caller=self,
                                    flowsheet=self.flowsheet,
                                    operation_seq=6,
                                    num_subitems=1)
        df = smplng.Sampling.generate_test_df(sample_name="test sample 1",
                                              sampling_cat=smplng.opt_sampling_cat_ipc,
                                              #ipc_criteria="残原料1:≦0.5%",
                                              ipc_rec_titles="残原料1",
                                              ipc_rec_units="%",
                                              sample_comment="This is a comment for sample test 4305.")
        with self.assertRaises(expected_exception=ValueError):
            test_inst.load_params_from_df(df=df)

    def test_4306_ipc_item_unit_mismatch(self):
        test_inst = smplng.Sampling(caller=self,
                                    flowsheet=self.flowsheet,
                                    operation_seq=6,
                                    num_subitems=1)
        df = smplng.Sampling.generate_test_df(sample_name="test sample 1",
                                              sampling_cat=smplng.opt_sampling_cat_ipc,
                                              ipc_criteria="残原料1:≦0.5%",
                                              ipc_rec_titles="残原料1\n残原料2",
                                              ipc_rec_units="%",
                                              sample_comment="This is a comment for sample test 4306.")
        with self.assertRaises(expected_exception=ValueError):
            test_inst.load_params_from_df(df=df)
    
    def test_4307_ipc_criteria_item_mismatch(self):
        test_inst = smplng.Sampling(caller=self,
                                    flowsheet=self.flowsheet,
                                    operation_seq=6,
                                    num_subitems=1)
        df = smplng.Sampling.generate_test_df(sample_name="test sample 1",
                                              sampling_cat=smplng.opt_sampling_cat_ipc,
                                              ipc_criteria="残原料1:≦0.5%\n残原料2≦0.1%",
                                              ipc_rec_titles="残原料1",
                                              ipc_rec_units="%",
                                              sample_comment="This is a comment for sample test 4307.")
        with self.assertRaises(expected_exception=ValueError):
            test_inst.load_params_from_df(df=df)
    
    def test_4308_monit_item_unit_mismatch(self):
        test_inst = smplng.Sampling(caller=self,
                                    flowsheet=self.flowsheet,
                                    operation_seq=6,
                                    num_subitems=1)
        df = smplng.Sampling.generate_test_df(sample_name="test sample 1",
                                              sampling_cat=smplng.opt_sampling_cat_monit,
                                              monit_items="酸性度",
                                              monit_rec_items="pH",
                                            #   monit_rec_units="",
                                              sample_comment="This is a comment for sample test 4308.")
        with self.assertRaises(expected_exception=ValueError):
            test_inst.load_params_from_df(df=df)


def suite_0000_40000():
    suite = unittest.TestSuite()
    # suite.addTest(UnitOperationOutputTest("test_1001_placeholder"))
    #For the 2nd and likewise.... suite.addTest("something here")
    # suite.addTest(UnitOperationOutputTest("test_1004_temp_ctrl_prog_mode"))
    # suite.addTest(UnitOperationOutputTest("test_1005_temp_ctrl_TiTj_mode"))
    # suite.addTest(UnitOperationOutputTest("test_1006_temp_ctrl_Tj_mode"))
    # suite.addTest(UnitOperationOutputTest("test_1007_temp_ctrl_Ti_mode"))
    suite.addTest(UnitOperationOutputTest("test_1008_agit_full"))
    suite.addTest(UnitOperationOutputTest("test_1009_agit_minimal"))
    # suite.addTest(UnitOperationOutputTest("test_1010_settling_full"))
    # suite.addTest(UnitOperationOutputTest("test_1011_settling_minimal"))
    # suite.addTest(UnitOperationOutputTest("test_1012_phase_disch_full"))
    # suite.addTest(UnitOperationOutputTest("test_1013_phase_disch_med"))
    # suite.addTest(UnitOperationOutputTest("test_1014_phase_disch_minimal"))
    # suite.addTest(AgitationTest2000("test_2001_press_discrepancy"))
    # suite.addTest(AgitationTest2000("test_2002_no_press_unit"))
    # suite.addTest(AgitationTest2000("test_2003_no_evap_endpoint"))
    # suite.addTest(AgitationTest2000("test_2004_minimum_datasets"))
    # suite.addTest(CIPTest3000("test_3000_full_datasets"))
    # suite.addTest(CIPTest3000("test_3001_minimum_datasets"))
    # suite.addTest(TransfTest4100("test_4100_fullset"))
    # suite.addTest(TransfTest4100("test_4101_no_via"))
    # suite.addTest(TransfTest4100("test_4102_minimum"))
    # suite.addTest(TransfTest4100("test_4103_err_no_operation"))
    # suite.addTest(TransfTest4100("test_4104_err_no_destin"))
    # suite.addTest(FiltTest4200("test_4201_filt_full"))
    # suite.addTest(FiltTest4200("test_4202_filt_p_max"))
    # suite.addTest(FiltTest4200("test_4203_filt_min"))
    # suite.addTest(FiltTest4200("test_4204_no_equip"))
    # suite.addTest(FiltTest4200("test_4205_no_p_unit"))
    # suite.addTest(samplingTest4300("test_4301_full"))
    # suite.addTest(SamplingTest4300("test_4302_ipc_only"))
    # suite.addTest(SamplingTest4300("test_4303_monit_only"))
    # suite.addTest(SamplingTest4300("test_4304_noname_err"))
    # suite.addTest(SamplingTest4300("test_4305_no_ipc_crteria"))
    # suite.addTest(SamplingTest4300("test_4306_ipc_item_unit_mismatch"))
    # suite.addTest(SamplingTest4300("test_4307_ipc_criteria_item_mismatch"))
    # suite.addTest(SamplingTest4300("test_4308_monit_item_unit_mismatch"))


    return suite


if __name__=="__main__":
    unittest.TextTestRunner(verbosity=2).run(suite_0000_40000())



