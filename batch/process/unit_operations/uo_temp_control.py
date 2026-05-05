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



#########################################################
# Common items: headers etc
#########################################################
header_precomment = defs.hedr_cmn_io_dtil_precmnt #Don't include this in the specific header list!!!
header_postcomment = defs.hedr_cmn_io_dtil_postcmnt #Don't include this in the specific header list!!!


#########################################################
# UO-specific hader items and list thereof
#########################################################

#hedr_<something> = defs.hedr_<unit operation>_<specification item>
#list_hedr = defs.list_hedr_<list of header items for the uo>
#dict_dtil_drpdwn = defs.dict_opt_<unit operation>

#########################################################
# UO-specific options, list, header_item: list dictionry thereof (for data input and internalsignaling)
#########################################################

            ##### header items for detail worksheet######

hedr_mode = defs.hedr_uo_tempr_ctrl_mode
"""Detail heder item: temperature control mode (e.g. Ti, Ti/Tj, amping)"""
hedr_Ti_sp = defs.hedr_uo_tempr_ctrl_Ti_sp
"""Detail heder item: Ti set point for Ti, Ti/Tj mode"""
hedr_Ti_low = defs.hedr_uo_tempr_ctrl_Ti_low
"""Detail heder item: Ti lower limit designaetd by the process owner."""
hedr_Ti_high = defs.hedr_uo_tempr_ctrl_Ti_high
"""Detail heder item: Ti upper limit designated by the process owner."""
hedr_Ti_tgt_high = defs.hedr_uo_tempr_ctrl_Ti_tgt_low
"""Detail heder item: Ti TARGET lower limit designated by the process owner."""
hedr_Ti_tgt_low = defs.hedr_uo_tempr_ctrl_Ti_tgt_high
"""Detail heder item: Ti TARGET higher limit designated by the process owner."""
hedr_Tj_sp = defs.hedr_uo_tempr_ctrl_Tj_sp
"""Detail heder item: Tj set point for Tj mode"""
hedr_Tj_low = defs.hedr_uo_tempr_ctrl_Tj_low
"""Detail heder item: Tj min for Tj, Ti/Tj mode."""
hedr_Tj_high = defs.hedr_uo_tempr_ctrl_Tj_high
"""Detail heder item: Tj max for Tj, Ti/Tj mode"""
hedr_Ti_sp_end = defs.hedr_uo_tempr_ctrl_prog_Ti_sp_end
"""Detail heder item: Ti end target for ramp mode"""
hedr_prog_time_val = defs.hedr_uo_tempr_ctrl_prog_time_val
"""Detail heder item: Ramp up/down time value"""
hedr_prog_time_unit = defs.hedr_uo_tempr_ctrl_prog_time_unit
"""Detail heder item: Ramp up/down time unit"""
hedr_temp_check = defs.hedr_uo_tempr_ctrl_check
"""Detail heder item: need for heating/cooling end point check."""
list_hedr = defs.list_hedr_uo_tempr_ctrl
"""List of header items for unit operation temperature controle"""



        ##### Option items for the detail input table #######

#For hedr_uo_tempr_ctrl_mode
opt_mode_TiTj = defs.opt_uo_tempr_ctrl_mode_TiTj
"""Option for detail table: temperature control with single point Ti and Tj range"""
opt_mode_Tj = defs.opt_uo_tempr_ctrl_mode_Tj
"""Option for detail table: temperature control on jacket temperature (single point)"""
opt_mode_prog = defs.opt_uo_tempr_ctrl_mode_prog
"""Option for detail table: temperature ramping, cooling or heating with time constraint"""
opt_mode_Ti = defs.opt_uo_tempr_ctrl_mode_Ti
"""Option for detail table: temperature control on liquid temperature (single point)"""
# list_opt_mode = defs.list_opt_uo_tempr_ctrl_mode
# """List of a series of temperature control options"""


opt_check_endpoint_yes = defs.tag_yes
"""Option for detail table: Need for temperature control endpoint check-box--yes"""
pot_check_endpoint_no = defs.tag_no
"""Option for detail table: Need for temperature control endpoint check-box--no"""
# list_opt_check_endpoint=defs.list_opt_uo_tempr_ctrl_check_endpoint
# """List options for detail table: Need for temperature control endpoint check-box--yes/no"""


dict_opt = defs.dict_opt_uo_tempr_ctrl
"""Dictionary for detail input form for the unit operation uo_tempr_ctrl"""


