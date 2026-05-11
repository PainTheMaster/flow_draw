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

hedr_origin = defs.hedr_uo_phasedisch_origin
"""Header item for uo_phase_discharge: origin of the discarded lower phase, e.g., reaction vessel, etc."""
hedr_via = defs.hedr_uo_phasedisch_via
"""Header item for uo_phase_discharge: way point of the discarded lower phase, e.g., multiplexker, etc"""
hedr_destin = defs.hedr_uo_phasedisch_destin
"""Header item for uo_phase_discharge: destination of the discarded lower phase, e.g., wate liqour tank, etc"""
list_hedr = defs.list_hedr_uo_phasedich
"""list of  hader fields for the unit operation phase discharge"""

#########################################################
# UO-specific options, list, header_item: list dictionry thereof (for data input and internalsignaling)
#########################################################

#options for this unit operation




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

                  #>>>>>>>>>>>>> Flowsheet components <<<<<<<<<<<<<<<<

tag_part_flow_method_connection = defs.tag_part_flow_uo_phasedisch_method_connection
"""Tag for a flowsheet component for a unit operation phase discharging: Discharging line connection"""
tag_part_flow_chk_connected = defs.tag_part_flow_uo_phasedisch_chk_connected
"""Tag for a flowsheet component for a unit operation phase discharging: check box for phase discharging line connected"""
tag_part_flow_method_disch = defs.tag_part_flow_uo_phasedisch_method_disch
"""Tag for a flowsheet component for a unit operation phase discharging: Instruction (method colum) for discharging."""
tag_part_flow_content_disch = defs.tag_part_flow_uo_phasedisch_content_disch
"""Tag for a flowsheet component for a unit operation phase discharging: Description of action (content column) for discharging"""
tag_part_flow_chk_discharged = defs.tag_part_flow_uo_phasedisch_chk_discharged
"""Tag for a flowsheet component for a unit operation phase discharging: check box for the completion of the phase discharging"""
dict_jp_part_flow = defs.dict_jp_part_flow_uo_phasedisch
"""Language dictionary for flowsheet parts for the unit operation phase discharging"""

                    #>>>>>>>>>>>>> Sentences <<<<<<<<<<<<<<<<<<<<<<<<<

tag_stc_origin = defs.tag_stc_uo_phasedisch_origin
"""A tag for an instruction sentence for a unit operation phase discharging: sentence to designate the origon vessel of the discharged phase, includes placeholder {origin}"""
tag_stc_via = defs.tag_stc_uo_phasedisch_via
"""A tag for an instruction sentence for a unit operation phase discharging: sentence to designate the way point, e.g., multiplexer, includes placeholder {via}"""
tag_stc_destin_single = defs.tag_stc_uo_phasedisch_destin_single
"""A tag for an instruction sentence for a unit operation phase discharging: sentence to designate the destination, includes placeholder {destination}"""
tag_stc_destin_multi = defs.tag_stc_uo_phasedisch_destin_multi
"""A tag for an instruction sentence for a unit operation phase discharging: sentence to designate multiple destinations, includes placeholder {destination}--singular!"""
dict_jp_stcs = defs.dict_jp_stcs_uo_phasedisch
"""Japanese language dictionary for instruction sentences for the unit operation phase discharging"""

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

class PhaseDisch(uo.UnitOperation, uo_tag=defs.tag_uo_phase_disch):
    def __init__(self,
                caller: type[trdef.UniversalTrait] =None,
                flowsheet:fsht.Flowsheet=None,
                operation_seq: int=None,
                num_subitems: int = None,
                edit_comment:str=None):
        super().__init__(caller = caller, flowsheet=flowsheet, operation_seq=operation_seq, num_subitems=num_subitems, edit_comment=edit_comment)
        self.origin:str = None
        self.via:str = None
        self.destin:list[str] = []


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
        if not pd.isna(first_row[hedr_origin]):
            self.origin = first_row[hedr_origin]
        if not pd.isna(first_row[hedr_via]):
            self.via = first_row[hedr_via]
        for _, subitem in df.iterrows():
            if not pd.isna(subitem[hedr_destin]):
                self.destin.append(subitem[hedr_destin])
            



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