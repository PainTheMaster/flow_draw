
#########################################################
# imports
#########################################################
import pandas as pd
import flow_draw.definitions as defs
import flow_draw.data_io.flowsheet as fsht
import warnings
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

hedr_time_min = defs.hedr_uo_settling_time_min
"""header for the unit operation settling: Minimum settling time"""
hedr_time_max = defs.hedr_uo_settling_time_max
"""header for the unit operation settling: Maximum settling time"""
hedr_time_unit = defs.hedr_uo_settling_time_unit
"""header for the unit operation settling: Time unit"""
hedr_Ti_min = defs.hedr_uo_settling_Ti_min
"""header for the unit operation settling: Ti min"""
hedr_Ti_max = defs.hedr_uo_settling_Ti_max
"""header for the unit operation settling: Ti max"""
list_hedr = defs.list_hedr_uo_settling
"""list of header items for the unit operation settling"""


#########################################################
# UO-specific options, list, header_item: list dictionry thereof (for data input and internalsignaling)
#########################################################

dict_opt = defs.dict_opt_uo_settling
"""dict of options for heaader items"""


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

                #----------flowsheet parts------------------#

tag_part_init_settling = defs.tag_part_uo_settling_init_settling
"""Tag for a flowsheet component for the unit operation settling: """
tag_part_rec_chk_agitator_stop = defs.tag_part_uo_settling_rec_chk_agitator_stop
"""Tag for a flowsheet component for the unit operation settling: cutting off agitation for settling"""
tag_part_rec_Tj_ini = defs.tag_part_uo_settling_rec_Tj_ini
"""Tag for a flowsheet component for the unit operation settling: record field for the initial Tj"""
tag_part_rec_Ti_ini = defs.tag_part_uo_settling_rec_Ti_ini
"""Tag for a flowsheet component for the unit operation settling: recorod field for the initial Ti"""
tag_part_end_settling = defs.tag_part_uo_settling_end_settling
"""Tag for a flowsheet component for the unit operation settling: end of settling"""
tag_part_Tj_end = defs.tag_part_uo_settling_Tj_end
"""Tag for a flowsheet component for the unit operation settling: Recording field for Tj at the end of settling"""
tag_part_Ti_end = defs.tag_part_uo_settling_Ti_end
"""Tag for a flowsheet component for the unit operation settling:Recording field for Ti at the end of settling """
dict_part_flow = defs.dict_jp_part_flow_uo_settling
"""language dictionary for flowsheet components for the unit opeataion settling"""



                #----------flowsheet sentences----------------#

tag_stc_time_min = defs.tag_stc_uo_settling_time_min
"""Tag for a flowsheet sentence for the unit operation settling: minimum settling time. contains placeholders {time_min} and {time_unit}"""
tag_stc_time_max = defs.tag_stc_uo_settling_time_max
"""Tag for a flowsheet sentence for the unit operation settling: maximum settling time. contains placeholders {time_max} and {time_unit}"""
tag_stc_time_range = defs.tag_stc_uo_settling_time_range
"""Tag for a flowsheet sentence for the unit operation settling: settling time range. contains placeholders {time_min}, {time_max}, and {time_unit}"""
tag_stc_time_single_point = defs.tag_stc_uo_settling_time_single_point
"""Tag for a flowsheet sentence for the unit operation settling: settling time single point. contains placeholders {time} and {time_unit}"""
tag_stc_Ti_min = defs.tag_stc_uo_settling_Ti_min
"""Tag for a flowsheet sentence for the unit operation settling: Minimum Ti for settling. contains placeholders {Ti_min}"""
tag_stc_Ti_max = defs.tag_stc_uo_settling_Ti_max
"""Tag for a flowsheet sentence for the unit operation settling: Maximum Ti for settling. contains placeholders {Ti_max}"""
tag_stc_Ti_range = defs.tag_stc_uo_settling_Ti_range
"""Tag for a flowsheet sentence for the unit operation settling: Ti range for settling. contains placeholders {Ti_min} and {Ti_max}"""
tag_stc_rec_duration = defs.tag_stc_uo_settling_rec_duration
"""Tag for a flowsheet sentence for the unit operation settling: record field for setting duration. contains placeholders {time_unit}"""
dict_stcs = defs.dict_jp_stcs_uo_settling
"""Japanese language dictionary for senteces in flowsheets for the unit operation settling"""



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

