#########################################################
# imports
#########################################################
import pandas as pd
import warnings
import flow_draw.definitions as defs
import flow_draw.data_io.flowsheet as fsht
from typing import Optional
from typing import Literal
from flow_draw.batch.process.unit_operations import unit_operation as uo
from flow_draw.data_io import process_io as procio
from flow_draw.materials import materials as mats
from flow_draw.trait_def import trait_def as trdef
#from flow_draw.trait_def.trait_def import GetMats
from flow_draw.data_io.json_io import Objason, Array, Primitive



#########################################################
# Common items: headers etc
#########################################################
hedr_precomment:str = defs.hedr_cmn_io_dtil_precmnt #Don't include this in the specific header list!!!
"""A common header item: header for unit operation precomment"""
hedr_postcomment:str = defs.hedr_cmn_io_dtil_postcmnt #Don't include this in the specific header list!!!
"""A common header item: header for unit operation postcomment"""

        #### Common option items for the detail input table #####
opt_yes:str = defs.opt_yes
"""Affirmative option for various user choice."""
opt_no: str = defs.opt_no
"""Negative option for various user coice"""

opt_time_unit_second:str = defs.tag_flow_cmn_time_unit_second
"""Tag for a common flowsheet component for an unit of time: second"""
opt_time_unit_minute:str = defs.tag_flow_cmn_time_unit_minute
"""Tag for a common flowsheet component for an unit of time: minute"""
opt_time_unit_hour:str = defs.tag_flow_cmn_time_unit_hour
"""Tag for a common flowsheet component for an unit of time: hour"""

#########################################################
# UO-specific hader items and list thereof
#########################################################
#hedr_<something> = defs.hedr_<unit operation>_<specification item>
#list_hedr = defs.list_hedr_<list of header items for the uo>
#dict_dtil_drpdwn = defs.dict_opt_<unit operation>

"""
Here, header items to hold pieces of information for the filter dryer set-up shall be placed. The following ithems have to be collected to complete the unit operation block:
-ID of the filtering equipment.
-Type/catalog code of the filter cloth.
-Number of the filter cloths.
-Type/catalog code of the bag filter.
""" 

hedr_Tj_ctrl_cat:str = "Tj_ctrl_cat"
"""Header item for uo_drying. The category of the filter dryer jacket temperature control. Options are "spec", "arbitrary", and "guide"."""
hedr_Tj_low:str = "Tj_low_drying"
"""Header item for uo_drying. The lower limit of the filter dryer jacket temperature. The unit is in degree Celsius. Nullable where appropriate."""
hedr_Tj_high:str = "Tj_high_drying"
"""Header item for uo_drying. The upper limit of the filter dryer jacket temperature. The unit is in degree Celsius. Nullable where appropriate."""

hedr_Tbr_low:str = "Tbr_low"
"""Header item for uo_drying. The lower limit of the condenser brine temeprature. The unit is in degree Celsius. Nullable where appropriate."""
hedr_Tbr_high:str = "Tbr_high"
"""Header item for uo_drying. The upper limit of the condenser brine temeprature. The unit is in degree Celsius. Nullable where appropriate."""

hedr_mode_vac:str = "mode_vac"
"""Header item for uo_drying. The mode vacuum for the filter dryer. Options are "arbitrary", "range", and "full_vacuum"."""
hedr_pres_low:str = "pres_low"
"""Header item for uo_drying. The lower limit of the filter dryer pressure in MPaG unit."""
hedr_pres_high:str = "pres_high"
"""Header item for uo_drying. The upper limit of the filter dryer pressure in MPaG unit."""

hedr_rpm_min:str = "rpm_min"
"""Header item for uo_drying. The minimum rotational speed of the drying equipment in RPM. Nullable where appropriate."""
hedr_rpm_max:str = "rpm_max"
"""Header item for uo_drying. The maximum rotational speed of the drying equipment in RPM. Nullable where appropriate."""


hedr_intermission:str = "intermission_drying"
"""Header item for uo_drying. Intermission of the drying is allowed or not. Options are "yes" and "no"."""

hedr_test_cat:str = "test_cat"
"""Header item for uo_drying. The test category for drying. Options are "IPC", "monit_no_tgt", "monit_with_tgt"."""
hedr_test_item:str = "test_item"
"""Header item for uo_drying. The test item for drying."""
hedr_test_val_tgt_criterion:str = "test_tgt_criterion"
"""Header item for uo_drying. The target criterion for the test item for drying. Nullable where appropriate."""
hedr_test_unit:str = "test_unit"
"""Header item for uo_drying. The unit for the value of the test target, criterion, and the result."""

key_json_obj_test:str = "test_drying"
"""Key for the JSON object for the test description for drying operation."""
key_json_arr_test:str = "list_test_drying"
"""Key for the JSON array for the list of test description for drying operation."""


list_uo_specif_hedr:list[str] = [hedr_Tj_low,
                       hedr_Tj_high,
                       hedr_Tbr_low,
                       hedr_Tbr_high,
                       hedr_mode_vac,
                       hedr_pres_low,
                       hedr_pres_high,
                       hedr_rpm_min,
                       hedr_rpm_max,
                       hedr_intermission,
                       hedr_test_cat,
                       hedr_test_item,
                       hedr_test_val_tgt_criterion,
                       hedr_test_unit
                       ]



#########################################################
# UO-specific options, list, header_item: list dictionry thereof (for data input and internalsignaling)
#########################################################

