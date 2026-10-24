"""
Flowsheet output tests.
Every unit operation is loaded from a DataFrame, in the same shape as the detail input worksheet,
and the flowsheet is output through Process.output_flowsheet() so that the material quantities are calculated as in production.
The output files go to test/output_flowsheet/.
"""
import os
import unittest
import pandas as pd
import flow_draw.definitions as defs
import flow_draw.batch.process.process as proc
import flow_draw.batch.process.unit_operations.unit_operation as uo
import flow_draw.batch.process.unit_operations.material_input as matin
import flow_draw.batch.process.unit_operations.uo_charging as chgng
import flow_draw.batch.process.unit_operations.uo_cryst_wash as cwash
import flow_draw.batch.process.unit_operations.uo_placeholder as plchldr
import flow_draw.batch.process.unit_operations.uo_line_clearance as lnclnc
import flow_draw.batch.process.unit_operations.uo_inert_replacement as inert
import flow_draw.batch.process.unit_operations.uo_temp_control as tempr
import flow_draw.batch.process.unit_operations.uo_agitation as agit
import flow_draw.batch.process.unit_operations.uo_settling as stlng
import flow_draw.batch.process.unit_operations.uo_phase_discharge as phdisch
import flow_draw.batch.process.unit_operations.uo_evaporation as evap
import flow_draw.batch.process.unit_operations.uo_cip as cip
import flow_draw.batch.process.unit_operations.uo_transfer as trsf
import flow_draw.batch.process.unit_operations.uo_filtration as filt
import flow_draw.batch.process.unit_operations.uo_sampling as smplng
import flow_draw.batch.process.unit_operations.uo_filter_setup as fltsup
import flow_draw.batch.process.unit_operations.uo_drying as drying
import flow_draw.batch.process.unit_operations.uo_alloc as alloc
import flow_draw.batch.process.unit_operations.uo_tare as tare
from flow_draw.materials.materials import Materials


dir_output = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_flowsheet")
"""Directory for the flowsheets output by the tests."""

#Materials used throughout the tests
name_sm = "SM-A"
name_tgt = "TGT-B"
name_meoh = "MeOH"
name_water = "H2O"
name_naoh = "NaOH"
gross_kg_sm = 10.0
assay_sm = 95.0
mw_sm = 200.0
mw_tgt = 250.0


#########################################################
# Helpers
#########################################################
def make_mats_df(with_tgt: bool = True) -> pd.DataFrame:
    """Materials table for the tests. The target material is optional."""
    df = Materials.generate_mats_df()
    df = Materials.add_to_mats_df(mats_df=df, material=name_sm, sm_tgt=defs.itm_io_mats_sm,
                                  mw=mw_sm, density=1.2, conc_assay=assay_sm, kg_sm=gross_kg_sm, remark="Starting material")
    if with_tgt:
        df = Materials.add_to_mats_df(mats_df=df, material=name_tgt, sm_tgt=defs.itm_io_mats_tgt,
                                      mw=mw_tgt, remark="Target material")
    df = Materials.add_to_mats_df(mats_df=df, material=name_meoh, mw=32.04, density=0.792, conc_assay=100.0)
    df = Materials.add_to_mats_df(mats_df=df, material=name_water, mw=18.02, density=1.0, conc_assay=100.0)
    df = Materials.add_to_mats_df(mats_df=df, material=name_naoh, mw=40.0, density=1.5, conc_assay=48.0, remark="48% aq.")
    return df


def make_detail_df(hedr: list[str], rows: list[dict]) -> pd.DataFrame:
    """
    Detail input DataFrame for a unit operation which has no generate_test_df().
    hedr is the UO-specific header list. Each dict in rows is a row on the worksheet; missing items are left empty.
    """
    cols = defs.list_hedr_cmn_io_dtil + hedr
    return pd.DataFrame([{col: row.get(col, None) for col in cols} for row in rows], columns=cols)