#########################################################
# signal -> local language dictionary and tags for it
#########################################################
lang_dict_uo_titles = defs.dict_jp_part_uo_titles


#Tags (keys) for translation of common parts 
tag_flow_cmn_rec_time = defs.tag_flow_cmn_rec_time
"""The key to the time-recording field for the flowsheet, a common item."""
tag_flow_cmn_rec_sign = defs.tag_flow_cmn_rec_sign
"""The key to the ignature field for the flowsheet, a common item."""
lang_dict_cmn = defs.dict_jp_part_flow_cmn
"""
Language dictionary for common parts.
    tag_flow_cmn_rec_time : part_flow_cmn_rec_time_jp,
    tag_flow_cmn_rec_sign : part_flow_cmn_rec_sign_jp
"""

#lang_dict_<this unit operation> = defs.dict_jp_part_<this unit operation>

tag_part_flow_check_config:str = defs.tag_part_flow_tempr_ctrl_check_config
"""Tag for a flowsheet part: check-box for temperature configuration."""
tag_part_flow_check_endpoint:str = defs.tag_part_flow_tempr_ctrl_check_endpoint
"""Tag for a flowsheet part: check-box for temperature end point"""
dict_parts_flow = defs.dict_jp_part_flow_tempr_ctrl
"""Japanese language dictionary for flowsheet parts for unit operation temperature control."""

tag_stc_Tj_sp = defs.tag_stc_tempr_ctrl_Tj_sp
"""Tag for an instruction sentence for temperature control. Tj set point. Includes placeholder{Tj}"""
tag_stc_Ti_Tj_config = defs.tag_stc_tempr_ctrl_Ti_Tj_config
"""Tag for an instruction sentence for temperature control. Ti/Tj configuration. Includes placeholder{Ti}, {Tj_low}, and {Tj_high}"""
tag_stc_Ti_range = defs.tag_stc_tempr_ctrl_Ti_range
"""Tag for an instruction sentence for temperature control. Ti range Includes placeholder {Ti_low} and {Ti_high}"""
tag_stc_Ti_tgt_range = defs.tag_stc_tempr_ctrl_Ti_tgt_range
"""Tag for an instruction sentence for temperature control. Ti target range. Includes placeholder {Ti_low} and {Ti_high}."""
tag_stc_Ti_tgt_single = defs.tag_stc_tempr_ctrl_Ti_tgt_single
"""Tag for an instruction sentence for temperature control. Ti target single point.  Includes placeholder {Ti}"""
dict_stcs = defs.dict_jp_stcs_tempr_ctrl
"""JP language dictionary for """


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

class TempControl(uo.UnitOperation, uo_tag=defs.tag_uo_tempr_ctrl):
    def __init__(self,
                 caller:type[trdef.UniversalTrait] = None,
                 flowsheet:fsht.Flowsheet=None,
                 operation_seq:int = None,
                 num_subitems:int = None,
                 edit_comment:str = None):
        super().__init__(caller=caller, flowsheet=flowsheet, operation_seq=operation_seq, num_subitems=num_subitems, edit_comment=edit_comment)
        self.ctrl_mode:str = None
        self.Ti_sp:float = None
        self.Ti_low:float = None
        self.Ti_high:float = None
        self.Ti_tgt_low:float = None
        self.Ti_tgt_high:float = None
        self.Tj_sp:float = None
        self.Tj_low:float = None
        self.Tj_high:float = None
        self.Ti_prog_endpoint:float = None
        self.time_val_prog:float = None
        self.time_unit_prog:str = None
        self.end_point_check:bool = None


    def load_params_from_df(self, df: pd.DataFrame):
        """
        Loads necessary parameters from a DataFrame object.
        The header items must be in line with the definition the class Charging.
        The header items can be passed from the get_detail_header() of each UnitOperation-drived class.
        This is the overriding mehtod in the class Charging..
        """

        first_row = df.iloc[0]
        if not pd.isna(first_row[header_precomment]):
            self.pre_comment = first_row[header_precomment]
        if not pd.isna(first_row[header_postcomment]):
            self.post_comment = first_row[header_postcomment]
        for _, subitem in df.iterrows():
            #<uo-specific process>



    def get_detail_header(self) -> list[str]:
        pass

    def get_detail_option_menu(self) -> Optional[dict[str, list[str]]]:
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