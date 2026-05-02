import unittest
import pandas as pd
import flow_draw.definitions as defs
import flow_draw.batch.batch as batch
import flow_draw.batch.process.process as proc
import flow_draw.batch.process.unit_operations.charging as chgng
import flow_draw.materials.materials as mats
import os

class SaltyWaterFlow(unittest.TestCase):
    def setUp(self):
        # test_proc = proc.Process(project_name="flowtest000",process_name="salt water",num=1)
        # test_proc = proc.Process.__new__(proc.Process)
        # test_proc.project_name="flowtest000"
        # test_proc.process_name="salt water"
        # test_proc.num_uo = 1
        # test_proc.mats_data = mats.Materials(PrepSaltAndWater)
        # proj_name = "flowtest000"
        # proc_name = "salt_water"
        # tst_proc = proc.Process(process_name=proj_name, proc_name=proc_name,num_uo=1)
        # tst_proc.mats_data = mats.Materials(df_mats=PurchaseMaterials())
        # tst_chgng = chgng.Charging(caller=tst_proc,
        #                            flow_sheet=tst_proc.flowsheet,
        #                            operation_seq=1,
        #                            num_subitems=2,
        #                            edit_comment="put salt and water")
        # tst_proc.list_uo.append(tst_chgng)
        # tst_proc.list_uo[0].load_params_from_df(SetInputData)
        return super().setUp()
    
    def test0000_OutputFlow(self):
        proj_name = "flowtest000"
        proc_name = "salt_water"
        tst_proc = proc.Process(project_name=proj_name, process_name=proc_name,num_uo=1)
        tst_proc.mats_data = mats.Materials(df_mats=PurchaseMaterials())
        tst_chgng = chgng.Charging(caller=tst_proc,
                                    flow_sheet=tst_proc.flowsheet,
                                    operation_seq=1,
                                    num_subitems=2,
                                    edit_comment="put salt and water")
        tst_proc.list_uo.append(tst_chgng)
        tst_proc.list_uo[0].load_params_from_df(SetChgngForSaltWater())
        tst_proc.list_uo[0].output_unit_operation()
        tst_proc.flowsheet.save("test000_SaltWaterOutputFlow.xlsx")
        self.assertTrue(True)



    
    def test0001_Project(self):
        wrong_proj_name = "wrong_proj_name"
        right_proj_name = "right_proj_name"
        proc_name = "salt_water"
        test_proj = batch.Project()
        test_proj.proj_name = wrong_proj_name
        test_proj.num_procs = 1
        test_df = prep_test_df(proj_name=right_proj_name, proc_name=proc_name, num_uo=1)
        test_proj.load_outline(test_df)
        test_proc = test_proj.list_proc[0]
        result:bool = ((test_proj.num_procs==(len(test_df)-1)/2) and
                       (test_proc.project_name==right_proj_name) and
                       (test_proc.process_name==proc_name))
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


def prep_test_df(proj_name:str=None, proc_name:str=None, num_uo:int =0 )-> pd.DataFrame:
    dict0: dict[str, list[str|int]] ={0:[defs.hedr_io_proj_project_name,
                                            defs.hedr_io_proj_proC_name_stem.format(1),
                                            defs.hedr_io_proj_proC_num_uo_stem.format(1),
                                            defs.hedr_io_proj_proC_name_stem.format(2),
                                            defs.hedr_io_proj_proC_num_uo_stem.format(2)                                            ],
                                    1:[proj_name,
                                        proc_name,
                                        num_uo,
                                        proc_name,
                                        num_uo]}

    test_df = pd.DataFrame(dict0)
    print("in prep_test_df(): test_df")
    print(test_df)
    print("==========\n")
    test_df.index = test_df[0]
    print("in prep_test_df(): test_df re-indexed")
    print(test_df)
    print("==========\n")
    print("len(test_df): ", len(test_df))
    print("==========\n")
    return test_df





if __name__=="__main__":
    unittest.main()