#########################################################
# Base class
#########################################################
class FlowsheetTestBase(unittest.TestCase):
    """
    Each test builds a Process, adds unit operations from DataFrames with add_uo() and calls output().
    """
    mats_with_tgt: bool = False
    """
    Set True in a derived class to put the target material in the materials table.
    The target material is linked to the starting material inputs, hence the process needs to charge the starting material.
    """

    def setUp(self):
        os.makedirs(dir_output, exist_ok=True)
        self.test_name: str = self.id().split('.')[-1]
        self.proc = proc.Process(process_name=self.test_name)
        self.proc.mats_data = Materials(make_mats_df(with_tgt=self.mats_with_tgt))

    def add_uo(self, uo_cls: type[uo.UnitOperation], df: pd.DataFrame,
               precomment: str = None, postcomment: str = None, edit_comment: str = None) -> uo.UnitOperation:
        """
        Fills the common columns as the worksheet does, loads df to a new instance of uo_cls and appends it to the process.
        """
        seq = len(self.proc.seq_uo) + 1
        inst = uo_cls(caller=self.proc,
                      flowsheet=self.proc.flowsheet,
                      operation_seq=seq,
                      num_subitems=len(df),
                      edit_comment=edit_comment)
        df = df.copy()
        for col in defs.list_hedr_cmn_io_dtil:
            if col not in df.columns:
                df[col] = None
        df[defs.hedr_cmn_io_dtil_seq] = seq
        df[defs.hedr_cmn_io_dtil_uo] = inst.uo_tag
        df[defs.hedr_cmn_io_dtil_edt_cmnt] = edit_comment
        if precomment is not None:
            df.at[df.index[0], defs.hedr_cmn_io_dtil_precmnt] = precomment
        if postcomment is not None:
            df.at[df.index[0], defs.hedr_cmn_io_dtil_postcmnt] = postcomment
        inst.load_params_from_df(df)
        self.proc.seq_uo.append(inst)
        return inst

    def output(self) -> str:
        """Calculates the quantities and saves the flowsheet as <test name>.xlsx. Returns the path."""
        path = os.path.join(dir_output, self.test_name + ".xlsx")
        self.proc.output_flowsheet(file_name=path)
        self.assertTrue(os.path.exists(path))
        return path

    def get_input(self, id_input: int) -> matin.Input:
        return self.proc.get_input(id_input=id_input)


