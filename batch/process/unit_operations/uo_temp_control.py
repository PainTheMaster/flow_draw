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

#########################################################
# UO-specific options, list, header_item: list dictionry thereof (for data input and internalsignaling)
#########################################################

            ##### header items for detail worksheet######
hedr_mode:str = defs.hedr_uo_tempr_ctrl_mode
"""Detail heder item: temperature control mode (e.g. Ti, Ti/Tj, amping)"""
hedr_Ti_sp:str = defs.hedr_uo_tempr_ctrl_Ti_sp
"""Detail heder item: Ti set point for Ti, Ti/Tj mode"""
hedr_Ti_limit_low:str = defs.hedr_uo_tempr_ctrl_Ti_limit_low
"""Detail heder item: Ti lower limit designaetd by the process owner."""
hedr_Ti_limit_high:str = defs.hedr_uo_tempr_ctrl_Ti_limit_high
"""Detail heder item: Ti upper limit designated by the process owner."""
hedr_Ti_tgt_low:str = defs.hedr_uo_tempr_ctrl_Ti_tgt_low
"""Detail heder item: Ti TARGET lower limit designated by the process owner."""
hedr_Ti_tgt_high:str = defs.hedr_uo_tempr_ctrl_Ti_tgt_high
"""Detail heder item: Ti TARGET higher limit designated by the process owner."""
hedr_Tj_sp:str = defs.hedr_uo_tempr_ctrl_Tj_sp
"""Detail heder item: Tj set point for Tj mode"""
hedr_Tj_limit_low:str = defs.hedr_uo_tempr_ctrl_Tj_limit_low
"""Detail heder item: Tj lower limit for Tj, Ti/Tj mode."""
hedr_Tj_lmit_high:str = defs.hedr_uo_tempr_ctrl_Tj_limit_high
"""Detail heder item: Tj higher limit for Tj, Ti/Tj mode"""
#hedr_Ti_prog_sp_end:str = defs.hedr_uo_tempr_ctrl_prog_Ti_sp_end
#hedr_Ti_prog_sp_end:str = defs.hedr_uo_tempr_ctrl_Ti_sp #TODO check if this is needed. Now, programme mode uses just Ti_sp
"""Detail heder item: Ti end target for ramp mode"""
hedr_prog_time_val:str = defs.hedr_uo_tempr_ctrl_prog_time_val
"""Detail heder item: Ramp up/down time value"""
hedr_prog_time_unit:str = defs.hedr_uo_tempr_ctrl_prog_time_unit
"""Detail heder item: Ramp up/down time unit"""
hedr_endpoint_check:str = defs.hedr_uo_tempr_ctrl_endpoint_check
"""Detail heder item: need for heating/cooling end point check."""

list_hedr:list[str] = defs.list_hedr_uo_tempr_ctrl
"""List of header items for unit operation temperature controle"""


        ##### UO-specific option items for the detail input table #######
#For hedr_uo_tempr_ctrl_mode
opt_mode_TiTj:str = defs.opt_uo_tempr_ctrl_mode_TiTj
"""Option for detail table: temperature control with single point Ti and Tj range"""
opt_mode_Tj:str = defs.opt_uo_tempr_ctrl_mode_Tj
"""Option for detail table: temperature control on jacket temperature (single point)"""
opt_mode_prog:str = defs.opt_uo_tempr_ctrl_mode_prog
"""Option for detail table: temperature ramping, cooling or heating with time constraint"""
opt_mode_Ti:str = defs.opt_uo_tempr_ctrl_mode_Ti
"""Option for detail table: temperature control on liquid temperature (single point)"""
# list_opt_mode = defs.list_opt_uo_tempr_ctrl_mode
# """List of a series of temperature control options"""


opt_check_endpoint_yes:str = opt_yes
"""Option for detail table: Need for temperature control endpoint check-box--yes"""
opt_check_endpoint_no:str = opt_no
"""Option for detail table: Need for temperature control endpoint check-box--no"""


tag_flow_cmn_time_unit_second:str = defs.tag_flow_cmn_time_unit_second
"""Tag for a common flowsheet component for an unit of time: second"""
tag_flow_cmn_time_unit_minute:str = defs.tag_flow_cmn_time_unit_minute
"""Tag for a common flowsheet component for an unit of time: minute"""
tag_flow_cmn_time_unit_hour:str = defs.tag_flow_cmn_time_unit_hour
"""Tag for a common flowsheet component for an unit of time: hour"""