opt_Tj_ctrl_cat_spec:str = "Tj_ctrl_spec"
"""An option for the category of the filter dryer jacket temperature control. Spec: Control by specification."""
opt_Tj_ctrl_cat_arbitrary:str = "Tj_ctrl_arbitrary"
"""An option for the category of the filter dryer jacket temperature control. Arbitrary: Control by arbitrary setting."""
opt_Tj_ctrl_cat_guide:str = "Tj_ctrl_guide"
"""An option for the category of the filter dryer jacket temperature control. Guide: Control by guidance."""
list_opt_Tj_ctrl_cat:list[str] = [opt_Tj_ctrl_cat_spec, opt_Tj_ctrl_cat_arbitrary, opt_Tj_ctrl_cat_guide]
"""A list of options for the category of the filter dryer jacket temperature control."""

opt_mode_vac_arbitrary:str = "arbitrary"
"""An option for the mode of vacuum. Arbitrary: Arbitrary vacuum setting"""
opt_mode_vac_range:str = "range"
"""An option for the mode of vacuum. Range: Vacuum setting within a range"""
opt_mode_vac_full_vacuum:str = "full_vacuum"
"""An option for the mode of vacuum. Full_vacuum: Full vacuum setting"""
list_opt_mode_vac:list[str] = [opt_mode_vac_arbitrary, opt_mode_vac_range, opt_mode_vac_full_vacuum]
"""A list of options for the vacuum control mode."""


opt_test_cat_ipc:str = "ipc"
"""An option for the test category. IPC: In-Process Control"""
opt_test_cat_monit_no_tgt:str = "monit_no_tgt"
"""An option for the test category. Monit_no_tgt: Monitoring without target criterion"""
opt_test_cat_monit_with_tgt:str = "monit_with_tgt"
"""An option for the test category. Monit_with_tgt: Monitoring with target criterion"""
list_opt_test_cat:list[str] = [opt_test_cat_ipc, opt_test_cat_monit_no_tgt, opt_test_cat_monit_with_tgt]
"""A list of options for the test category."""

list_opt_intermission:list[str] = [opt_yes, opt_no]

dict_opt:dict[str, list[str]] = {
    hedr_Tj_ctrl_cat : list_opt_Tj_ctrl_cat,
    hedr_mode_vac : list_opt_mode_vac,
    hedr_test_cat : list_opt_test_cat,
    hedr_intermission : list_opt_intermission,
}




#########################################################
# signal -> local language dictionary and tags for it
#########################################################
lang_dict_uo_titles = defs.dict_jp_part_uo_titles


        ##### Tags (keys) for translation of common parts ####
tag_flow_cmn_rec_time:str = defs.tag_flow_cmn_rec_time
"""The key to the time-recording field for the flowsheet, a common item."""
tag_flow_cmn_rec_sign:str = defs.tag_flow_cmn_rec_sign
"""The key to the ignature field for the flowsheet, a common item."""
tag_flow_cmn_time_unit_second = opt_time_unit_second
"""Tag for a common flowsheet component for an unit of time: second"""
tag_flow_cmn_time_unit_minute = opt_time_unit_minute
"""Tag for a common flowsheet component for an unit of time: minute"""
tag_flow_cmn_time_unit_hour = opt_time_unit_hour
"""Tag for a common flowsheet component for an unit of time: hour"""
lang_dict_cmn:dict[str, str] = defs.dict_jp_part_flow_cmn
"""
Language dictionary for common parts.
    tag_flow_cmn_rec_time : part_flow_cmn_rec_time_jp,
    tag_flow_cmn_rec_sign : part_flow_cmn_rec_sign_jp
    tag_flow_cmn_time_unit_second : part_flow_cmn_time_unit_second,
    tag_flow_cmn_time_unit_minute : part_flow_cmn_time_unit_minute,
    tag_flow_cmn_time_unit_hour : part_flow_cmn_time_unit_hour
"""

tag_part_method_instr_init:str = "instr_init_drying"
"""The key to the instruction to start the drying operation."""
tag_part_content_instr_chron_rec:str = "content_instr_chron_rec"
"""The key to the content of the chronological record for the drying operation."""

tag_part_content_Tj_arbitrary:str = "content_Tj_arbitrary"
"""The key to the arbitrary setting of the filter dryer jacket temperature for the drying operation."""
tag_part_content_Tbr_arbitrary:str = "content_Tbr_arbitrary"
"""The key to the arbitrary setting of the condenser brine temperature for the drying operation."""

tag_part_rec_temp_cond_brine:str = "rec_temp_cond_brine"
"""The key to the record of the condenser brine temperature for the drying operation."""
tag_part_content_press_arbitrary:str = "press_arbitrary"
"""The key to the arbitrary vacuum setting for the drying operation."""
tag_part_rec_press_drying:str = "rec_press"
"""The key to the record field of the drying pressure for the drying operation."""
tag_part_content_rot_arbitrary:str = "content_rot_arbitrary"
"""The key to the arbitrary rotation setting for the drying operation."""
tag_part_rec_rot_drying:str = "rec_rot"
"""The key to the record field of the rotation rate for the drying operation."""
tag_part_content_instr_intermission:str = "content_instr_intermission"
"""The key to the instruction for intermission of the drying operation."""
tag_part_content_instr_sampling_intermission:str = "content_instr_sampling_intermission"
"""The key to the instruction for sampling before and after the intermissionof the drying operation."""
tag_part_content_instr_digging:str = "content_instr_digging"
"""The key to the instruction for digging the cake in the filter dryer during the drying operation."""
tag_part_method_instr_end:str = "instr_end_drying"
"""The key to the instruction to end the drying operation."""
tag_part_content_record_monitoring:str = "content_record_monitoring"
"""The key to the instruction for recording the monitoring of the drying operation."""
tag_part_record_ok_nok:str = "record_ok_nok"
"""The key to the record field for the monitoring result of the drying operation."""
tag_part_content_instr_continue_till_tgt:str = "content_instr_continue_tgt"
"""The key to the instruction for continuing the drying operation until the target value is reached."""