#########################################################
# 1000: Unit operations without material inputs
#########################################################
class UnitOperationOutputTest1000(FlowsheetTestBase):
    def test_1001_placeholder(self):
        df = make_detail_df(plchldr.list_hedr, [{plchldr.hedr_lines: 3}])
        self.add_uo(plchldr.Placeholder, df,
                    precomment='Test 1001 precomment\nTest 1001 additional precomment (line-2)',
                    postcomment='Test 1001 postcomment')
        self.output()

    def test_1002_line_clearance(self):
        df = make_detail_df(lnclnc.list_hedr, [{lnclnc.hedr_sop: "TEST SOP"}])
        self.add_uo(lnclnc.LineClearance, df)
        self.output()

    def test_1003_inert_replace(self):
        df = make_detail_df(inert.list_hedr, [{inert.hedr_gas: inert.opt_gas_Ar,
                                               inert.hedr_neg_pres: -0.08,
                                               inert.hedr_num_repeat: 2}])
        self.add_uo(inert.InertReplacement, df)
        self.output()

    def test_1004_temp_ctrl_prog_mode(self):
        df = make_detail_df(tempr.list_hedr, [{tempr.hedr_mode: tempr.opt_mode_prog,
                                               tempr.hedr_Ti_sp: 10.0,
                                               tempr.hedr_prog_time_val: 1.0,
                                               tempr.hedr_prog_time_unit: tempr.opt_time_unit_hour,
                                               tempr.hedr_Ti_limit_low: 5.0,
                                               tempr.hedr_Ti_limit_high: 15.0,
                                               tempr.hedr_Tj_limit_low: 0.0,
                                               tempr.hedr_Tj_limit_high: 30.0}])
        self.add_uo(tempr.TempControl, df)
        self.output()

    def test_1005_temp_ctrl_TiTj_mode(self):
        df = make_detail_df(tempr.list_hedr, [{tempr.hedr_mode: tempr.opt_mode_TiTj,
                                               tempr.hedr_Ti_sp: 30.0,
                                               tempr.hedr_Tj_limit_low: 20.0,
                                               tempr.hedr_Tj_limit_high: 35.0,
                                               tempr.hedr_Ti_limit_low: 25.0,
                                               tempr.hedr_Ti_limit_high: 35.0,
                                               tempr.hedr_Ti_tgt_low: 27.5,
                                               tempr.hedr_Ti_tgt_high: 32.5,
                                               tempr.hedr_endpoint_check: tempr.opt_check_endpoint_yes}])
        self.add_uo(tempr.TempControl, df, precomment="Pre-comment line-1\nPre-comment line-2")
        self.output()

    def test_1006_temp_ctrl_Tj_mode(self):
        df = make_detail_df(tempr.list_hedr, [{tempr.hedr_mode: tempr.opt_mode_Tj,
                                               tempr.hedr_Ti_sp: 30.0,
                                               tempr.hedr_Tj_sp: 30.0,
                                               tempr.hedr_endpoint_check: tempr.opt_check_endpoint_yes}])
        self.add_uo(tempr.TempControl, df, precomment="Pre-comment line-1\nPre-comment line-2")
        self.output()

    def test_1007_temp_ctrl_Ti_mode(self):
        df = make_detail_df(tempr.list_hedr, [{tempr.hedr_mode: tempr.opt_mode_Ti,
                                               tempr.hedr_Ti_sp: 40.0,
                                               tempr.hedr_Tj_sp: 30.0,
                                               tempr.hedr_Ti_limit_low: 35.0,
                                               tempr.hedr_Ti_limit_high: 45.0,
                                               tempr.hedr_Ti_tgt_low: 37.5,
                                               tempr.hedr_Ti_tgt_high: 42.5,
                                               tempr.hedr_endpoint_check: tempr.opt_check_endpoint_yes}])
        self.add_uo(tempr.TempControl, df, precomment="Pre-comment line-1\nPre-comment line-2")
        self.output()

    def test_1008_temp_ctrl_no_mode_err(self):
        df = make_detail_df(tempr.list_hedr, [{tempr.hedr_Ti_sp: 40.0}])
        with self.assertRaises(ValueError):
            self.add_uo(tempr.TempControl, df)

    def test_1010_agit_full(self):
        df = make_detail_df(agit.list_hedr, [{agit.hedr_spec_agit: agit.opt_spec_guide,
                                              agit.hedr_rpm: 80.0,
                                              agit.hedr_Ti_min: 35.0,
                                              agit.hedr_Ti_max: 45.0,
                                              agit.hedr_time_min: 1.0,
                                              agit.hedr_time_max: 1.0,
                                              agit.hedr_time_unit: agit.opt_time_unit_hour,
                                              agit.hedr_dissolution_check: agit.opt_yes}])
        self.add_uo(agit.Agitation, df)
        self.output()

    def test_1011_agit_minimal(self):
        df = make_detail_df(agit.list_hedr, [{agit.hedr_spec_agit: agit.opt_spec_guide,
                                              agit.hedr_rpm: 80.0}])
        self.add_uo(agit.Agitation, df)
        self.output()

    def test_1012_agit_no_spec_err(self):
        df = make_detail_df(agit.list_hedr, [{agit.hedr_rpm: 80.0}])
        with self.assertRaises(RuntimeError):
            self.add_uo(agit.Agitation, df)

    def test_1020_settling_full(self):
        df = make_detail_df(stlng.list_hedr, [{stlng.hedr_time_min: 1.0,
                                               stlng.hedr_time_max: 1.0,
                                               stlng.hedr_time_unit: stlng.opt_time_unit_second,
                                               stlng.hedr_Ti_min: 20.0,
                                               stlng.hedr_Ti_max: 30.0}])
        self.add_uo(stlng.Settling, df)
        self.output()

    def test_1021_settling_minimal(self):
        df = make_detail_df(stlng.list_hedr, [{}])
        self.add_uo(stlng.Settling, df)
        self.output()

    def test_1030_phase_disch_full(self):
        df = make_detail_df(phdisch.list_hedr, [{phdisch.hedr_origin: "RV_ORIG",
                                                 phdisch.hedr_via: "Multiplexer",
                                                 phdisch.hedr_destin: "Destin tank 1"},
                                                {phdisch.hedr_destin: "Destin tank 2"}])
        inst = self.add_uo(phdisch.PhaseDisch, df, precomment="Pre-comment-1\nPre-comment-2", postcomment="Post-comment")
        self.assertEqual(inst.destin, ["Destin tank 1", "Destin tank 2"])
        self.output()

    def test_1031_phase_disch_minimal(self):
        df = make_detail_df(phdisch.list_hedr, [{phdisch.hedr_destin: "Destin tank"}])
        self.add_uo(phdisch.PhaseDisch, df)
        self.output()


