#########################################################
# imports
#########################################################
import pandas as pd
import flow_draw.definitions as defs
import flow_draw.data_io.flowsheet as fsht
from typing import Optional
from flow_draw.batch.process.unit_operations import unit_operation as uo
from flow_draw.data_io import process_io as procio
from flow_draw.trait_def import trait_def as trdef




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
hedr_spec_agit = defs.hedr_uo_agitation_spec
"""header item for the unit operation Agitation, the way the rotation rate is specified: specific rpm, guidance rpm, or discretion"""
hedr_rpm = defs.hedr_uo_agitation_rpm
"""header item for the unit operation Agitation, specific rotation rate"""
hedr_Ti_min = defs.hedr_uo_agitation_Ti_min
"""header item for the unit operation Agitation, specific Ti_min during agitation, optional"""
hedr_Ti_max = defs.hedr_uo_agitation_Ti_max
"""header item for the unit operation Agitation, specific Ti_max during agitation, optional"""
hedr_time_min = defs.hedr_uo_agitation_time_min
"""header item for the unit operation Agitation, minimum agitation time, optional"""
hedr_time_max = defs.hedr_uo_agitation_time_max
"""header item for the unit operation Agitation, maximum agitation time, optional"""
hedr_time_unit = defs.hedr_uo_agitation_time_unit
"""header item for the unit operation Agitation, second, minute, hour, day"""
hedr_dissolution_check = defs.hedr_uo_agitation_dissolution_check
"""header item for the unit operation Agitation, need for dissolution check. bool"""
list_hedr = defs.list_hedr_uo_agitation
"""List of uo-specific heder items for the unit operation Agitation"""


        ##### UO-specific option items for the detail input table #######
opt_spec_specif = defs.opt_uo_agitation_spec_specif
"""option for the header item 'spec'. Specifi RPM is provided by the user."""
opt_spec_guide = defs.opt_uo_agitation_spec_guide
"""option for the header item 'spec'. A guidance RPM is provided by the user."""
opt_spec_arbitrary = defs.opt_uo_agitation_spec_arbitrary


# list_opt_spec = defs.list_opt_uo_agitation_spec
# """List of options for the header item agitation_spec"""
# list_opt_time_unit = defs.list_opt_uo_agitation_time_unit
# """List of options for the header item agitation_time_unit"""
# list_opt_dissolution_check = defs.list_opt_uo_agitation_dissolution_check
# """List of options for the header item agitation_dissolution_check"""

dict_opt = defs.dict_opt_uo_agitation



#########################################################
# signal -> local language dictionary and tags for it
#########################################################
lang_dict_uo_titles = defs.dict_jp_part_uo_titles


        ##### Tags (keys) for translation of common parts ####
tag_flow_cmn_rec_time:str = defs.tag_flow_cmn_rec_time
"""The key to the time-recording field for the flowsheet, a common item."""
tag_flow_cmn_rec_sign:str = defs.tag_flow_cmn_rec_sign
"""The key to the ignature field for the flowsheet, a common item."""
tag_flow_cmn_time_unit_second:str = opt_time_unit_second
"""Tag for a common flowsheet component for an unit of time: second"""
tag_flow_cmn_time_unit_minute:str = opt_time_unit_minute
"""Tag for a common flowsheet component for an unit of time: minute"""
tag_flow_cmn_time_unit_hour:str = opt_time_unit_hour
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