jp_dict_parts:dict[str, str] = {
    tag_part_method_instr_init : "乾燥開始",
    tag_part_content_instr_chron_rec : "*作業詳細は経時的な作業記録書に記録すること",
    tag_part_content_Tj_arbitrary : "外温設定:現場調整",
    tag_part_content_Tbr_arbitrary : "冷却用ブライン:現場調整",
    tag_part_rec_temp_cond_brine : "冷却用ブライン温度:___________℃",
    tag_part_content_press_arbitrary : "真空度:現場調整",
    tag_part_rec_press_drying : "真空度:___________MPa",
    tag_part_content_rot_arbitrary : "回転数:現場調整",
    tag_part_rec_rot_drying : "回転数:___________rpm",
    tag_part_content_instr_intermission : "乾燥作業の途中で保管しても良い。保管する場合は保管前後でサンプリングすること。",
    tag_part_content_instr_sampling_intermission : "X時間後のサンプルを保管前サンプルとしてもよい。",
    tag_part_content_instr_digging : "乾燥終点の評価は攪拌乾燥で翼が最下端まで到達して乾燥継続した後のサンプルから実施し、"
    "それ以前のサンプルはモニタリング用とする。",
    tag_part_method_instr_end : "乾燥終了",
    tag_part_content_record_monitoring : "*最終結果を記載する",
    tag_part_record_ok_nok : "□適 □不適",
    tag_part_content_instr_continue_till_tgt : "目標値達成まで乾燥を継続する。継続後も目標値に到達しない場合、製薬研・製管責と対応を協議すること。"
}

dict_parts:dict[str, str] = jp_dict_parts

"""
def put_line(
    time: str = '',
    method: str = '',
    content: str = '',
    record: str = '',
    operator: str = '',
    witness: str = ''
) -> None
"""

tag_stc_Tj_spec_low:str = "stc_Tj_limit_low"
"""The key to the sentence for the lower limit of the filter dryer jacket temperature. Includes a placeholder "Tj_low"."""
tag_stc_Tj_spec_high:str = "stc_Tj_limit_high"
"""The key to the sentence for the upper limit of the filter dryer jacket temperature. Includes a placeholder "Tj_high"."""
tag_stc_Tj_spec_range:str = "stc_Tj_range"
"""The key to the sentence for the range of the filter dryer jacket temperature. Includes placeholders "Tj_low" and "Tj_high"."""
tag_stc_Tj_guide_single:str = "stc_Tj_guidance_single"
"""The key to the sentence for the single point guidance of the filter dryer jacket temperature. Includes placeholder "Tj_guide"."""
tag_stc_Tj_guide_range:str = "stc_Tj_guidance_range"
"""The key to the sentence for the range guidance of the filter dryer jacket temperature. Includes placeholders "Tj_low" and "Tj_high"."""
tag_stc_Tbr_limit_low:str = "stc_Tbr_limit_low_drying"
"""The key to the sentence for the lower limit of the condenser brine temperature. Includes a placeholder "Tbr_low"."""
tag_stc_Tbr_limit_high:str = "stc_Tbr_limit_high_drying"
"""The key to the sentence for the upper limit of the condenser brine temperature. Includes a placeholder "Tbr_high"."""
tag_stc_Tbr_range:str = "stc_Tbr_range_drying"
"""The key to the sentence for the range of the condenser brine temperature. Includes placeholders "Tbr_low" and "Tbr_high"."""
tag_stc_press_low:str = "stc_press_min_drying"
"""The key to the sentence for the lower limit of the drying pressure. Includes a placeholder "pres_low". In the unit of MPa."""
tag_stc_press_high:str = "stc_press_max_drying"
"""The key to the sentence for the upper limit of the drying pressure. Includes a placeholder "pres_high". In the unit of MPa."""
tag_stc_press_range:str = "stc_press_range_drying"
"""The key to the sentence for the range of the drying pressure. Includes placeholders "pres_low" and "pres_high". In the unit of MPa."""
tag_stc_rot_min:str = "stc_rot_min_drying"
"""The key to the sentence for the lower limit of the rotation rate of the filter dryer. Includes a placeholder "rpm_min"."""
tag_stc_rot_max:str = "stc_rot_max_drying"
"""The key to the sentence for the upper limit of the rotation rate of the filter dryer. Includes a placeholder "rpm_max"."""
tag_stc_rot_range:str = "stc_rot_range_drying"
"""The key to the sentence for the range of the rotation rate of the filter dryer. Includes placeholders "rpm_min" and "rpm_max"."""
tag_stc_content_instr_sample_name_intermission:str = "content_instr_sample_name_intermission_drying"
"""The key to the instruction for naming the sample before and after the intermission of the drying operation. Includes a placeholder "proc_name"."""
tag_stc_content_ipc:str = "test_ipc"
"""The key to the instruction for testing: IPC with an item name and a criterion. Includes placeholders "test_item", "criterion", and "unit"."""
tag_stc_content_monit_with_tgt:str = "test_monit_with_tgt"
"""The key to the instruction for testing: Monitoring with an item name and the target value. Includes placeholders "test_item", "criterion", and "unit"."""
tag_stc_content_monit_no_tgt:str = "test_monit_no_tgt"
"""The key to the instruction for testing: Monitoring with an item name. Includes a placeholder "test_item"."""
tag_stc_record_test_result:str = "record_test_result"
"""The key to the instruction for recording the test result of the drying operation. Includes placeholders "test_item" and "unit"."""