#########################################################
# 2000: Evaporation
#########################################################
class EvaporationTest2000(FlowsheetTestBase):
    def __full_df(self, **kwargs) -> pd.DataFrame:
        params = dict(precomment="precomment for evaporation",
                      postcomment="postcomment for evaporation",
                      Tj_min=50.0, Tj_max=100.0,
                      Tbr_min=-25, Tbr_max=5,
                      press_ctrl=evap.opt_press_ctrl_specific,
                      press_min=0.0, press_max=1.0,
                      unit_press=evap.opt_press_unit_kPaA,
                      agit_spec=evap.opt_agit_spec_guide, agit_rpm=30.0,
                      vw_spec_min=10, vw_spec_max=15.0,
                      vw_guide_min=11.0, vw_guide_max=12.0)
        params.update(kwargs)
        return evap.Evaporation.generate_test_df(**params)

    def test_2000_full(self):
        inst = self.add_uo(evap.Evaporation, self.__full_df())
        #The end point volume is calculated from the net weight of the starting material.
        self.assertAlmostEqual(inst.end_volume_spec_min, gross_kg_sm * assay_sm / 100.0 * 10)
        self.output()

    def test_2001_press_discrepancy_err(self):
        with self.assertRaises(ValueError):
            self.add_uo(evap.Evaporation, self.__full_df(press_min=None, press_max=None))

    def test_2002_no_press_unit_err(self):
        with self.assertRaises(ValueError):
            self.add_uo(evap.Evaporation, self.__full_df(unit_press=None))

    def test_2003_no_endpoint_err(self):
        self.add_uo(evap.Evaporation, self.__full_df(vw_spec_min=None, vw_spec_max=None, vw_guide_min=None, vw_guide_max=None))
        with self.assertRaises(ValueError):
            self.output()

    def test_2004_minimum(self):
        df = evap.Evaporation.generate_test_df(Tj_min=50.0, Tbr_max=5, vw_guide_max=12.0)
        self.add_uo(evap.Evaporation, df)
        self.output()


#########################################################
# 3000: CIP
#########################################################
class CIPTest3000(FlowsheetTestBase):
    def test_3000_full(self):
        df = cip.CIP.generate_test_df(precomment="Pre-comment for test-3000",
                                      postcomment="Post-comment for test-3000",
                                      cip_tgt="大きな釜", solvent=name_water, qty_kg=10, via="multiplexer")
        cip.CIP.add_to_test_df(df=df, cip_tgt="大きな釜", solvent=name_meoh, qty_kg=15, via="multiplexer")
        self.add_uo(cip.CIP, df)
        self.output()

    def test_3001_minimum(self):
        df = cip.CIP.generate_test_df(cip_tgt="大きな釜", solvent=name_water, qty_kg=10)
        cip.CIP.add_to_test_df(df=df, cip_tgt="大きな釜", solvent=name_meoh, qty_kg=15)
        self.add_uo(cip.CIP, df)
        self.output()


#########################################################
# 4100: Transfer
#########################################################
class TransferTest4100(FlowsheetTestBase):
    def test_4100_full(self):
        self.add_uo(trsf.Transfer, trsf.Transfer.generate_test_df(operation=trsf.opt_operation_setup,
                                                                  origin="Setup test origin",
                                                                  via="Setup test waypoint",
                                                                  destination="Setup test destination",
                                                                  filter="Setup test filter"))
        self.add_uo(trsf.Transfer, trsf.Transfer.generate_test_df(operation=trsf.opt_operation_transfer,
                                                                  origin="Transf test origin",
                                                                  via="Transf test waypoint",
                                                                  destination="Transf test destination",
                                                                  filter="Transf test filter"))
        self.output()

    def test_4101_no_via(self):
        self.add_uo(trsf.Transfer, trsf.Transfer.generate_test_df(operation=trsf.opt_operation_setup,
                                                                  origin="Setup test origin",
                                                                  destination="Setup test destination",
                                                                  filter="Setup test filter"))
        self.add_uo(trsf.Transfer, trsf.Transfer.generate_test_df(operation=trsf.opt_operation_transfer,
                                                                  origin="Transf test origin",
                                                                  destination="Transf test destination",
                                                                  filter="Transf test filter"))
        self.output()

    def test_4102_minimum(self):
        self.add_uo(trsf.Transfer, trsf.Transfer.generate_test_df(operation=trsf.opt_operation_setup,
                                                                  destination="Setup test destination"))
        self.add_uo(trsf.Transfer, trsf.Transfer.generate_test_df(operation=trsf.opt_operation_transfer,
                                                                  destination="Transf test destination"))
        self.output()

    def test_4103_no_operation_err(self):
        with self.assertRaises(ValueError):
            self.add_uo(trsf.Transfer, trsf.Transfer.generate_test_df(destination="Setup test destination"))

    def test_4104_no_destination_err(self):
        with self.assertRaises(ValueError):
            self.add_uo(trsf.Transfer, trsf.Transfer.generate_test_df(operation=trsf.opt_operation_setup,
                                                                      origin="Setup test origin"))