class Settling(uo.UnitOperation, uo_tag=defs.tag_uo_settling):
    def __init__(self,
                 caller: type[trdef.UniversalTrait] = None,
                 flowsheet: fsht.Flowsheet = None,
                 operation_seq: int = None,
                 num_subitems: int = None,
                 edit_comment:str = None):
        super().__init__(caller=caller, flowsheet=flowsheet, operation_seq=operation_seq, num_subitems=1, edit_comment=edit_comment)
        self.time_min:float = None
        self.time_max:float = None
        self.time_unit:str = None
        self.Ti_min:float = None
        self.Ti_max:float = None

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
        if not pd.isna(first_row[hedr_time_min]):
            self.time_min = first_row[hedr_time_min]
        if not pd.isna(first_row[hedr_time_max]):
            self.time_max = first_row[hedr_time_max]
        if self.time_min is not None and self.time_max is not None:
            if not pd.isna(first_row[hedr_time_unit]):
                self.time_unit = first_row[hedr_time_unit]
            else:
                self.time_unit = opt_time_unit_minute
                warnings.warn(message=f"{self.__class__.__name__}: No time unit is designated for Op. Seq {self.operation_seq} "
                                     "even though the minimum and/or maximum time has been provided. Time unit of minute is put "
                                     "just to keep the ball rolling.",
                                category=RuntimeWarning)
                # raise RuntimeWarning(f"{self.__class__.__name__}: No time unit is not designated for Op. Seq {self.operation_seq} "
                #                      "even though the minimum and/or maximum time has been provided. Time unit of minumte is put "
                #                      "just to keep the ball rolling.")
            
        if not pd.isna(first_row[hedr_Ti_min]):
            self.Ti_min = first_row[hedr_Ti_min]
        if not pd.isna(first_row[hedr_Ti_max]):
            self.Ti_max = first_row[hedr_Ti_max]


    def get_detail_header(self) -> list[str]:
        return list_hedr

    def get_detail_option_menu(self) -> Optional[dict[str, list[str]]]:
        return dict_opt
    
    def output_unit_operation(self):
        self.flowsheet.header_organizer(op_nr=self.operation_seq, title=lang_dict_uo_titles[self.uo_tag])
        if not (self.pre_comment == None or self.pre_comment == ''):
            self.flowsheet.put_body_comments(self.pre_comment)
            self.flowsheet.linefeed()        
        self.__put_settling_ini()
        if self.Ti_min is not None or self.Ti_max is not None:
            self.__put_temp_ctrl()
        self.flowsheet.linefeed()

        self.__put_final_check()
        self.flowsheet.linefeed()

        if not (self.post_comment == None or self.post_comment == ''):
            self.flowsheet.put_body_comments(self.post_comment)
            self.flowsheet.linefeed()

    def __put_settling_ini(self):
        sentence_instr_time:str = None
        if self.time_min is not None and self.time_max is not None:
            if self.time_min != self.time_max:
                sentence_instr_time = dict_stcs[tag_stc_time_range].format(time_min=self.time_min, time_max=self.time_max, time_unit=lang_dict_cmn[self.time_unit])
            else:
                sentence_instr_time = dict_stcs[tag_stc_time_single_point].format(time=self.time_min, time_unit=lang_dict_cmn[self.time_unit])
        elif self.time_min is not None:
            sentence_instr_time = dict_stcs[tag_stc_time_min].format(time_min=self.time_min, time_unit=lang_dict_cmn[self.time_unit])
        elif self.time_max is not None:
            sentence_instr_time = dict_stcs[tag_stc_time_max].format(time_max=self.time_max, time_unit=lang_dict_cmn[self.time_unit])
        else:
            sentence_instr_time = ""
        
        self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                method=dict_part_flow[tag_part_init_settling],
                                content=sentence_instr_time,
                                record=dict_part_flow[tag_part_rec_chk_agitator_stop],
                                operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
    
    def __put_temp_ctrl(self):
        sentence_instr_temp:str = None
        if self.Ti_min is not None and self.Ti_max is not None:
            sentence_instr_temp = dict_stcs[tag_stc_Ti_range].format(Ti_min=self.Ti_min, Ti_max=self.Ti_max)
        elif self.Ti_min is not None:
            sentence_instr_temp = dict_stcs[tag_stc_Ti_min].format(Ti_min=self.Ti_min)
        else:
            sentence_instr_temp = dict_stcs[tag_stc_Ti_max].format(Ti_max=self.Ti_max)
        
        self.flowsheet.put_line(content=sentence_instr_temp,
                                record=dict_part_flow[tag_part_rec_Tj_ini])
        self.flowsheet.put_line(record=dict_part_flow[tag_part_rec_Ti_ini])

    def __put_final_check(self):
        temp_time_unit:str = None
        if self.time_unit is not None:
            temp_time_unit=self.time_unit
        else:
            temp_time_unit=opt_time_unit_minute
        self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                method=dict_part_flow[tag_part_end_settling],
                                record=dict_stcs[tag_stc_rec_duration].format(time_unit=lang_dict_cmn[temp_time_unit]),
                                operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
        if self.Ti_min is not None or self.Ti_max is not None:
            self.flowsheet.put_line(record=dict_part_flow[tag_part_Tj_end])
            self.flowsheet.put_line(record=dict_part_flow[tag_part_Ti_end])