tag_part_flow_title_disslnck = defs.tag_part_flow_uo_agitation_title_disslnck
"""Tag for a flowsheet component for uo_agitation: title for combined agitation and dissoltion check operation"""
tag_part_flow_instr_rpm_arbitrary = defs.tag_part_flow_uo_agitation_instr_rpm_arbitrary
"""Tag for a flowsheet component for uo_agitation: instruction for totally arbitrary agitation rate"""
tag_part_flow_rec_rpm_act = defs.tag_part_flow_uo_agitation_rec_rpm_act
"""Tag for a flowsheet component for uo_agitation: record field for agitation rate"""
tag_part_flow_rec_chk_agit_ini = defs.tag_part_flow_uo_agitation_rec_chk_agit_ini
"""Tag for a flowsheet component for uo_agitation: check box for agitation initiation"""
tag_part_flow_rec_Tj_ini = defs.tag_part_flow_uo_agitation_rec_Tj_ini
"""Tag for a flowsheet component for uo_agitation: recording field for initial Tj"""
tag_part_flow_rec_Ti_ini = defs.tag_part_flow_uo_agitation_rec_Ti_ini
"""Tag for a flowsheet component for uo_agitation: recording field for initial Ti"""
tag_part_flow_instr_dissoln_check_visual = defs.tag_part_flow_uo_agitation_instr_dissoln_check_visual
"""Tag for a flowsheet component for uo_agitation: instruction for dissolution chec by visual"""
tag_part_flow_rec_chk_dissoln = defs.tag_part_flow_uo_agitation_rec_chk_dissoln
"""Tag for a flowsheet component for uo_agitation: check box for dissolution"""
tag_part_flow_rec_final_Tj = defs.tag_part_flow_uo_agitation_rec_final_Tj
"""Tag for a flowsheet component for uo_agitation: recording field for final Tj"""
tag_part_flow_rec_final_Ti = defs.tag_part_flow_uo_agitation_rec_final_Ti
"""Tag for a flowsheet component for uo_agitation: recording field for final Ti"""
tag_part_flow_rec_dissoln_Tj = defs.tag_part_flow_uo_agitation_rec_dissoln_Tj
"""Tag for a flowsheet component for uo_agitation: recording field for Tj at the time of dissolution"""
tag_part_flow_rec_dissoln_Ti = defs.tag_part_flow_uo_agitation_rec_dissoln_Ti
"""Tag for a flowsheet component for uo_agitation: recording field for Ti at the time of dissolution"""
tag_part_flow_rec_chk_agit_compl = defs.tag_part_flow_uo_agitation_rec_chk_agit_compl
"""Tag for a flowsheet component for uo_agitation: check box for agitation completion"""
dict_part_flow = defs.dict_part_flow_uo_agitation_jp
"""Japanese lanugae dictionary for flowsheet part for the unit operation Agitation"""


tag_stc_flow_rpm_spec = defs.tag_stc_flow_uo_agitation_rpm_spec
"""Tag for a sentence for the unit operation Agitation: instruction for agitation at an specified agitation rate, includes a placeholder {rpm}"""
tag_stc_flow_rpm_guidance = defs.tag_stc_flow_uo_agitation_rpm_guidance
"""Tag for a sentence for the unit operation Agitation: instruction for agitation with a guideline rate, includes a placeholder {rpm}"""
tag_stc_flow_Ti_range = defs.tag_stc_flow_uo_agitation_Ti_range
"""Tag for a sentence for the unit operation Agitation: Instrction on temperature range. Includes placeholders {Ti_min} and {Ti_max}"""
tag_stc_flow_Ti_min = defs.tag_stc_flow_uo_agitation_Ti_min
"""Tag for a sentence for the unit operation Agitation: Instruction on minimum temperature. Includes placeholder {Ti_min}"""
tag_stc_flow_Ti_max = defs.tag_stc_flow_uo_agitation_Ti_max
"""Tag for a sentence for the unit operation Agitation: Instruction on maximum temperature. Includes placeholder {Ti_max}"""
tag_stc_flow_time_range = defs.tag_stc_flow_uo_agitation_time_range
"""Tag for a sentence for the unit operation Agitation: Instruction on agitation time range. Includes placeholders {time_min}, {time_max} , and {time_unit}"""
tag_stc_flow_time_min = defs.tag_stc_flow_uo_agitation_time_min
"""Tag for a sentence for the unit operation Agitation: Instruction on minimum agitation time. Includes placeholders {time_min} and {time_unit}"""
tag_stc_flow_time_max = defs.tag_stc_flow_uo_agitation_time_max
"""Tag for a sentence for the unit operation Agitation: Instruction on maximum agitation time. Includes {time_max} and {time_unit}"""
tag_stc_flow_time_single_point = defs.tag_stc_flow_uo_agitation_time_single_point
"""Tag for a sentence for the unit operation Agitation: Instruction on agitation time (single point). Includes a placeholder {time} and {time_unit}"""
tag_stc_flow_rec_duration = defs.tag_stc_flow_uo_agitation_rec_duration
"""Tag for a sentence for the unit operation Agitation: Record field for agitation duration, includes a placeholder {time_unit}"""
dict_stcs = defs.dict_jp_stcs_uo_agitation
"""Japanese language dictionary for sentences for flowsheet for the unit operation Agitation"""

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