#########################################################
# 4200: Filtration
#########################################################
class FiltrationTest4200(FlowsheetTestBase):
    def test_4201_full(self):
        df = filt.Filtration.generate_test_df(equipment="test_4201_FD", Tj=25, P_min=100, P_max=100,
                                              P_unit=filt.opt_hedr_press_kPa, integ_test=filt.opt_integ_test_yes)
        self.add_uo(filt.Filtration, df)
        self.output()

    def test_4202_p_max_only(self):
        df = filt.Filtration.generate_test_df(equipment="test_4202_FD", Tj=25, P_max=100,
                                              P_unit=filt.opt_hedr_press_kPa, integ_test=filt.opt_integ_test_yes)
        self.add_uo(filt.Filtration, df)
        self.output()

    def test_4203_minimum(self):
        self.add_uo(filt.Filtration, filt.Filtration.generate_test_df(equipment="test_4203_FD"))
        self.output()

    def test_4204_no_equipment_err(self):
        df = filt.Filtration.generate_test_df(Tj=25, P_min=100, P_max=100,
                                              P_unit=filt.opt_hedr_press_kPa, integ_test=filt.opt_integ_test_yes)
        with self.assertRaises(ValueError):
            self.add_uo(filt.Filtration, df)

    def test_4205_no_press_unit_err(self):
        df = filt.Filtration.generate_test_df(equipment="test_4205_FD", Tj=25, P_min=100, P_max=100,
                                              integ_test=filt.opt_integ_test_yes)
        with self.assertRaises(ValueError):
            self.add_uo(filt.Filtration, df)


#########################################################
# 4300: Sampling
#########################################################
class SamplingTest4300(FlowsheetTestBase):
    def test_4301_full(self):
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
        self.add_uo(smplng.Sampling, df)
        self.output()

    def test_4302_ipc_only(self):
        df = smplng.Sampling.generate_test_df(sample_name="test sample 1",
                                              sampling_cat=smplng.opt_sampling_cat_ipc,
                                              ipc_criteria="残原料1:≦0.5%",
                                              ipc_rec_titles="残原料1",
                                              ipc_rec_units="%",
                                              sample_comment="This is a comment for sample test 4302.")
        self.add_uo(smplng.Sampling, df)
        self.output()

    def test_4303_monit_only(self):
        df = smplng.Sampling.generate_test_df(sample_name="test sample 1",
                                              sampling_cat=smplng.opt_sampling_cat_monit,
                                              monit_items="酸性度",
                                              monit_rec_items="pH",
                                              monit_rec_units="",
                                              sample_comment="This is a comment for sample test 4303.")
        self.add_uo(smplng.Sampling, df)
        self.output()

    def test_4304_no_name_err(self):
        df = smplng.Sampling.generate_test_df(sampling_cat=smplng.opt_sampling_cat_monit,
                                              monit_items="酸性度",
                                              monit_rec_items="pH",
                                              monit_rec_units="")
        with self.assertRaises(ValueError):
            self.add_uo(smplng.Sampling, df)

    def test_4305_no_ipc_criteria_err(self):
        df = smplng.Sampling.generate_test_df(sample_name="test sample 1",
                                              sampling_cat=smplng.opt_sampling_cat_ipc,
                                              ipc_rec_titles="残原料1",
                                              ipc_rec_units="%")
        with self.assertRaises(ValueError):
            self.add_uo(smplng.Sampling, df)

    def test_4306_ipc_item_unit_mismatch_err(self):
        df = smplng.Sampling.generate_test_df(sample_name="test sample 1",
                                              sampling_cat=smplng.opt_sampling_cat_ipc,
                                              ipc_criteria="残原料1:≦0.5%",
                                              ipc_rec_titles="残原料1\n残原料2",
                                              ipc_rec_units="%")
        with self.assertRaises(ValueError):
            self.add_uo(smplng.Sampling, df)

    def test_4307_ipc_criteria_item_mismatch_err(self):
        df = smplng.Sampling.generate_test_df(sample_name="test sample 1",
                                              sampling_cat=smplng.opt_sampling_cat_ipc,
                                              ipc_criteria="残原料1:≦0.5%\n残原料2≦0.1%",
                                              ipc_rec_titles="残原料1",
                                              ipc_rec_units="%")
        with self.assertRaises(ValueError):
            self.add_uo(smplng.Sampling, df)

    def test_4308_monit_item_unit_mismatch_err(self):
        df = smplng.Sampling.generate_test_df(sample_name="test sample 1",
                                              sampling_cat=smplng.opt_sampling_cat_monit,
                                              monit_items="酸性度",
                                              monit_rec_items="pH")
        with self.assertRaises(ValueError):
            self.add_uo(smplng.Sampling, df)