dict_stc_jp:dict[str, str] = {
    tag_stc_Tj_spec_low : "外温設定:{Tj_low}℃以上",
    tag_stc_Tj_spec_high : "外温設定:{Tj_high}℃以下",
    tag_stc_Tj_spec_range : "外温設定:{Tj_low}～{Tj_high}℃",
    tag_stc_Tj_guide_range : "外温設定目安:{Tj_low}～{Tj_high}℃",
    tag_stc_Tj_guide_single : "外温設定目安:{Tj_guide}℃",
    tag_stc_Tbr_limit_low : "冷却用ブライン:{Tbr_low}℃以上",
    tag_stc_Tbr_limit_high : "冷却用ブライン:{Tbr_high}℃以下",
    tag_stc_Tbr_range : "冷却用ブライン:{Tbr_low}～{Tbr_high}℃",
    tag_stc_press_low : "真空度:{pres_low}MPa以上",
    tag_stc_press_high : "真空度:{pres_high}MPa以下",
    tag_stc_press_range : "真空度:{pres_low}～{pres_high}MPa",
    tag_stc_rot_min : "回転数:{rpm_min}rpm以上",
    tag_stc_rot_max : "回転数:{rpm_max}rpm以下",
    tag_stc_rot_range : "回転数:{rpm_min}～{rpm_max}rpm",
    tag_stc_content_instr_sample_name_intermission : "サンプル名「{proc_name}静置/攪拌乾燥X時間後」",
    tag_stc_content_ipc : "IPC: {test_item} {criterion}{unit}",
    tag_stc_content_monit_with_tgt : "モニタリング(目標値): {test_item} {criterion}{unit}",
    tag_stc_content_monit_no_tgt : "モニタリング: {test_item}",
    tag_stc_record_test_result : "{test_item}:___________{unit}"

}

dict_stc:dict[str, str] = dict_stc_jp

#########################################################
# Class (uo.UnitOperation, uo_tag=defs.tag_uo_<UO_NAME>)
#------------------------------------------
# Mandatory methods
# __init__(self,
#           caller: type[trdef.UniversalTrait] =None,
#           flowsheet:fsht.Flowsheet=None,
#           operation_seq: int=None,
#           num_subitems: int = None,
#           edit_comment:str=None)
# get_detail_header(self) -> list[str]

