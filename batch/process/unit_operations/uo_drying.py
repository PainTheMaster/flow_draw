#########################################################
# imports
#########################################################
import pandas as pd
import flow_draw.definitions as defs
import flow_draw.data_io.flowsheet as fsht
from typing import Optional
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

hedr_Tj_low:str = "Tj_low_drying"
"""Header item for uo_drying. The lower limit of the filter dryer jacket temperature. The unit is in degree Celsius. Nullable where appropriate."""
hedr_Tj_high:str = "Tj_high_drying"
"""Header item for uo_drying. The upper limit of the filter dryer jacket temperature. The unit is in degree Celsius. Nullable where appropriate."""
hedr_Tbr_low:str = "Tbr_low_drying"
"""Header item for uo_drying. The lower limit of the condenser brine temeprature. The unit is in degree Celsius. Nullable where appropriate."""
hedr_Tbr_high:str = "Tbr_high_drying"
"""Header item for uo_drying. The upper limit of the condenser brine temeprature. The unit is in degree Celsius. Nullable where appropriate."""
hedr_mode_vac:str = "mode_vac_drying"
"""Header item for uo_drying. The mode vacuum for the filter dryer. Options are "arbitrary", "range", and "full_vacuum"."""
hedr_pres_low:str = "pres_low_drying"
"""Header item for uo_drying. The lower limit of the filter dryer pressure in MPaG unit."""
hedr_pres_high:str = "pres_high_drying"
"""Header item for uo_drying. The upper limit of the filter dryer pressure in MPaG unit."""

hedr_test_cat:str = "test_cat_drying"
"""Header item for uo_drying. The test category for drying. Options are "IPC", "monit_no_tgt", "monit_with_tgt"."""
hedr_test_item:str = "test_item_drying"
"""Header item for uo_drying. The test item for drying."""
hedr_test_val_tgt_criterion:str = "test_tgt_criterion_drying"
"""Header item for uo_drying. The target criterion for the test item for drying. Nullable where appropriate."""
hedr_test_unit_val:str = "test_unit_val_drying"
"""Header item for uo_drying. The unit for the value of the test target, criterion, and the result."""



#########################################################
# UO-specific options, list, header_item: list dictionry thereof (for data input and internalsignaling)
#########################################################

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

dict_opt:dict[str, list[str]] = {
    hedr_mode_vac : list_opt_mode_vac,
    hedr_test_cat : list_opt_test_cat
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
tag_part_content_instr_chron_rec:str = "content_instr_chron_rec_drying"
"""The key to the content of the chronological record for the drying operation."""
tag_part_rec_temp_cond_brine:str = "rec_temp_cond_brine_drying"
"""The key to the record of the condenser brine temperature for the drying operation."""




jp_dict_parts:dict[str, str] = {
    tag_part_method_instr_init : "乾燥開始",
    tag_part_content_instr_chron_rec : "*作業詳細は経時的な作業記録書に記録すること",
    tag_part_rec_temp_cond_brine : "冷却用ブライン温度:___________℃"


}

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

tag_stc_Tj_limit_low:str = "stc_Tj_limit_low_drying"
"""The key to the sentence for the lower limit of the filter dryer jacket temperature. Includes a placeholder "Tj_low"."""
tag_stc_Tj_limit_high:str = "stc_Tj_limit_high_drying"
"""The key to the sentence for the upper limit of the filter dryer jacket temperature. Includes a placeholder "Tj_high"."""
tag_stc_Tj_range:str = "stc_Tj_range_drying"
"""The key to the sentence for the range of the filter dryer jacket temperature. Includes placeholders "Tj_low" and "Tj_high"."""


jp_dict_stc:dict[str, str] = {
    tag_stc_Tj_limit_low : "外温設定:{Tj_low}℃以上",
    tag_stc_Tj_limit_high : "外温設定:{Tj_high}℃以下",
    tag_stc_Tj_range : "外温設定:{Tj_low}～{Tj_high}℃"
}



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
                 caller: type[trdef.UniversalTrait] =None,
                 flowsheet:fsht.Flowsheet=None,
                 operation_seq: int=None,
                 num_subitems: int = None,
                 edit_comment:str=None):
        super().__init__(caller=caller, flowsheet=flowsheet, operation_seq=operation_seq, num_subitems=num_subitems, edit_comment=edit_comment)
    
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
            #<uo-specific process>



    def get_detail_header(self) -> list[str]:
        """UO-specific items only."""
        pass

    def get_detail_option_menu(self) -> Optional[dict[str, list[str]]]:
        pass
    
    def get_json_schema(caller: trdef.UniversalTrait=None)->Objason:
        common_schema:list[Primitive] = ThisClass.json_common()


    def load_from_json_dict(self, json_dict: dict[str, any]):
        super().load_from_json_dict(json_dict)
        pass

    def output_unit_operation(self):
        self.flowsheet.header_organizer(op_nr=self.operation_seq, title=lang_dict_uo_titles[self.uo_tag])
        if not (self.pre_comment == None or self.pre_comment == ''):
            self.flowsheet.put_body_comments(self.pre_comment)
            self.flowsheet.linefeed()        

        #<Operation-specific processes here>

        if not (self.post_comment == None or self.post_comment == ''):
            self.flowsheet.put_body_comments(self.post_comment)
            self.flowsheet.linefeed()
    
    @classmethod
    def generate_test_df(cls,
                       PARAMETER=DEFALUT_VALUE)->pd.DataFrame:
        hedr:list[str] = defs.list_hedr_cmn_io_dtil + list_hedr
        content: list[any] = [None]*len(hedr)
        s:pd.Series = pd.Series(data=content, index=hedr)
        df = s.to_frame().T
        df.at[df.index[0], HEDR_ITEM]=PARAMETER
        ...

        return df
    
    @classmethod
    def add_to_test_df(cls,
                       df: pd.DataFrame=None,
                       PARAMETER=DEFALUT_VALUE)->None:
        width:int = len(df.columns)
        new_row:list[any] = [None]*width
        row:int = len(df)
        df.loc[row]=new_row
        df.at[row, HEADER_ITEM]=PARAMETER
        ...