#########################################################
# 4400 - 4700: Filter setup, drying, allocation, tare
#########################################################
class FiltSetupTest4400(FlowsheetTestBase):
    def test_4400_full(self):
        df = fltsup.FiltSetup.generate_test_df(equip_id="test_4400_FD",
                                               filt_cloth="FC-4400",
                                               num_cloth=1,
                                               bag_filter="BF-4400",
                                               press_leak_test="0.1",
                                               press_drop_leak_test="0.01",
                                               time_leak_test="10",
                                               unit_press='MPa')
        self.add_uo(fltsup.FiltSetup, df, edit_comment="This is a comment for test 4400.")
        self.output()


class DryingTest4500(FlowsheetTestBase):
    def test_4500_full(self):
        df = drying.Drying.generate_test_df(precomment="Pre-comment for test-4500",
                                            postcomment="Post-comment for test-4500",
                                            Tj_ctrl_cat="Tj_ctrl_arbitrary",
                                            Tj_low=50.0,
                                            Tj_high=80.0,
                                            Tbr_low=-20.0,
                                            Tbr_high=5.0,
                                            mode_vac="range",
                                            pres_low=0.0,
                                            pres_high=0.05,
                                            intermission="Yes",
                                            test_cat="ipc",
                                            test_item="KF",
                                            test_val_tgt_criterion=5.0,
                                            test_unit_val="%")
        drying.Drying.add_to_test_df(df=df, test_cat="monit_with_tgt", test_item="THF",
                                     test_val_tgt_criterion=100, test_unit_val="ppm")
        drying.Drying.add_to_test_df(df=df, test_cat="monit_no_tgt", test_item="pH")
        self.add_uo(drying.Drying, df)
        self.output()


class AllocTest4600(FlowsheetTestBase):
    def test_4600_full(self):
        df = alloc.Alloc.generate_test_df(precomment="Pre-comment for test-4600",
                                          postcomment="Post-comment for test-4600",
                                          prod_cell="Cell-4600",
                                          op_resouce="Operator-4600")
        self.add_uo(alloc.Alloc, df, edit_comment="This is a comment for test 4600.")
        self.output()


class TareTest4700(FlowsheetTestBase):
    def test_4700_full(self):
        df = tare.Tare.generate_test_df(precomment="This is a pre-comment for test 4700.",
                                        pkg_location="Some location",
                                        pkg_material=tare.opt_pkg_polym_bag,
                                        num_pkg=5,
                                        postcomment="This is a post-comment for test 4700.")
        self.add_uo(tare.Tare, df, edit_comment="This is a comment for test 4700.")
        self.output()


#########################################################
# 5000: Charging (material inputs)
#########################################################
def charge_sm_df(id_input: int = 0) -> pd.DataFrame:
    """A charging DataFrame for the whole starting material (1.0 equiv)."""
    return matin.Input.generate_test_df(material_name=name_sm, metrics_val=1.0, metrics_unit=matin.opt_mtrcs_eq,
                                        error_pct=1.0, method=matin.method_pow, vessel_train=["R-1"],
                                        id_input=id_input)