class Agitation(uo.UnitOperation, uo_tag=defs.tag_uo_agitation):
    def __init__(self,
                 caller:type[trdef.UniversalTrait] = None,
                 flowsheet:fsht.Flowsheet = None,
                 operation_seq:int = None,
                 num_subitems: int = None,
                 edit_comment:str = None):
        super().__init__(caller=caller, flowsheet=flowsheet, operation_seq=operation_seq, num_subitems=num_subitems, edit_comment=edit_comment)
        self.spec_agit: str = None
        self.rpm: float = None
        self.Ti_min: float = None
        self.Ti_max: float = None
        self.time_min: float = None
        self.time_max: float = None
        self.time_unit: str = None
        self.dissolution_check: bool = False



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
        
        if not pd.isna(first_row[hedr_spec_agit]):
            self.spec_agit = first_row[hedr_spec_agit]
        else:
            raise RuntimeError(f"{self.__class__.__name__}: \"{hedr_spec_agit}\" not specified in the detail input worksheet \
                               for Op. Seq. {self.operation_seq}.")
        
        if self.spec_agit == opt_spec_specif or self.spec_agit == opt_spec_guide:
            if not pd.isna(first_row[hedr_rpm]):
                self.rpm = first_row[hedr_rpm]
            else:
                raise RuntimeError(f"{self.__class__.__name__}: \"{hedr_rpm}\" not specified in the detail input worksheet \
                                   for Op. Seq. {self.operation_seq} although the user chose to provide a specific rotation rate \
                                    in the column \"{hedr_spec_agit}\".")
        else:
            if not pd.isna(first_row[hedr_rpm]):
                self.rpm = first_row[hedr_rpm]
    
        if not pd.isna(first_row[hedr_Ti_min]):
            self.Ti_min = first_row[hedr_Ti_min]
        
        if not pd.isna(first_row[hedr_Ti_max]):
            self.Ti_max = first_row[hedr_Ti_max]

        if not pd.isna(first_row[hedr_time_min]):
            self.time_min = first_row[hedr_time_min]
    
        if not pd.isna(first_row[hedr_time_max]):
            self.time_max = first_row[hedr_time_max]
        
        if self.time_min is not None or self.time_max is not None:
            if not pd.isna(first_row[hedr_time_unit]):
                self.time_unit = first_row[hedr_time_unit]
            else:
                self.time_unit = lang_dict_cmn[opt_time_unit_minute]
                raise RuntimeWarning(f"{self.__class__.__name__}: \"{hedr_time_unit}\" not selected in the detail input worksheet \
                                     for Op. Seq. {self.operation_seq} although minimum and/or maximum agitation time has benn provided \
                                     in the worksheet. Time unit of \"min\" is used to keep the ball rolling.")
        
        if first_row[hedr_dissolution_check] == opt_yes:
            self.dissolution_check = True


    def get_detail_header(self) -> list[str]:
        return list_hedr

    def get_detail_option_menu(self) -> Optional[dict[str, list[str]]]:
        return dict_opt
    
    def output_unit_operation(self):
        self.flowsheet.header_organizer(op_nr=self.operation_seq, title=lang_dict_uo_titles[self.uo_tag])
        if not (self.pre_comment == None or self.pre_comment == ''):
            self.flowsheet.put_body_comments(self.pre_comment)
            self.flowsheet.linefeed()        

        self.__put_rpm_control()
        if self.time_min is not None or self.time_max is not None:
            self.__put_time_control()
        if self.Ti_min is not None or self.Ti_max is not None:
            self.__put_temp_control()
        self.flowsheet.linefeed()

        self.__put_final_check()
        self.flowsheet.linefeed()

        if not (self.post_comment == None or self.post_comment == ''):
            self.flowsheet.put_body_comments(self.post_comment)
            self.flowsheet.linefeed()
    

    def __put_rpm_control(self):
        stc_rpm_ctrl: str = None
        if self.spec_agit==opt_spec_specif:
            stc_rpm_ctrl = dict_stcs[tag_stc_flow_rpm_spec].format(rpm=self.rpm)
        elif self.spec_agit==opt_spec_guide:
            stc_rpm_ctrl = dict_stcs[tag_stc_flow_rpm_guidance].format(rpm=self.rpm)
        else:
            stc_rpm_ctrl = dict_part_flow[tag_part_flow_instr_rpm_arbitrary]
        self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                content=stc_rpm_ctrl,
                                record=dict_part_flow[tag_part_flow_rec_rpm_act],
                                operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                witness=lang_dict_cmn[tag_flow_cmn_rec_sign])

    def __put_time_control(self):
        stc_time_ctrl:str = None
        if self.time_min is not None and self.time_max is not None:
            if self.time_min != self.time_max:
                stc_time_ctrl = dict_stcs[tag_stc_flow_time_range].format(time_min=self.time_min, time_max=self.time_max, time_unit=self.time_unit)
            else:
                stc_time_ctrl = dict_stcs[tag_stc_flow_time_single_point].format(time=self.time_min, time_unit=self.time_unit)
        elif self.time_min is not None:
            stc_time_ctrl = dict_stcs[tag_stc_flow_time_min].format(time_min=self.time_min, time_unit=self.time_unit)
        elif self.time_max is not None:
            stc_time_ctrl = dict_stcs[tag_stc_flow_time_max].format(time_max=self.time_max, time_unit=self.time_unit)
        else:
            raise RuntimeWarning(f"{__class__.__name__}: Wrong call for __put_time_control() in Op. Seq. {self.operation_seq}.")
        self.flowsheet.put_line(content=stc_time_ctrl)
    
    def __put_temp_control(self):
        stc_temp_ctrl:str = None
        if self.Ti_min is not None and self.Ti_max is not None:
            stc_temp_ctrl = dict_stcs[tag_stc_flow_Ti_range].format(Ti_min=self.Ti_min, Ti_max=self.Ti_max)
        elif self.Ti_min is not None:
            stc_temp_ctrl = dict_stcs[tag_stc_flow_Ti_min].format(Ti_min=self.Ti_min)
        elif self.Ti_max is not None:
            stc_temp_ctrl = dict_stcs[tag_stc_flow_Ti_max].format(Ti_min=self.Ti_max)
        else:
            raise RuntimeWarning(f"{__class__.__name__}: Wrong call for __put_temp_control() in Op. Seq. {self.operation_seq}.")

        self.flowsheet.put_line(content=stc_temp_ctrl,
                                record=dict_part_flow[tag_part_flow_rec_Tj_ini])
        self.flowsheet.put_line(record=dict_part_flow[tag_part_flow_rec_Ti_ini])       


    def __put_final_check(self):
        if self.dissolution_check:
            self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                    content=dict_part_flow[tag_part_flow_instr_dissoln_check_visual],
                                    record=dict_part_flow[tag_part_flow_rec_chk_dissoln],
                                    operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
            if self.time_min is not None or self.time_max is not None:
                self.flowsheet.put_line(record=dict_stcs[tag_stc_flow_rec_duration].format(time_unit=self.time_unit))
            self.flowsheet.put_line(record=dict_part_flow[tag_part_flow_rec_dissoln_Tj])
            self.flowsheet.put_line(record=dict_part_flow[tag_part_flow_rec_dissoln_Ti])
        elif self.Ti_min is not None or self.Ti_max is not None:
            self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                    record=dict_part_flow[tag_part_flow_rec_chk_agit_compl],
                                    operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
            self.flowsheet.put_line(record=dict_part_flow[tag_part_flow_rec_final_Tj])
            self.flowsheet.put_line(record=dict_part_flow[tag_part_flow_rec_final_Ti])
            if self.time_min is not None or self.time_max is not None:
                self.flowsheet.put_line(record=dict_stcs[tag_stc_flow_rec_duration].format(time_unit=self.time_unit))
        else:
            self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                    record=dict_part_flow[tag_part_flow_rec_chk_agit_compl],
                                    operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
            if self.time_min is not None or self.time_max is not None:
                self.flowsheet.put_line(record=dict_stcs[tag_stc_flow_rec_duration].format(time_unit=self.time_unit))

            