# load_papams_from_df(self, df: pd.DataFrame)
# output_unit_operation(self)
#
#########################################################
class Drying(uo.UnitOperation, uo_tag=defs.tag_uo_drying):
    def __init__(self,
                 caller: type[trdef.GetProcName] =None,
                 flowsheet:fsht.Flowsheet=None,
                 operation_seq: int=None,
                 num_subitems: int = None,
                 edit_comment:str=None):
        super().__init__(caller=caller, flowsheet=flowsheet, operation_seq=operation_seq, num_subitems=num_subitems, edit_comment=edit_comment)
        self.Tj_ctrl_cat: str = None
        self.Tj_low: float = None
        self.Tj_high: float = None
        self.Tbr_low: float = None
        self.Tbr_high: float = None
        self.mode_vac: str = None
        """Mode of vacuum for the drying operation. Refer to list_opt_mode_vac for the options."""
        self.pres_low: float = None
        self.pres_high: float = None
        self.rpm_min: float = None
        self.rpm_max: float = None
        self.intermission: bool = None
        """Intermission of the drying operation is allowed or not. Refer to list_opt_intermission for the options."""
        self.list_ipc: list[TestDescription] = []
        """List of IPC items for the drying operation."""
        self.list_monit_with_tgt: list[TestDescription] = []
        """List of monitoring items with target criterion for the drying operation."""
        self.list_monit_no_tgt: list[TestDescription] = []
        """List of monitoring items without target criterion for the drying operation."""

    
    def load_params_from_df(self, df: pd.DataFrame):
        """
        Loads necessary parameters from a DataFrame object.
        The header items must be in line with the definition the class Charging.
        The header items can be passed from the get_detail_header() of each UnitOperation-drived class.
        This is the overriding mehtod in the class Charging..
        """

        first_row = df.iloc[0]
        if not pd.isna(first_row[hedr_precomment]):
            self.pre_comment = first_row[hedr_precomment]
        if not pd.isna(first_row[hedr_postcomment]):
            self.post_comment = first_row[hedr_postcomment]
        for _, subitem in df.iterrows():
            if not pd.isna(subitem[hedr_Tj_ctrl_cat]):
                self.Tj_ctrl_cat = subitem[hedr_Tj_ctrl_cat]
            if not pd.isna(subitem[hedr_Tj_low]):
                self.Tj_low = subitem[hedr_Tj_low]
            if not pd.isna(subitem[hedr_Tj_high]):
                self.Tj_high = subitem[hedr_Tj_high]
            if not pd.isna(subitem[hedr_Tbr_low]):
                self.Tbr_low = subitem[hedr_Tbr_low]
            if not pd.isna(subitem[hedr_Tbr_high]):
                self.Tbr_high = subitem[hedr_Tbr_high]
            if not pd.isna(subitem[hedr_mode_vac]):
                self.mode_vac = subitem[hedr_mode_vac]
            if not pd.isna(subitem[hedr_rpm_min]):
                self.rpm_min = subitem[hedr_rpm_min]
            if not pd.isna(subitem[hedr_rpm_max]):
                self.rpm_max = subitem[hedr_rpm_max]
            if not pd.isna(subitem[hedr_pres_low]):
                self.pres_low = subitem[hedr_pres_low]
            if not pd.isna(subitem[hedr_pres_high]):
                self.pres_high = subitem[hedr_pres_high]
            if not pd.isna(subitem[hedr_intermission]):
                if subitem[hedr_intermission] == opt_yes:
                    self.intermission = True
                else:
                    self.intermission = False
            if not pd.isna(subitem[hedr_test_cat]) and not pd.isna(subitem[hedr_test_item]):
                test_item:TestDescription = TestDescription(test_cat=subitem[hedr_test_cat],
                                                    test_item=subitem[hedr_test_item],
                                                    test_val_tgt_criterion=subitem.get(hedr_test_val_tgt_criterion, None),
                                                    test_unit_val=subitem.get(hedr_test_unit, None))
                if test_item.test_cat == opt_test_cat_ipc:
                    self.list_ipc.append(test_item)
                elif test_item.test_cat == opt_test_cat_monit_with_tgt:
                    self.list_monit_with_tgt.append(test_item)
                elif test_item.test_cat == opt_test_cat_monit_no_tgt:
                    self.list_monit_no_tgt.append(test_item)


    def get_detail_header(self) -> list[str]:
        """UO-specific items only."""
        return list_uo_specif_hedr

    def get_detail_option_menu(self) -> Optional[dict[str, list[str]]]:
        return dict_opt
    
    def get_json_schema(cls, caller: type[trdef.UniversalTrait]=None)->Objason:
        common_schema:list[Primitive] = cls.json_common()
        Tj_ctrl_cat:Primitive = Primitive(prim_type="string",
                                          key=hedr_Tj_ctrl_cat,
                                          description=f'The category of the filter dryer jacket temperature control. '
                                          f'Options are "{opt_Tj_ctrl_cat_spec}", "{opt_Tj_ctrl_cat_guide}", and "{opt_Tj_ctrl_cat_arbitrary}". '
                                          f'"{opt_Tj_ctrl_cat_spec}": The jacket temperature has to be kept within the range specified by "{hedr_Tj_low}" and/or "{hedr_Tj_high}", strictly GMP-wise. '
                                          f'"{opt_Tj_ctrl_cat_guide}": The temperature is controlled according to a non-binding guidance indicated by "{hedr_Tj_low}" and/or "{hedr_Tj_high}". '
                                          f'"{opt_Tj_ctrl_cat_arbitrary}": The temperature can be arbitrarily controlled by the operator on the shop floor. ',
                                          enum=list_opt_Tj_ctrl_cat
                                          )
        Tj_low:Primitive = Primitive(prim_type="number",
                                     key=hedr_Tj_low,
                                     description=f'The lower limit of the jacket temperature. '
                                     f'If "{hedr_Tj_ctrl_cat}" is "{opt_Tj_ctrl_cat_spec}" or "{opt_Tj_ctrl_cat_guide}", '
                                     f'at least one of this value or "{hedr_Tj_high}" is mandatory. Nullable, otherwise. The unit is in degree Celsius.'
                                     f'If a guideline value is given as a single point, please put it in both "{hedr_Tj_low}" and "{hedr_Tj_high}".',
                                     nullable=True,
                                     required=True)
        Tj_high:Primitive = Primitive(prim_type="number",
                                      key=hedr_Tj_high,
                                      description=f'The upper limit of the jacket temperature. '
                                      f'If "{hedr_Tj_ctrl_cat}" is "{opt_Tj_ctrl_cat_spec}" or "{opt_Tj_ctrl_cat_guide}", '
                                      f'at least one of this value or "{hedr_Tj_low}" is mandatory. Nullable, otherwise. The unit is in degree Celsius.'
                                      f'If a guideline value is given as a single point, please put it in both "{hedr_Tj_low}" and "{hedr_Tj_high}".',
                                      nullable=True,
                                      required=True)
        Tbr_low:Primitive = Primitive(prim_type="number",
                                      key=hedr_Tbr_low,
                                      description='The lower limit of the condenser brine temperature. '
                                      'Nullable if not specified in the data source. The unit is in degree Celsius. ',
                                      nullable=True,
                                      required=True)
        Tbr_high:Primitive = Primitive(prim_type="number",
                                       key=hedr_Tbr_high,
                                       description=f'The upper limit of the condenser brine temperature. '
                                       f'Nullable if not specified in the data source. The unit is in degree Celsius.',
                                       nullable=True,
                                       required=True)
        mode_vac:Primitive = Primitive(prim_type="string",
                                       key=hedr_mode_vac,
                                       description=f'The mode of vacuum for the drying operation. Options are "{opt_mode_vac_arbitrary}", "{opt_mode_vac_range}", and "{opt_mode_vac_full_vacuum}". '
                                       f'"{opt_mode_vac_arbitrary}": The vacuum can be arbitrarily controlled by the operator on the shop floor. '
                                       f'"{opt_mode_vac_range}": The vacuum has to be kept within the range specified by "{hedr_pres_low}" and/or "{hedr_pres_high}".'
                                       f'"{opt_mode_vac_full_vacuum}": The vacuum has to be kept at full vacuum.'
                                       'If no specification is found in the data source, please select "{opt_mode_vac_full_vacuum}" as the default.',
                                       enum=list_opt_mode_vac,
                                       nullable=False,
                                       required=True)
        pres_low:Primitive = Primitive(prim_type="number",
                                       key=hedr_pres_low,
                                       description=f'The lower limit of the drying pressure. '
                                       f'If "{hedr_mode_vac}" is "{opt_mode_vac_range}", '
                                       f'at least one of this value or "{hedr_pres_high}" is mandatory. Nullable, otherwise. The unit is in MPa absolute.',
                                       nullable=True,
                                       required=True)
        pres_high:Primitive = Primitive(prim_type="number",
                                        key=hedr_pres_high,
                                        description=f'The upper limit of the drying pressure. '
                                        f'If "{hedr_mode_vac}" is "{opt_mode_vac_range}", '
                                        f'at least one of this value or "{hedr_pres_low}" is mandatory. Nullable, otherwise. The unit is in MPa absolute.',
                                        nullable=True,
                                        required=True)
        rpm_min:Primitive = Primitive(prim_type="number",
                                      key=hedr_rpm_min,
                                      description=f'The minimum rotation rate of the filter dryer. '
                                      f'Nullable if not specified in the data source. The unit is in RPM.',
                                      nullable=True,
                                      required=True)
        rpm_max:Primitive = Primitive(prim_type="number",
                                      key=hedr_rpm_max,
                                      description=f'The maximum rotation rate of the filter dryer. '
                                      f'Nullable if not specified in the data source. The unit is in RPM.',
                                      nullable=True,
                                      required=True)
        intermission:Primitive = Primitive(prim_type="string",
                                            key=hedr_intermission,
                                            description=f'Whether intermission of the drying operation is allowed or not. Options are "{opt_yes}" and "{opt_no}". '
                                            f'If no specification is found in the data source, please select "{opt_no}" as the default.',
                                            enum=list_opt_intermission,
                                            nullable=False,
                                            required=True)
        test_cat:Primitive = Primitive(prim_type="string",
                                       key=hedr_test_cat,
                                       description=f'The test category for the drying operation. Options are "{opt_test_cat_ipc}", "{opt_test_cat_monit_with_tgt}", and "{opt_test_cat_monit_no_tgt}". '
                                       f'"{opt_test_cat_ipc}": In-Process Control (IPC) with a test item name and a criterion. '
                                       f'"{opt_test_cat_monit_with_tgt}": Monitoring with target criterion with an item name, a target value, and a unit. '
                                       f'"{opt_test_cat_monit_no_tgt}": Monitoring without target criterion with an item name. ',                                       
                                       enum=list_opt_test_cat,
                                       nullable=False,
                                       required=True)
        test_item:Primitive = Primitive(prim_type="string",
                                        key=hedr_test_item,
                                        description='The test item name for the drying operation.',
                                        nullable=False,
                                        required=True)
        test_val_tgt_criterion:Primitive = Primitive(prim_type='number',
                                                    key=hedr_test_val_tgt_criterion,
                                                    description='The target value or the criterion for the test item for the drying operation. '
                                                    f'if "{hedr_test_cat}" is "{opt_test_cat_ipc}" or "{opt_test_cat_monit_with_tgt}", this value is mandatory. Nullable, otherwise.',
                                                    nullable=True,
                                                    required=True)
        test_unit_val:Primitive = Primitive(prim_type='string',
                                            key=hedr_test_unit,
                                            description='The unit for the value of the test target, criterion, and the result for the drying operation. Nullable where appropriate.',
                                            nullable=True,
                                            required=True)
        obj_test:Objason = Objason(key=key_json_obj_test,
                                   props=[test_cat, test_item, test_val_tgt_criterion, test_unit_val],
                                   description='The JSON object for the test description for the drying operation.')
        arr_test:Array = Array(key=key_json_arr_test,
                               items=obj_test,
                               description='The JSON array for the list of test description for the drying operation.'
                               'Normally, multiple test items of various categories are possible for a drying operation.')
        obj_drying:Objason = Objason(key=cls.uo_tag,
                                    props=common_schema+[Tj_ctrl_cat,
                                                          Tj_low, Tj_high,
                                                          Tbr_low, Tbr_high,
                                                          mode_vac, pres_low, pres_high,
                                                          rpm_min, rpm_max,
                                                          intermission,
                                                          arr_test],
                                    description='The JSON object for the drying operation.',
                                    )
        return obj_drying


        
        
        


    def load_from_json_dict(self, json_dict: dict[str, any]):
        super().load_from_json_dict(json_dict)
        pass

    def output_unit_operation(self):
        self.flowsheet.header_organizer(op_nr=self.operation_seq, title=lang_dict_uo_titles[self.uo_tag])
        if not (self.pre_comment == None or self.pre_comment == ''):
            self.flowsheet.put_body_comments(self.pre_comment)
            self.flowsheet.linefeed()        

        self.flowsheet.put_line(content=dict_parts[tag_part_content_instr_chron_rec])
        self.__put_tempr_ctrl()
        self.__put_vac_ctrl()
        self.__put_rot_ctrl()
        self.flowsheet.linefeed()
        self.__terminate_drying()
        self.flowsheet.put_line(content=dict_parts[tag_part_content_instr_intermission])
        self.flowsheet.put_line(content=dict_parts[tag_part_content_instr_sampling_intermission])
        self.flowsheet.put_line(content=dict_stc[tag_stc_content_instr_sample_name_intermission].format(proc_name=self.caller.get_proc_name()))
        self.flowsheet.put_line(content=dict_parts[tag_part_content_instr_digging])
        self.flowsheet.linefeed()

        if not (self.post_comment == None or self.post_comment == ''):
            self.flowsheet.put_body_comments(self.post_comment)
            self.flowsheet.linefeed()


    def __put_tempr_ctrl(self):
        stc_Tj:str = None
        if self.Tj_ctrl_cat == opt_Tj_ctrl_cat_spec:
            if self.Tj_low is not None and self.Tj_high is not None:
                stc_Tj = dict_stc[tag_stc_Tj_spec_range].format(Tj_low=self.Tj_low, Tj_high=self.Tj_high)
            elif self.Tj_low is not None:
                stc_Tj = dict_stc[tag_stc_Tj_spec_low].format(Tj_low=self.Tj_low)
            elif self.Tj_high is not None:
                stc_Tj = dict_stc[tag_stc_Tj_spec_high].format(Tj_high=self.Tj_high)
            else:
                warnings.warn(f'{self.__class__.__name__}, Op.{self.operation_seq}: '
                              f'Neither of the lower limit nor the upper limit of the filter dryer jacket temperature is specified '
                              f'although the Tj control category is "{self.Tj_ctrl_cat}"')
                stc_Tj = dict_parts[tag_part_content_Tj_arbitrary]
        elif self.Tj_ctrl_cat == opt_Tj_ctrl_cat_guide:
            if self.Tj_low is not None and self.Tj_high is not None:
                if self.Tj_low == self.Tj_high:
                    stc_Tj = dict_stc[tag_stc_Tj_guide_single].format(Tj_guide=self.Tj_low)
                else:
                    stc_Tj = dict_stc[tag_stc_Tj_guide_range].format(Tj_low=self.Tj_low, Tj_high=self.Tj_high)
            elif self.Tj_low is not None:
                stc_Tj = dict_stc[tag_stc_Tj_guide_single].format(Tj_guide=self.Tj_low)
            elif self.Tj_high is not None:
                stc_Tj = dict_stc[tag_stc_Tj_guide_single].format(Tj_guide=self.Tj_high)
            else:
                warnings.warn(f'{self.__class__.__name__}, Op.{self.operation_seq}: '
                              f'Neither of the lower limit nor the upper limit of the filter dryer jacket temperature is specified '
                              f'although the Tj control category is "{self.Tj_ctrl_cat}"')
                stc_Tj = dict_parts[tag_part_content_Tj_arbitrary]
        else:
            stc_Tj = dict_parts[tag_part_content_Tj_arbitrary]
        self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                method=dict_parts[tag_part_method_instr_init],
                                content=stc_Tj,
                                operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
        stc_Tbr:str = None
        if self.Tbr_low is not None and self.Tbr_high is not None:
            stc_Tbr = dict_stc[tag_stc_Tbr_range].format(Tbr_low=self.Tbr_low, Tbr_high=self.Tbr_high)
        elif self.Tbr_low is not None:
            stc_Tbr = dict_stc[tag_stc_Tbr_limit_low].format(Tbr_low=self.Tbr_low)
        elif self.Tbr_high is not None:
            stc_Tbr = dict_stc[tag_stc_Tbr_limit_high].format(Tbr_high=self.Tbr_high)
        else:
            stc_Tbr = dict_parts[tag_part_content_Tbr_arbitrary]
        self.flowsheet.put_line(content=stc_Tbr,
                                record=dict_parts[tag_part_rec_temp_cond_brine])
        
        
    def __put_vac_ctrl(self):
        stc_press:str = None
        if self.pres_low is not None and self.pres_high is not None:
            stc_press = dict_stc[tag_stc_press_range].format(pres_low=self.pres_low, pres_high=self.pres_high)
        elif self.pres_low is not None:
            stc_press = dict_stc[tag_stc_press_low].format(pres_low=self.pres_low)
        elif self.pres_high is not None:
            stc_press = dict_stc[tag_stc_press_high].format(pres_high=self.pres_high)
        else:
            stc_press = dict_parts[tag_part_content_press_arbitrary]
        self.flowsheet.put_line(content=stc_press,
                                record=dict_parts[tag_part_rec_press_drying])    

    def __put_rot_ctrl(self):
        stc_rot:str = None
        if self.rpm_min is not None and self.rpm_max is not None:
            stc_rot = dict_stc[tag_stc_rot_range].format(rpm_min=self.rpm_min, rpm_max=self.rpm_max)
        elif self.rpm_min is not None:
            stc_rot = dict_stc[tag_stc_rot_min].format(rpm_min=self.rpm_min)
        elif self.rpm_max is not None:
            stc_rot = dict_stc[tag_stc_rot_max].format(rpm_max=self.rpm_max)
        else:
            stc_rot = dict_parts[tag_part_content_rot_arbitrary]
        self.flowsheet.put_line(content=stc_rot,
                                record=dict_parts[tag_part_rec_rot_drying])

    def __terminate_drying(self):
        is_first: bool = True

        if self.list_ipc is not None and len(self.list_ipc) > 0:
            is_ipc_set = True
        else:
            is_ipc_set = False

        if self.list_monit_with_tgt is not None and len(self.list_monit_with_tgt) > 0:
            is_monit_with_tgt_set = True
        else:
            is_monit_with_tgt_set = False

        if self.list_monit_no_tgt is not None and len(self.list_monit_no_tgt) > 0:
            is_monit_no_tgt_set = True
        else:
            is_monit_no_tgt_set = False


        if is_ipc_set:
            for test in self.list_ipc:
                content:str = dict_stc[tag_stc_content_ipc].format(test_item=test.test_item,
                                                                   criterion=test.test_val_tgt_criterion,
                                                                   unit=test.test_unit_val if test.test_unit_val is not None else '')
                record:str = dict_stc[tag_stc_record_test_result].format(test_item=test.test_item,
                                                                         unit=test.test_unit_val if test.test_unit_val is not None else '')
                if is_first:
                    self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                            method=dict_parts[tag_part_method_instr_end],
                                            content=dict_parts[tag_part_content_record_monitoring],
                                            record=dict_parts[tag_part_record_ok_nok],
                                            operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                            witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
                    self.flowsheet.put_line(content=content,
                                            record=record,)
                    is_first = False
                else:
                    self.flowsheet.put_line(content=content,
                                            record=record)
        if is_monit_with_tgt_set:
            for test in self.list_monit_with_tgt:
                content:str = dict_stc[tag_stc_content_monit_with_tgt].format(test_item=test.test_item,
                                                                             criterion=test.test_val_tgt_criterion,
                                                                             unit=test.test_unit_val if test.test_unit_val is not None else '')
                record:str = dict_stc[tag_stc_record_test_result].format(test_item=test.test_item,
                                                                         unit=test.test_unit_val if test.test_unit_val is not None else '')
                if is_first:
                    self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                            method=dict_parts[tag_part_method_instr_end],
                                            content=dict_parts[tag_part_content_record_monitoring],
                                            record=dict_parts[tag_part_record_ok_nok],
                                            operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                            witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
                    self.flowsheet.put_line(content=content,
                                            record=record)
                    is_first = False
                else:
                    self.flowsheet.put_line(content=content,
                                            record=record)
        if is_monit_no_tgt_set:
            for test in self.list_monit_no_tgt:
                content:str = dict_stc[tag_stc_content_monit_no_tgt].format(test_item=test.test_item)
                record:str = dict_stc[tag_stc_record_test_result].format(test_item=test.test_item,
                                                                         unit=test.test_unit_val if test.test_unit_val is not None else '')
                if is_first:
                    self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                            method=dict_parts[tag_part_method_instr_end],
                                            content=dict_parts[tag_part_content_record_monitoring],
                                            record=dict_parts[tag_part_record_ok_nok],
                                            operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                            witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
                    self.flowsheet.put_line(content=content,
                                            record=record)
                    is_first = False
                else:
                    self.flowsheet.put_line(content=content,
                                            record=record)
        if not (is_ipc_set or is_monit_with_tgt_set or is_monit_no_tgt_set):
            self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                    method=dict_parts[tag_part_method_instr_end],
                                    record=dict_parts[tag_part_record_ok_nok],
                                    operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
        if is_monit_with_tgt_set:
            self.flowsheet.put_line(content=dict_parts[tag_part_content_instr_continue_till_tgt])


    
    @classmethod
    def generate_test_df(cls,
                         precomment:str=None,
                         postcomment:str=None,
                         Tj_ctrl_cat:Literal["Tj_ctrl_spec", "Tj_ctrl_arbitrary", "Tj_ctrl_guide"]=None,
                         Tj_low:float=None,
                         Tj_high:float=None,
                         Tbr_high:float=None,
                         Tbr_low:float=None,
                         mode_vac:Literal["arbitrary", "range", "full_vacuum"]=None,
                         pres_low:float=None,
                         pres_high:float=None,
                         rpm_min:float=None,
                         rpm_max:float=None,
                         intermission:Literal["Yes", "No"]="Yes",
                         test_cat:Literal["ipc", "monit_no_tgt", "monit_with_tgt", None]=None,
                         test_item:str=None,
                         test_val_tgt_criterion:float=None,
                         test_unit_val:str=None)->pd.DataFrame:
        hedr:list[str] = defs.list_hedr_cmn_io_dtil + list_uo_specif_hedr
        content: list[any] = [None]*len(hedr)
        s:pd.Series = pd.Series(data=content, index=hedr)
        df = s.to_frame().T
        df.at[df.index[0], hedr_precomment]=precomment
        df.at[df.index[0], hedr_postcomment]=postcomment
        df.at[df.index[0], hedr_Tj_ctrl_cat]=Tj_ctrl_cat
        df.at[df.index[0], hedr_Tj_low]=Tj_low
        df.at[df.index[0], hedr_Tj_high]=Tj_high
        df.at[df.index[0], hedr_Tbr_low]=Tbr_low
        df.at[df.index[0], hedr_Tbr_high]=Tbr_high
        df.at[df.index[0], hedr_mode_vac]=mode_vac
        df.at[df.index[0], hedr_pres_low]=pres_low
        df.at[df.index[0], hedr_pres_high]=pres_high
        df.at[df.index[0], hedr_rpm_min]=rpm_min
        df.at[df.index[0], hedr_rpm_max]=rpm_max
        df.at[df.index[0], hedr_intermission]=intermission
        df.at[df.index[0], hedr_test_cat]=test_cat
        df.at[df.index[0], hedr_test_item]=test_item
        df.at[df.index[0], hedr_test_val_tgt_criterion]=test_val_tgt_criterion
        df.at[df.index[0], hedr_test_unit]=test_unit_val

        return df
    
    @classmethod
    def add_to_test_df(cls,
                       df: pd.DataFrame=None,
                       test_cat:Literal["ipc", "monit_no_tgt", "monit_with_tgt", None]=None,
                       test_item:str=None,
                       test_val_tgt_criterion:float=None,
                       test_unit_val:str=None)->pd.DataFrame:
        width:int = len(df.columns)
        new_row:list[any] = [None]*width
        row:int = len(df)
        df.loc[row]=new_row
        df.at[row, hedr_test_cat]=test_cat
        df.at[row, hedr_test_item]=test_item
        df.at[row, hedr_test_val_tgt_criterion]=test_val_tgt_criterion
        df.at[row, hedr_test_unit]=test_unit_val

        return df

class TestDescription:
    def __init__(self, test_cat:str=None, test_item:str=None, test_val_tgt_criterion:float=None, test_unit_val:str=None):
        self.test_cat:str = test_cat
        self.test_item:str = test_item
        self.test_val_tgt_criterion:float = test_val_tgt_criterion
        self.test_unit_val:str = test_unit_val