class ChargingTest5000(FlowsheetTestBase):
    mats_with_tgt = True

    def test_5000_sm_and_solvent(self):
        df = charge_sm_df()
        matin.Input.add_to_test_df(df=df, material_name=name_water, metrics_val=5.0, metrics_unit=matin.opt_mtrcs_v_per_w,
                                   method=matin.method_liq, vessel_train=["R-1"], id_input=1, list_id_basis_input=[0],
                                   temp_control=matin.temprctrl_min_max, temp_min=15.0, temp_max=25.0)
        self.add_uo(chgng.Charging, df, precomment="Charge the starting material and water.")
        self.output()
        self.assertAlmostEqual(self.get_input(0).qty_kg_gross, gross_kg_sm)
        #5 v/w against the net weight of SM. Water: density 1.0, assay 100%
        self.assertAlmostEqual(self.get_input(1).qty_kg_gross, gross_kg_sm * assay_sm / 100.0 * 5.0)

    def test_5001_equiv_with_time_control(self):
        self.add_uo(chgng.Charging, charge_sm_df())
        df = matin.Input.generate_test_df(material_name=name_naoh, metrics_val=2.0, metrics_unit=matin.opt_mtrcs_eq,
                                          method=matin.method_press, vessel_train=["V-1", "R-1"], id_input=1, list_id_basis_input=[0],
                                          time_control=matin.timectrl_min_max, time_min=30, time_max=60,
                                          temp_control=matin.temprctrl_max, temp_max=30.0)
        self.add_uo(chgng.Charging, df)
        self.output()
        #2.0 equiv of SM in mol, 48% aq. solution
        mol_sm = gross_kg_sm * assay_sm / 100.0 * 1000.0 / mw_sm
        self.assertAlmostEqual(self.get_input(1).qty_kg_gross, mol_sm * 2.0 * 40.0 / 1000.0 / 0.48)

    def test_5002_based_on_tgt(self):
        self.add_uo(chgng.Charging, charge_sm_df())
        df = matin.Input.generate_test_df(material_name=name_meoh, metrics_val=3.0, metrics_unit=matin.opt_mtrcs_v_per_w,
                                          method=matin.method_mobile_tank, vessel_train=["R-1"], id_input=1,
                                          list_id_basis_input=[matin.opt_special_id_basis_tgt])
        self.add_uo(chgng.Charging, df)
        self.output()
        self.assertIsNotNone(self.get_input(1).qty_kg_gross)

    def test_5003_duplicated_id_err(self):
        df = charge_sm_df()
        matin.Input.add_to_test_df(df=df, material_name=name_water, metrics_val=5.0, metrics_unit=matin.opt_mtrcs_v_per_w,
                                   method=matin.method_liq, id_input=0, list_id_basis_input=[0])
        self.add_uo(chgng.Charging, df)
        with self.assertRaises(RuntimeError):
            self.output()


class ChargingNoTgtTest5100(FlowsheetTestBase):
    def test_5100_no_tgt(self):
        df = charge_sm_df()
        matin.Input.add_to_test_df(df=df, material_name=name_water, metrics_val=5.0, metrics_unit=matin.opt_mtrcs_v_per_w,
                                   method=matin.method_liq, id_input=1, list_id_basis_input=[0])
        self.add_uo(chgng.Charging, df)
        self.output()
        self.assertEqual(len(self.proc.list_inpts), 2)

    def test_5101_based_on_missing_tgt_err(self):
        df = charge_sm_df()
        matin.Input.add_to_test_df(df=df, material_name=name_meoh, metrics_val=3.0, metrics_unit=matin.opt_mtrcs_v_per_w,
                                   method=matin.method_liq, id_input=1, list_id_basis_input=[matin.opt_special_id_basis_tgt])
        self.add_uo(chgng.Charging, df)
        with self.assertRaises(RuntimeError):
            self.output()


#########################################################
# 5200: Crystal washing (material inputs)
#########################################################
class CrystWashingTest5200(FlowsheetTestBase):
    mats_with_tgt = True

    def __wash_df(self, mode: str) -> pd.DataFrame:
        df = cwash.CrystWashing.generate_test_df(precomment=f"Pre-comment for washing: {mode}",
                                                 equipment="FD-1",
                                                 mode_washing=mode,
                                                 duration_minutes=30,
                                                 agitation_rpm=60,
                                                 material_name=name_meoh, metrics_val=2.0, metrics_unit=matin.opt_mtrcs_v_per_w,
                                                 method=matin.method_shower, vessel_train=["R-1"],
                                                 id_input=1, list_id_basis_input=[0])
        cwash.CrystWashing.add_to_test_df(df=df, material_name=name_water, metrics_val=1.0, metrics_unit=matin.opt_mtrcs_v_per_w,
                                          method=matin.method_liq, id_input=2, list_id_basis_input=[0])
        return df

    def __run_mode(self, mode: str):
        self.add_uo(chgng.Charging, charge_sm_df())
        inst = self.add_uo(cwash.CrystWashing, self.__wash_df(mode))
        self.output()
        self.assertEqual([i.material_name for i in inst.get_list_inputs()], [name_meoh, name_water])
        #The washing equipment is appended to the vessel train.
        self.assertEqual(self.get_input(1).vessel_train, ["R-1", "FD-1"])
        self.assertAlmostEqual(self.get_input(2).qty_kg_gross, gross_kg_sm * assay_sm / 100.0 * 1.0)

    def test_5200_reslurry(self):
        self.__run_mode(cwash.opt_washmode_reslurry)

    def test_5201_soak(self):
        self.__run_mode(cwash.opt_washmode_soak)

    def test_5202_displacement(self):
        self.__run_mode(cwash.opt_washmode_displacement)

    def test_5203_placeholder(self):
        self.__run_mode(cwash.opt_washmode_placeholder)

    def test_5204_no_equipment(self):
        df = cwash.CrystWashing.generate_test_df(material_name=name_meoh, metrics_val=2.0, metrics_unit=matin.opt_mtrcs_v_per_w,
                                                 method=matin.method_shower, id_input=1, list_id_basis_input=[0])
        self.add_uo(chgng.Charging, charge_sm_df())
        inst = self.add_uo(cwash.CrystWashing, df)
        self.output()
        self.assertEqual(inst.equipment, cwash.dict_parts_stcs[cwash.tag_part_val_equipment_plchldr])