# list_opt_check_endpoint=defs.list_opt_uo_tempr_ctrl_check_endpoint
# """List options for detail table: Need for temperature control endpoint check-box--yes/no"""


dict_opt:dict[str, list[str]] = defs.dict_opt_uo_tempr_ctrl
"""Dictionary for detail input form for the unit operation uo_tempr_ctrl"""


#########################################################
# signal -> local language dictionary and tags for it
#########################################################
lang_dict_uo_titles:dict[str, str] = defs.dict_jp_part_uo_titles


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

                    #------------- component dictionary ---------------------

tag_part_flow_title_tempr_config:str = defs.tag_part_flow_tempr_ctrl_title_tempr_config
"""Tag for a flowsheet component: Unit operation title for temperature configuration."""
tag_part_flow_title_compl_tempr_ctrl:str = defs.tag_part_flow_tempr_ctrl_title_compl_tempr_ctrl
"""Tag for a flowsheet component: Unit operation title for complete temperature control."""
# tag_part_flow_prog_mode:str = defs.tag_part_flow_tempr_ctrl_prog_mode
# """Tag for a flowsheet component: Instruction for progremme heating/cooling mode"""
tag_part_flow_instr_init_temp_ctrl:str = defs.tag_part_flow_tempr_ctrl_instr_init_temp_ctrl
"""Tag for a flowsheet component: Instruction to activate temperature control."""
tag_part_flow_instr_compl_temp_ctrl:str = defs.tag_part_flow_tempr_ctrl_instr_compl_temp_ctrl
"""Tag for a flowsheet component: Instrction to complete the temperature control."""
tag_part_flow_instr_check_Ti_in_range:str = defs.tag_part_flow_tempr_ctrl_instr_check_Ti_in_range
"""Tag for a flowsheet component: Instrction to check if the Ti is in range."""
tag_part_flow_check_config:str = defs.tag_part_flow_tempr_ctrl_check_config
"""Tag for a flowsheet part: check-box for temperature configuration."""
tag_part_flow_check_activate:str = defs.tag_part_flow_tempr_ctrl_check_activate
"""Tag for a flowsheet part: check-box for activation of temperature control."""
tag_part_flow_check_endpoint:str = defs.tag_part_flow_tempr_ctrl_check_endpoint
"""Tag for a flowsheet part: check-box for temperature end point"""
tag_part_flow_rec_Ti_ini:str = defs.tag_part_flow_tempr_ctrl_rec_Ti_ini
"""Tag for a flowsheet part: recrd field for initial Ti"""
tag_part_flow_rec_Ti_end:str = defs.tag_part_flow_tempr_ctrl_rec_Ti_end
"""Tag for a flowsheet part: recrd field for end Ti"""
lang_dict_parts_flow:dict[str, str]  = defs.dict_jp_part_flow_tempr_ctrl
"""Japanese language dictionary for flowsheet parts for unit operation temperature control."""


                    #------------- Sentece dictionary ---------------------