#########################################################
# 6000: A process with several unit operations
#########################################################
class ProcessTest6000(FlowsheetTestBase):
    mats_with_tgt = True

    @unittest.expectedFailure
    def test_6001_tgt_without_sm_input(self):
        """
        Current behaviour: the target material has no basis to link to when no starting material is charged in the process,
        and Input.link_inputs() raises RuntimeError. Remove expectedFailure once the behaviour is decided and implemented.
        """
        self.add_uo(lnclnc.LineClearance, make_detail_df(lnclnc.list_hedr, [{lnclnc.hedr_sop: "SOP-001"}]))
        self.output()

    def test_6000_crystallization_and_isolation(self):
        self.add_uo(lnclnc.LineClearance, make_detail_df(lnclnc.list_hedr, [{lnclnc.hedr_sop: "SOP-001"}]))
        self.add_uo(inert.InertReplacement, make_detail_df(inert.list_hedr, [{inert.hedr_gas: inert.opt_gas_N2,
                                                                               inert.hedr_neg_pres: -0.08,
                                                                               inert.hedr_num_repeat: 3}]))
        df = charge_sm_df()
        matin.Input.add_to_test_df(df=df, material_name=name_meoh, metrics_val=8.0, metrics_unit=matin.opt_mtrcs_v_per_w,
                                   method=matin.method_mobile_tank, vessel_train=["R-1"], id_input=1, list_id_basis_input=[0])
        self.add_uo(chgng.Charging, df)
        self.add_uo(tempr.TempControl, make_detail_df(tempr.list_hedr, [{tempr.hedr_mode: tempr.opt_mode_Ti,
                                                                          tempr.hedr_Ti_sp: 60.0,
                                                                          tempr.hedr_Ti_limit_low: 55.0,
                                                                          tempr.hedr_Ti_limit_high: 65.0,
                                                                          tempr.hedr_endpoint_check: tempr.opt_check_endpoint_yes}]))
        self.add_uo(agit.Agitation, make_detail_df(agit.list_hedr, [{agit.hedr_spec_agit: agit.opt_spec_guide,
                                                                      agit.hedr_rpm: 100.0,
                                                                      agit.hedr_dissolution_check: agit.opt_yes}]))
        self.add_uo(evap.Evaporation, evap.Evaporation.generate_test_df(Tj_min=50.0, Tj_max=70.0, Tbr_max=5,
                                                                         vw_guide_min=4.0, vw_guide_max=5.0))
        self.add_uo(trsf.Transfer, trsf.Transfer.generate_test_df(operation=trsf.opt_operation_transfer,
                                                                  origin="R-1", destination="FD-1"))
        self.add_uo(filt.Filtration, filt.Filtration.generate_test_df(equipment="FD-1"))
        wash = cwash.CrystWashing.generate_test_df(equipment="FD-1", mode_washing=cwash.opt_washmode_reslurry,
                                                   duration_minutes=30, agitation_rpm=60,
                                                   material_name=name_meoh, metrics_val=2.0, metrics_unit=matin.opt_mtrcs_v_per_w,
                                                   method=matin.method_shower, vessel_train=["R-1"],
                                                   id_input=2, list_id_basis_input=[matin.opt_special_id_basis_tgt])
        self.add_uo(cwash.CrystWashing, wash)
        self.add_uo(drying.Drying, drying.Drying.generate_test_df(Tj_ctrl_cat="Tj_ctrl_arbitrary", Tj_low=40.0, Tj_high=60.0,
                                                                  mode_vac="full_vacuum", test_cat="ipc", test_item="LOD",
                                                                  test_val_tgt_criterion=0.5, test_unit_val="%"))
        self.add_uo(tare.Tare, tare.Tare.generate_test_df(num_pkg=2))
        self.output()
        self.assertEqual(len(self.proc.seq_uo), 11)
        #SM, MeOH for charging, MeOH for washing and TGT
        self.assertEqual(len(self.proc.list_inpts), 4)


def suite_selected() -> unittest.TestSuite:
    """Test classes to run when this file is executed directly. Add or remove classes as needed."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(CrystWashingTest5200))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite_selected())