tag_stc_Tj_sp:str = defs.tag_stc_tempr_ctrl_Tj_sp
"""Tag for an instruction sentence for temperature control. Tj set point. Includes placeholder{Tj}"""
tag_stc_Ti_Tj_config:str = defs.tag_stc_tempr_ctrl_Ti_Tj_config
"""Tag for an instruction sentence for temperature control. Ti/Tj configuration. Includes placeholder{Ti}, {Tj_low}, and {Tj_high}"""
tag_stc_prog_mode:str = defs.tag_stc_tempr_ctrl_prog_mode
"""Tag for an instruction sentence for temperature control. Programme mode. Includes placeholder{Ti}, {Tj_low}, and {Tj_high}"""
tag_stc_prog_duration_minimum:str = defs.tag_stc_tempr_ctrl_prog_duration_minimum
"""Sentence template for temperature control. Time requirement for programme heating/cooling mode. Includes  placeholders {time_min} and {time_unit}."""
tag_stc_Ti_range:str = defs.tag_stc_tempr_ctrl_Ti_range
"""Tag for an instruction sentence for temperature control. Ti range Includes placeholder {Ti_low} and {Ti_high}"""
tag_stc_prog_term_Ti_range:str = defs.tag_stc_tempr_ctrl_prog_term_Ti_range
"""Tag for an instruction sentence for temperature control. Programme mode terminal Ti range. Includes placeholder {Ti_low} and {Ti_high}"""
tag_stc_Ti_high_limit_only:str = defs.tag_stc_tempr_ctrl_Ti_high_limit_only
"""Tag for an instruction sentence for temperature control. Ti upper limit only, includes placeholder {Ti_high}"""
tag_stc_Ti_low_limit_only:str = defs.tag_stc_tempr_ctrl_Ti_low_limit_only
"""Tag for an instruction sentence for temperature control. Ti lower limit only, includes placeholder {Ti_low}"""
tag_stc_Ti_tgt_range:str = defs.tag_stc_tempr_ctrl_Ti_tgt_range
"""Tag for an instruction sentence for temperature control. Ti target range. Includes placeholder {Ti_low} and {Ti_high}."""
tag_stc_Ti_tgt_single:str = defs.tag_stc_tempr_ctrl_Ti_tgt_single
"""Tag for an instruction sentence for temperature control. Ti target single point.  Includes placeholder {Ti}"""
tag_stc_Ti_spec_sp_single:str = defs.tag_stc_tempr_ctrl_Ti_spec_sp_single
"""Tag for an instruction sentence for temperature control. Ti specification single point for Ti mode. Includes placeholder {Ti}"""
tag_stc_duration:str = defs.tag_stc_flow_tempr_ctrl_result_duration
"""Tag for a record field for temperature control (cooling/heating) duration in a specic time unit. Includes a placeholder {time_unit}"""
lang_dict_stcs:dict[str, str] = defs.dict_jp_stcs_tempr_ctrl
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
        super().__init__(caller=caller, flowsheet=flowsheet, operation_seq=operation_seq, num_subitems=1, edit_comment=edit_comment)
        self.ctrl_mode:str = None
        """Temperature control mode: Ti/Tj, Tj, programme, Ti"""
        self.Ti_sp:float = None
        """Ti (single) set point for Ti/Tj, programme, and Ti mode"""
        self.Ti_limit_low:float = None
        """Ti lower limit (instructed by the process owner)"""
        self.Ti_limit_high:float = None
        """Ti higher limit (instructed by the process owner)"""
        self.Ti_tgt_low:float = None
        """Lower end of Ti target range (instructed by the process woner)"""
        self.Ti_tgt_high:float = None
        """Higher end of Ti target range (instructed by the process woner)"""
        self.Tj_sp:float = None
        """Tj set point for Tj control mode"""
        self.Tj_limit_low:float = None
        """Lower limit of Tj range for Ti/Tj and programme mode"""
        self.Tj_limit_high:float = None
        """Higher limit of Tj range for Ti/Tj and programme mode"""
        # self.Ti_prog_sp:float = None
        # """Ti set point for programme heating/cooling mode."""
        self.time_val_prog:float = None
        """Ramp time for programme heating/cooling mode"""
        self.time_unit_prog:str = None
        """Time unit (normally minute or hours) for programme heatin/cooling mode"""
        self.endpoint_check:bool = None
        """Need for temperature control end point check. (temperature reached)"""


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

        if not pd.isna(first_row[hedr_mode]):
            self.ctrl_mode = first_row[hedr_mode]
        else:
            raise ValueError(f"{self.__class__.__name__}: Op. Seq. {self.operation_seq}: Temperature control mode not selected in the input form.")

        if not pd.isna(first_row[hedr_Ti_sp]):
            self.Ti_sp = float(first_row[hedr_Ti_sp])

        if not pd.isna(first_row[hedr_Ti_limit_low]):
            self.Ti_limit_low = float(first_row[hedr_Ti_limit_low])

        if not pd.isna(first_row[hedr_Ti_limit_high]):
            self.Ti_limit_high = float(first_row[hedr_Ti_limit_high])

        if not pd.isna(first_row[hedr_Ti_tgt_low]):
            self.Ti_tgt_low = float(first_row[hedr_Ti_tgt_low])
        
        if not pd.isna(first_row[hedr_Ti_tgt_high]):
            self.Ti_tgt_high = float(first_row[hedr_Ti_tgt_high])
        
        if not pd.isna(first_row[hedr_Tj_sp]):
            self.Tj_sp = float(first_row[hedr_Tj_sp])
                
        if not pd.isna(first_row[hedr_Tj_limit_low]):
            self.Tj_limit_low = float(first_row[hedr_Tj_limit_low])
                
        if not pd.isna(first_row[hedr_Tj_lmit_high]):
            self.Tj_limit_high = float(first_row[hedr_Tj_lmit_high])
                
        # if not pd.isna(first_row[hedr_Ti_prog_sp_end]):
        #     self.Ti_prog_sp = float(first_row[hedr_Ti_prog_sp_end])
                
        if not pd.isna(first_row[hedr_prog_time_val]):
            self.time_val_prog = float(first_row[hedr_prog_time_val])
            if not pd.isna(first_row[hedr_prog_time_unit]):
                self.time_unit_prog = first_row[hedr_prog_time_unit]
            else:
                raise RuntimeWarning(f"{self.__class__.__name__}: Op. Seq. {self.operation_seq} temperature control: Ramp time for programme heating/cooling defined, but its unit (min, hour, etc) not selected in the form.")
                
        self.endpoint_check = (first_row[hedr_endpoint_check] == opt_yes)
        """first_row[hedr_endpoint_check] shall has a value of 'Yes', 'No', NaN or something else. Only 'Yes' is regarded as the affirmative choice."""




    def __put_TiTj_mode(self):
        stc_spec:str = None
        if self.Ti_limit_low is None and self.Ti_limit_high is None:
            raise ValueError(f"{self.__class__.__name__}: Op. Seq. {self.operation_seq} Ti limit not specified in the input form for Ti/Tj control mode.")
        elif self.Ti_limit_low is not None and self.Ti_limit_high is None:
            stc_spec = lang_dict_stcs[tag_stc_Ti_low_limit_only].format(Ti_low=self.Ti_limit_low)
        elif self.Ti_limit_low is None and self.Ti_limit_high is not None:
            stc_spec = lang_dict_stcs[tag_stc_Ti_high_limit_only].format(Ti_high=self.Ti_limit_high)
        else:
            stc_spec = lang_dict_stcs[tag_stc_Ti_range].format(Ti_low=self.Ti_limit_low, Ti_high=self.Ti_limit_high)

        stc_target:str = None        
        if self.Ti_tgt_low is None and self.Ti_tgt_high is None:
            pass
        elif self.Ti_tgt_low is not None and self.Ti_tgt_high is None:
            stc_target = lang_dict_stcs[tag_stc_Ti_tgt_single].format(Ti=self.Ti_tgt_low)
        elif self.Ti_tgt_low is None and self.Ti_tgt_high is not None:
            stc_target = lang_dict_stcs[tag_stc_Ti_tgt_single].format(Ti=self.Ti_tgt_high)
        elif self.Ti_tgt_low == self.Ti_tgt_high:
            stc_target = lang_dict_stcs[tag_stc_Ti_tgt_single].format(Ti=self.Ti_tgt_high)
        else:
            stc_target = lang_dict_stcs[tag_stc_Ti_tgt_range].format(Ti_low=self.Ti_tgt_low , Ti_high=self.Ti_tgt_high)
        
        stc_concat_ranges:str = None
        if stc_target is None:
            stc_concat_ranges = stc_spec
        else:
            stc_concat_ranges = stc_spec+" ("+stc_target+")"


        self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                method=lang_dict_parts_flow[tag_part_flow_instr_init_temp_ctrl],
                                content=lang_dict_stcs[tag_stc_Ti_Tj_config].format(Ti=self.Ti_sp, Tj_low=self.Tj_limit_low, Tj_high=self.Tj_limit_high),
                                record=lang_dict_parts_flow[tag_part_flow_check_config],
                                operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
        self.flowsheet.put_line(content=stc_concat_ranges,
                                record=lang_dict_parts_flow[tag_part_flow_rec_Ti_ini])
        self.flowsheet.linefeed()
        # if self.endpoint_check:
        #     self.flowsheet.linefeed()
        #     self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
        #                             content=lang_dict_parts_flow[tag_part_flow_instr_check_Ti_in_range],
        #                             record=lang_dict_parts_flow[tag_part_flow_check_endpoint],
        #                             operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
        #                             witness=lang_dict_cmn[tag_flow_cmn_rec_sign])

    def __put_Tj_mode(self):
        sentence_Tj:str = None
        if self.Tj_sp is None:
            raise ValueError(f"{self.__class__.__name__}: Op. Seq. {self.operation_seq} Tj not specified in the input form for Tj control mode.")
        else:
            sentence_Tj = lang_dict_stcs[tag_stc_Tj_sp].format(Tj=self.Tj_sp)
        
        stc_spec_Ti:str = None
        if self.Ti_limit_low is None and self.Ti_limit_high is None:
            pass
        elif self.Ti_limit_low is not None and self.Ti_limit_high is None:
            stc_spec_Ti = lang_dict_stcs[tag_stc_Ti_low_limit_only].format(Ti_low=self.Ti_limit_low)
        elif self.Ti_limit_low is None and self.Ti_limit_high is not None:
            stc_spec_Ti = lang_dict_stcs[tag_stc_Ti_high_limit_only].format(Ti_high=self.Ti_limit_high)
        else:
            stc_spec_Ti = lang_dict_stcs[tag_stc_Ti_range].format(Ti_low=self.Ti_limit_low, Ti_high=self.Ti_limit_high)

        stc_target_Ti:str = None        
        if self.Ti_tgt_low is None and self.Ti_tgt_high is None:
            pass
        elif self.Ti_tgt_low is not None and self.Ti_tgt_high is None:
            stc_target_Ti = lang_dict_stcs[tag_stc_Ti_tgt_single].format(Ti=self.Ti_tgt_low)
        elif self.Ti_tgt_low is None and self.Ti_tgt_high is not None:
            stc_target_Ti = lang_dict_stcs[tag_stc_Ti_tgt_single].format(Ti=self.Ti_tgt_high)
        elif self.Ti_tgt_low == self.Ti_tgt_high:
            stc_target_Ti = lang_dict_stcs[tag_stc_Ti_tgt_single].format(Ti=self.Ti_tgt_high)
        else:
            stc_target_Ti = lang_dict_stcs[tag_stc_Ti_tgt_range].format(Ti_low=self.Ti_tgt_low , Ti_high=self.Ti_tgt_high)
        
        stc_concat_Ti_ranges:str = None
        if stc_spec_Ti is None and stc_target_Ti is None:
            pass
        elif stc_spec_Ti is not None and stc_target_Ti is None:
            stc_concat_Ti_ranges = stc_spec_Ti
        elif stc_spec_Ti is None and stc_target_Ti is not None:
            stc_concat_Ti_ranges = stc_target_Ti
        else:
            stc_concat_Ti_ranges = stc_spec_Ti+" ("+stc_target_Ti+")"
        
        self.flowsheet.put_line(time = lang_dict_cmn[tag_flow_cmn_rec_time],
                                method=lang_dict_parts_flow[tag_part_flow_instr_init_temp_ctrl],
                                content=sentence_Tj,
                                record=lang_dict_parts_flow[tag_part_flow_check_config],
                                operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
        if stc_concat_Ti_ranges is None:
            self.flowsheet.put_line(record=lang_dict_parts_flow[tag_part_flow_rec_Ti_ini])
        else:
            self.flowsheet.put_line(content=stc_concat_Ti_ranges,
                                    record=lang_dict_parts_flow[tag_part_flow_rec_Ti_ini])
        self.flowsheet.linefeed()

    def __put_programme_mode(self):
        self.endpoint_check = True
        instr_main_sentence:str = None
        if self.Ti_sp is None:
            raise ValueError(f"{self.__class__.__name__}: Op. Seq. {self.operation_seq} Ti set point not specified in the input form for programme temperature control mode.")
        elif self.Tj_limit_low is None:
            raise ValueError(f"{self.__class__.__name__}: Op. Seq. {self.operation_seq} Tj lower limit not specified in the input form for programme temperature control mode.")
        elif self.Tj_limit_high is None:
            raise ValueError(f"{self.__class__.__name__}: Op. Seq. {self.operation_seq} Tj higher limit not specified in the input form for programme temperature control mode.")
        else:
            instr_main_sentence = lang_dict_stcs[tag_stc_prog_mode].format(Ti=self.Ti_sp, Tj_low=self.Tj_limit_low, Tj_high=self.Tj_limit_high)
        
        instr_ramp_time_sentence:str = None
        if self.time_val_prog is None:
            raise ValueError(f"{self.__class__.__name__}: Op. Seq. {self.operation_seq} ramp time value for temperature control not specified in the input form for programme control mode.")
        elif self.time_unit_prog is None:
            raise ValueError(f"{self.__class__.__name__}: Op. Seq. {self.operation_seq} ramp time unit for temperature control not specified in the input form for programme control mode.")
        else:
            instr_ramp_time_sentence = lang_dict_stcs[tag_stc_prog_duration_minimum].format(time_min=self.time_val_prog, time_unit=lang_dict_cmn[self.time_unit_prog])
        
        instr_Ti_range:str = None
        if self.Ti_limit_low is None:
            raise ValueError(f"{self.__class__.__name__}: Op. Seq. {self.operation_seq} Ti lower limit not specified in the input form for programme control mode.")
        elif self.Ti_limit_high is None:
            raise ValueError(f"{self.__class__.__name__}: Op. Seq. {self.operation_seq} Ti higher limit not specified in the input form for programme control mode.")
        else:
            instr_Ti_range = lang_dict_stcs[tag_stc_prog_term_Ti_range].format(Ti_low=self.Ti_limit_low, Ti_high=self.Ti_limit_high)

        self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                method=lang_dict_parts_flow[tag_part_flow_instr_init_temp_ctrl],
                                content=instr_main_sentence,
                                record=lang_dict_parts_flow[tag_part_flow_check_config],
                                operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
        self.flowsheet.put_line(content=instr_ramp_time_sentence,
                                record=lang_dict_parts_flow[tag_part_flow_check_activate])
        self.flowsheet.put_line(content=instr_Ti_range,
                                record=lang_dict_parts_flow[tag_part_flow_rec_Ti_ini])
        # self.flowsheet.put_line(record=lang_dict_parts_flow[tag_part_flow_rec_Ti_ini])
        self.flowsheet.linefeed()
        # self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
        #                         method=lang_dict_parts_flow[tag_part_flow_instr_compl_temp_ctrl],
        #                         content=lang_dict_parts_flow[tag_part_flow_instr_check_Ti_in_range],
        #                         record=lang_dict_parts_flow[tag_part_flow_check_endpoint],
        #                         operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
        #                         witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
        # self.flowsheet.put_line(record=lang_dict_stcs[tag_stc_duration].format(time_unit=self.time_unit_prog))
        # self.flowsheet.put_line(record=lang_dict_parts_flow[tag_part_flow_rec_Ti_end])




    def __put_Ti_mode(self):
        sentence_sp_Ti:str = None
        if self.Ti_sp is None:
            raise ValueError(f"{self.__class__.__name__}: Op. Seq. {self.operation_seq} Ti not specified in the input form for Ti control mode.")
        else:
            sentence_sp_Ti = lang_dict_stcs[tag_stc_Ti_spec_sp_single].format(Ti=self.Ti_sp)
        
        stc_spec_Ti:str = None
        if self.Ti_limit_low is None and self.Ti_limit_high is None:
            pass
        elif self.Ti_limit_low is not None and self.Ti_limit_high is None:
            stc_spec_Ti = lang_dict_stcs[tag_stc_Ti_low_limit_only].format(Ti_low=self.Ti_limit_low)
        elif self.Ti_limit_low is None and self.Ti_limit_high is not None:
            stc_spec_Ti = lang_dict_stcs[tag_stc_Ti_high_limit_only].format(Ti_high=self.Ti_limit_high)
        else:
            stc_spec_Ti = lang_dict_stcs[tag_stc_Ti_range].format(Ti_low=self.Ti_limit_low, Ti_high=self.Ti_limit_high)

        stc_target_Ti:str = None        
        if self.Ti_tgt_low is None and self.Ti_tgt_high is None:
            pass
        elif self.Ti_tgt_low is not None and self.Ti_tgt_high is None:
            stc_target_Ti = lang_dict_stcs[tag_stc_Ti_tgt_single].format(Ti=self.Ti_tgt_low)
        elif self.Ti_tgt_low is None and self.Ti_tgt_high is not None:
            stc_target_Ti = lang_dict_stcs[tag_stc_Ti_tgt_single].format(Ti=self.Ti_tgt_high)
        elif self.Ti_tgt_low == self.Ti_tgt_high:
            stc_target_Ti = lang_dict_stcs[tag_stc_Ti_tgt_single].format(Ti=self.Ti_tgt_high)
        else:
            stc_target_Ti = lang_dict_stcs[tag_stc_Ti_tgt_range].format(Ti_low=self.Ti_tgt_low , Ti_high=self.Ti_tgt_high)
        
        stc_concat_Ti_ranges:str = None
        if stc_spec_Ti is None and stc_target_Ti is None:
            pass
        elif stc_spec_Ti is not None and stc_target_Ti is None:
            stc_concat_Ti_ranges = stc_spec_Ti
        elif stc_spec_Ti is None and stc_target_Ti is not None:
            stc_concat_Ti_ranges = stc_target_Ti
        else:
            stc_concat_Ti_ranges = stc_spec_Ti+" ("+stc_target_Ti+")"

        self.flowsheet.put_line(time = lang_dict_cmn[tag_flow_cmn_rec_time],
                                method=lang_dict_parts_flow[tag_part_flow_instr_init_temp_ctrl],
                                content=sentence_sp_Ti,
                                record=lang_dict_parts_flow[tag_part_flow_check_config],
                                operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
        if stc_concat_Ti_ranges is None:
            self.flowsheet.put_line(record=lang_dict_parts_flow[tag_part_flow_rec_Ti_ini])
        else:
            self.flowsheet.put_line(content=stc_concat_Ti_ranges,
                                    record=lang_dict_parts_flow[tag_part_flow_rec_Ti_ini])
        self.flowsheet.linefeed()

    def get_detail_header(self) -> list[str]:
        return list_hedr

    def get_detail_option_menu(self) -> Optional[dict[str, list[str]]]:
        return dict_opt
    
    def output_unit_operation(self):
        uo_title: str = None
        if self.endpoint_check or self.ctrl_mode == opt_mode_prog:
            uo_title = lang_dict_parts_flow[tag_part_flow_title_compl_tempr_ctrl]
        else:
            uo_title = lang_dict_parts_flow[tag_part_flow_title_tempr_config]
        self.flowsheet.header_organizer(op_nr=self.operation_seq, title=uo_title)
        if not (self.pre_comment == None or self.pre_comment == ''):
            self.flowsheet.put_body_comments(self.pre_comment)
            self.flowsheet.linefeed()        

        #<Operation-specific processes here>
        if self.ctrl_mode == opt_mode_TiTj:
            self.__put_TiTj_mode()
        elif self.ctrl_mode == opt_mode_Tj:
            self.__put_Tj_mode()
        elif self.ctrl_mode == opt_mode_prog:
            self.__put_programme_mode()
        elif self.ctrl_mode == opt_mode_Ti:
            self.__put_Ti_mode()

        if self.endpoint_check:
            self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                    method=lang_dict_parts_flow[tag_part_flow_instr_compl_temp_ctrl],
                                    content=lang_dict_parts_flow[tag_part_flow_instr_check_Ti_in_range],
                                    record=lang_dict_parts_flow[tag_part_flow_check_endpoint],
                                    operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
            if self.time_unit_prog is not None:
                self.flowsheet.put_line(record=lang_dict_stcs[tag_stc_duration].format(time_unit=lang_dict_cmn[self.time_unit_prog]))
            else:
                self.flowsheet.put_line(record=lang_dict_stcs[tag_stc_duration].format(time_unit=lang_dict_cmn[opt_time_unit_minute]))
            self.flowsheet.put_line(record=lang_dict_parts_flow[tag_part_flow_rec_Ti_end])
            self.flowsheet.linefeed()
                        
        if not (self.post_comment == None or self.post_comment == ''):
            self.flowsheet.put_body_comments(self.post_comment)
            self.flowsheet.linefeed()