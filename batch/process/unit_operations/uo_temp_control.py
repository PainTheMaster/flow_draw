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

#########################################################
# UO-specific options, list, header_item: list dictionry thereof (for data input and internalsignaling)
#########################################################

            ##### header items for detail worksheet######

hedr_mode:str = "Control_Mode"
"""Detail heder item: temperature control mode (e.g. Ti, Ti/Tj, amping)"""
hedr_Ti_sp:str = "Ti_set_point(degC)"
"""Detail heder item: Ti set point for Ti, Ti/Tj mode"""
hedr_Ti_limit_low:str = "Ti_limit_low(degC)"
"""Detail heder item: Ti lower limit designaetd by the process owner."""
hedr_Ti_limit_high:str = "Ti_limit_high(degC)"
"""Detail heder item: Ti upper limit designated by the process owner."""
hedr_Ti_tgt_low:str = "Ti_tgt_low(degC)"
"""Detail heder item: Ti TARGET lower limit designated by the process owner."""
hedr_Ti_tgt_high:str = "Ti_tgt_high(degC)"
"""Detail heder item: Ti TARGET higher limit designated by the process owner."""

hedr_Tj_sp:str = "Tj_set_point(degC)"
"""Detail heder item: Tj set point for Tj mode"""

hedr_Tj_limit_low:str = "Tj_min(degC)"
"""Detail heder item: Tj lower limit for Tj, Ti/Tj mode."""

hedr_Tj_limit_high:str = "Tj_max(degC)"
"""Detail heder item: Tj higher limit for Tj, Ti/Tj mode"""

#hedr_Ti_prog_sp_end:str = defs.hedr_uo_tempr_ctrl_prog_Ti_sp_end
#hedr_Ti_prog_sp_end:str = defs.hedr_uo_tempr_ctrl_Ti_sp #TODO check if this is needed. Now, programme mode uses just Ti_sp
"""Detail heder item: Ti end target for ramp mode"""

hedr_prog_time_val:str = "Prog_time_value"
"""Detail heder item: Ramp up/down time value"""

hedr_prog_time_unit:str = "Prog_time_unit"
"""Detail heder item: Ramp up/down time unit"""

hedr_endpoint_check:str = "Check_end_point"
"""Detail heder item: need for heating/cooling end point check."""

list_hedr:list[str] = [hedr_mode,
                       hedr_Ti_sp,
                       hedr_Ti_limit_low,
                       hedr_Ti_limit_high,
                       hedr_Ti_tgt_low,
                       hedr_Ti_tgt_high,
                       hedr_Tj_sp,
                       hedr_Tj_limit_low,
                       hedr_Tj_limit_high,
                       hedr_prog_time_val,
                       hedr_prog_time_unit,
                       hedr_endpoint_check]
"""List of header items for unit operation temperature controle"""


        ##### UO-specific option items for the detail input table #######

opt_mode_TiTj:str = "Ti/Tj_control"
"""Option for detail table: temperature control with single point Ti and Tj range"""
opt_mode_Tj:str = "Tj_control"
"""Option for detail table: temperature control on jacket temperature (single point)"""
opt_mode_prog:str = "Programme"
"""Option for detail table: temperature ramping, cooling or heating with time constraint"""
opt_mode_Ti:str = "Ti_control"
"""Option for detail table: temperature control on liquid temperature (single point)"""

list_opt_mode:list[str] = [opt_mode_TiTj,
                           opt_mode_Tj,
                           opt_mode_prog,
                           opt_mode_Ti]
"""List of options corresponding to the header item hedr_mode for the detail input table of unit operation temperature control"""


opt_check_endpoint_yes:str = opt_yes
"""Option for detail table: Need for temperature control endpoint check-box--yes"""
opt_check_endpoint_no:str = opt_no
"""Option for detail table: Need for temperature control endpoint check-box--no"""
list_opt_check_endpoint:list[str] = [opt_check_endpoint_yes,
                                     opt_check_endpoint_no]
"""List options corresponding to the header item hedr_endpoint_check for the detail input table of unit operation temperature control"""


tag_flow_cmn_time_unit_second:str = defs.tag_flow_cmn_time_unit_second
"""Tag for a common flowsheet component for an unit of time: second"""
tag_flow_cmn_time_unit_minute:str = defs.tag_flow_cmn_time_unit_minute
"""Tag for a common flowsheet component for an unit of time: minute"""
tag_flow_cmn_time_unit_hour:str = defs.tag_flow_cmn_time_unit_hour
"""Tag for a common flowsheet component for an unit of time: hour"""
list_opt_time_unit:list[str] = [tag_flow_cmn_time_unit_second,
                                tag_flow_cmn_time_unit_minute,
                                tag_flow_cmn_time_unit_hour]
"""List of options corresponding to the header item hedr_prog_time_unit for the detail input table of unit operation temperature control"""


dict_opt:dict[str, list[str]] = {hedr_mode:list_opt_mode,
                                 hedr_endpoint_check:list_opt_check_endpoint,
                                 hedr_prog_time_unit:list_opt_time_unit}
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
tag_part_flow_title_tempr_config:str = "uo_title_tempr_config"
"""Tag for a flowsheet component: Unit operation title for temperature configuration."""
tag_part_flow_title_compl_tempr_ctrl:str = "uo_title_tempr_compl_control"
"""Tag for a flowsheet component: Unit operation title for complete temperature control."""
tag_part_flow_instr_init_temp_ctrl:str = "instr_init_temp_ctrl"
"""Tag for a flowsheet component: Instruction to activate temperature control."""
tag_part_flow_instr_compl_temp_ctrl:str = "instr_complete_temp_ctrl"
"""Tag for a flowsheet component: Instrction to complete the temperature control."""
tag_part_flow_instr_check_Ti_in_range:str = "instr_check_temp_in_range"
"""Tag for a flowsheet component: Instrction to check if the Ti is in range."""
tag_part_flow_check_config:str = "check_temp_config"
"""Tag for a flowsheet part: check-box for temperature configuration."""
tag_part_flow_check_activate:str = "check_temp_control_activated"
"""Tag for a flowsheet part: check-box for activation of temperature control."""
tag_part_flow_check_endpoint:str = "check_temp_end_point"
"""Tag for a flowsheet part: check-box for temperature end point"""
tag_part_flow_rec_Ti_ini:str = "rec_Ti_ini"
"""Tag for a flowsheet part: recrd field for initial Ti"""
tag_part_flow_rec_Ti_end:str = "rec_Ti_end"
"""Tag for a flowsheet part: recrd field for end Ti"""

dict_jp_part:dict[str, str] = {tag_part_flow_title_tempr_config: "温調開始",
                               tag_part_flow_title_compl_tempr_ctrl: "温調",
                               tag_part_flow_instr_init_temp_ctrl: "温調開始",
                               tag_part_flow_instr_compl_temp_ctrl: "温調完了",
                               tag_part_flow_instr_check_Ti_in_range: "内温管理範囲内確認",
                               tag_part_flow_check_config: "□ 設定値確認",
                               tag_part_flow_check_activate: "□ 温調開始",
                               tag_part_flow_check_endpoint: "□ 温度到達確認",
                               tag_part_flow_rec_Ti_ini: "温調開始時内温_______℃",
                               tag_part_flow_rec_Ti_end: "温調完了時内温_______℃"}

lang_dict_parts_flow:dict[str, str]  = dict_jp_part
"""Japanese language dictionary for flowsheet parts for unit operation temperature control."""


                    #------------- Sentece dictionary ---------------------
tag_stc_Tj_sp:str = "Tj_set_point"
"""Tag for an instruction sentence for temperature control. Tj set point. Includes placeholder{Tj}"""
tag_stc_Ti_Tj_config:str = "Ti_Tj_control"
"""Tag for an instruction sentence for temperature control. Ti/Tj configuration. Includes placeholder{Ti}, {Tj_low}, and {Tj_high}"""
tag_stc_prog_mode:str = "configure_programme_mode"
"""Tag for an instruction sentence for temperature control. Programme mode. Includes placeholder{Ti}, {Tj_low}, and {Tj_high}"""
tag_stc_prog_duration_minimum:str = "minimum_duration_programme_mode"
"""Sentence template for temperature control. Time requirement for programme heating/cooling mode. Includes  placeholders {time_min} and {time_unit}."""
tag_stc_Ti_range:str = "Ti_range"
"""Tag for an instruction sentence for temperature control. Ti range Includes placeholder {Ti_low} and {Ti_high}"""
tag_stc_prog_terminal_Ti_range:str = "Programme_mode_terminal_Ti_range"
"""Tag for an instruction sentence for temperature control. Programme mode terminal Ti range. Includes placeholder {Ti_low} and {Ti_high}"""
tag_stc_Ti_limit_high_only:str = "Ti_upper_limit_only"
"""Tag for an instruction sentence for temperature control. Ti upper limit only, includes placeholder {Ti_high}"""
tag_stc_Ti_limit_low_only:str = "Ti_lower_limit_only"
"""Tag for an instruction sentence for temperature control. Ti lower limit only, includes placeholder {Ti_low}"""
tag_stc_Ti_tgt_range:str = "Ti_tgt_range"
"""Tag for an instruction sentence for temperature control. Ti target range. Includes placeholder {Ti_low} and {Ti_high}."""
tag_stc_Ti_tgt_single:str = "Ti_tgt_single"
"""Tag for an instruction sentence for temperature control. Ti target single point.  Includes placeholder {Ti}"""
tag_stc_Ti_tgt_low:str = "Ti_tgt_low"
"""Tag for an instruction sentence for temperature control. Ti lower target. Includes placeholder {Ti_low}"""
tag_stc_Ti_tgt_high:str = "Ti_tgt_high"
"""Tag for an instruction sentence for temperature control. Ti higher target. Includes placeholder {Ti_high}"""
tag_stc_Ti_spec_sp_single:str = "Ti_spec_sp"
"""Tag for an instruction sentence for temperature control. Ti specification single point for Ti mode. Includes placeholder {Ti}"""
tag_stc_duration:str = "duration_for_temp_control_(result)"
"""Tag for a record field for temperature control (cooling/heating) duration in a specic time unit. Includes a placeholder {time_unit}"""

dict_jp_stcs: dict[str, str] = {tag_stc_Tj_sp :"外温設定: {Tj} ℃",
                               tag_stc_Ti_Tj_config :"内外温制御: 内温設定{Ti} ℃、外温範囲{Tj_low}～{Tj_high} ℃",
                               tag_stc_prog_mode :"プログラム温調: 内温設定{Ti} ℃、外温範囲{Tj_low}～{Tj_high} ℃",
                               tag_stc_prog_duration_minimum :"温調時間: {time_min} {time_unit}以上",
                               tag_stc_Ti_range :"内温管理幅: {Ti_low}～{Ti_high} ℃",
                               tag_stc_prog_terminal_Ti_range :"終点内温範囲: {Ti_low}～{Ti_high} ℃",
                               tag_stc_Ti_limit_high_only :"内温管理: {Ti_high} ℃以下",
                               tag_stc_Ti_limit_low_only :"内温管理: {Ti_low} ℃以上",
                               tag_stc_Ti_tgt_range :"内温目標幅: {Ti_low}～{Ti_high} ℃",
                               tag_stc_Ti_tgt_low :"内温目標: {Ti_low} ℃ 以上",
                               tag_stc_Ti_tgt_high :"内温目標: {Ti_high} ℃ 以下",
                               tag_stc_Ti_tgt_single :"内温目標値: {Ti} ℃",
                               tag_stc_Ti_spec_sp_single :"内温設定値: {Ti} ℃",
                               tag_stc_duration :"温調時間: _________{time_unit}"}

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
                
        if not pd.isna(first_row[hedr_Tj_limit_high]):
            self.Tj_limit_high = float(first_row[hedr_Tj_limit_high])
                
        if not pd.isna(first_row[hedr_prog_time_val]):
            self.time_val_prog = float(first_row[hedr_prog_time_val])
            if not pd.isna(first_row[hedr_prog_time_unit]):
                self.time_unit_prog = first_row[hedr_prog_time_unit]
            else:
                warnings.warn(message=f"{self.__class__.__name__}: Op. Seq. {self.operation_seq} temperature control: Ramp time for programme heating/cooling defined, but its unit (min, hour, etc) not selected in the form.",
                              category = RuntimeWarning)
                
        self.endpoint_check = (first_row[hedr_endpoint_check] == opt_yes)
        """first_row[hedr_endpoint_check] shall has a value of 'Yes', 'No', NaN or something else. Only 'Yes' is regarded as the affirmative choice."""

    def get_json_schema(caller: trdef.UniversalTrait=None)->Objason:
        common_schema:list[Primitive] = TempControl.json_common()
        mode = Primitive(prim_type='string',
                         key=hedr_mode,
                         description=f'Temperature control mode: This is a mandatory item.'
                                     f'"{opt_mode_TiTj}" mode is most common. A specific set point of the reactor internal temperature (Ti) is given, whereas a specific range of the jacket temperature (Tj) is instructed.'
                                     f'"{opt_mode_Tj}" mode is selected when only the jacket temperature must be maintained at a specific set point. '
                                     f'"{opt_mode_prog}" mode means the reactor Ti approaches a specific set point within a specific time frame, whereas the jacket temperature is maintained within a specific range. Prioritise this mode if time constraint is given. '
                                     f'"{opt_mode_Ti}" mode is selected when only the reactor internal temperature must be maintained at a specific set point. This is less common. This is less reliable mode of control. Try to avoid this mode and prioritise other modes as much as possible. '
                                     f'If no mode is provided in the data source, please select "{opt_mode_TiTj}" to keep the ball rolling.',
                         enum = list_opt_mode)
        Ti_sp = Primitive(prim_type='number',
                          key=hedr_Ti_sp,
                          description=f'Ti set point (instructed by the process owner). '
                          f'Mandatory if "{hedr_mode}" is "{opt_mode_TiTj}", "{opt_mode_prog}", or "{opt_mode_Ti}". '
                          f'Optional and nullable if "{hedr_mode}" is "{opt_mode_Tj}". '
                          'If necessary data is not provided, please put 1000 as a dummy value for the time being.',
                          nullable=True,
                          required=True)
        Ti_limit_low = Primitive(prim_type='number',
                                key=hedr_Ti_limit_low,
                                description=f'Ti lower limit (instructed by the process owner). '
                                f'At leaset one of "{hedr_Ti_limit_low}" or "{hedr_Ti_limit_high}" must be provided if "{hedr_mode}" is "{opt_mode_TiTj}". '
                                f'Both "{hedr_Ti_limit_low}" and "{hedr_Ti_limit_high}" must be provided if "{hedr_mode}" is "{opt_mode_prog}". '
                                f'Optional and nullable if "{hedr_mode}" is "{opt_mode_Tj}" or "{opt_mode_Ti}". '
                                'If the necessary data is not provided, please put 1000 as a dummy value for the time being.',
                                nullable=True,
                                required=True)
        Ti_limit_high = Primitive(prim_type='number',
                                key=hedr_Ti_limit_high,
                                description=f'Ti upper limit (instructed by the process owner). '
                                f'At leaset one of "{hedr_Ti_limit_low}" or "{hedr_Ti_limit_high}" must be provided if "{hedr_mode}" is "{opt_mode_TiTj}". '
                                f'Both "{hedr_Ti_limit_low}" and "{hedr_Ti_limit_high}" must be provided if "{hedr_mode}" is "{opt_mode_prog}". '
                                f'Optional and nullable if "{hedr_mode}" is "{opt_mode_Tj}" or "{opt_mode_Ti}". '
                                'If the necessary data is not provided, please put 1000 as a dummy value for the time being.',
                                nullable=True,
                                required=True)
        Ti_tgt_low = Primitive(prim_type='number',
                              key=hedr_Ti_tgt_low,
                              description='Lower end of Ti target range (instructed by the process woner). Nullable, if no data is provided',
                              nullable=True,
                              required=True)
        Ti_tgt_high = Primitive(prim_type='number',
                               key=hedr_Ti_tgt_high,
                               description='Upper end of Ti target range (instructed by the process woner). Nullable, if no data is provided',
                               nullable=True,
                               required=True)
        Tj_sp = Primitive(prim_type='number',
                          key=hedr_Tj_sp,
                          description=f'Tj set point for Tj control mode. Mandatory if "{hedr_mode}" is "{opt_mode_Tj}". Nullable otherwise.',
                          nullable=True,
                          required=True)
        Tj_limit_low = Primitive(prim_type='number',
                                 key=hedr_Tj_limit_low,
                                 description=f'Lower limit of the jacket temperature (instructed by the process owner). '
                                             f'Mandatory if "{hedr_mode}" is "{opt_mode_TiTj}" or "{opt_mode_prog}". '
                                             f'Optional and nullable otherwise.',
                                 nullable=True,
                                 required=True)
        Tj_limit_high = Primitive(prim_type='number',
                                  key=hedr_Tj_limit_high,
                                  description=f'Upper limit of the jacket temperature (instructed by the process owner). '
                                              f'Mandatory if "{hedr_mode}" is "{opt_mode_TiTj}" or "{opt_mode_prog}". '
                                              f'Optional and nullable otherwise.',
                                  nullable=True,
                                  required=True)
        prog_time_val = Primitive(prim_type='number',
                                  key=hedr_prog_time_val,
                                  description=f'Ramp time for programme heating/cooling mode. Mandatory if "{hedr_mode}" is "{opt_mode_prog}". '
                                              f'Optional and nullable otherwise.',
                                  nullable=True,
                                  required=True)
        prog_time_unit = Primitive(prim_type='string',
                                   key=hedr_prog_time_unit,
                                   description=f'Time unit for programme heating/cooling mode. Mandatory if "{hedr_mode}" is "{opt_mode_prog}". '
                                               f'Optional and nullable otherwise.',
                                   enum=list_opt_time_unit,
                                   nullable=True,
                                   required=True)
        endpoint_check = Primitive(prim_type='string',
                                   key=hedr_endpoint_check,
                                   description=f'Need for temperature control end point check. '
                                               f'Optional. Please select "{opt_check_endpoint_yes}" or "{opt_check_endpoint_no}" if apparent on the data source.',
                                   enum=list_opt_check_endpoint,
                                   nullable=True,
                                   required=True)
        obj_schema = Objason(key=TempControl.uo_tag,
                             description=f'Temperature control unit operation.',
                             props = common_schema+[mode,
                                                    Ti_sp,
                                                    Ti_limit_low,
                                                    Ti_limit_high,
                                                    Ti_tgt_low,
                                                    Ti_tgt_high,
                                                    Tj_sp,
                                                    Tj_limit_low,
                                                    Tj_limit_high,
                                                    prog_time_val,
                                                    prog_time_unit,
                                                    endpoint_check],
                            )
        return obj_schema

    def load_from_json_dict(self, json_dict: dict[str, any]):
        super().load_from_json_dict(json_dict)
        self.ctrl_mode = json_dict.get(hedr_mode, None)
        self.Ti_sp = json_dict.get(hedr_Ti_sp, None)
        self.Ti_limit_low = json_dict.get(hedr_Ti_limit_low, None)
        self.Ti_limit_high = json_dict.get(hedr_Ti_limit_high, None)
        self.Ti_tgt_low = json_dict.get(hedr_Ti_tgt_low, None)
        self.Ti_tgt_high = json_dict.get(hedr_Ti_tgt_high, None)
        self.Tj_sp = json_dict.get(hedr_Tj_sp, None)
        self.Tj_limit_low = json_dict.get(hedr_Tj_limit_low, None)
        self.Tj_limit_high = json_dict.get(hedr_Tj_limit_high, None)
        self.time_val_prog = json_dict.get(hedr_prog_time_val, None)
        self.time_unit_prog = json_dict.get(hedr_prog_time_unit, None)
        self.endpoint_check = (json_dict.get(hedr_endpoint_check, opt_no)== opt_yes)

    def __put_TiTj_mode(self):
        stc_spec:str = None
        if self.Ti_limit_low is None and self.Ti_limit_high is None:
            raise ValueError(f"{self.__class__.__name__}: Op. Seq. {self.operation_seq} Ti limit not specified in the input form for Ti/Tj control mode.")
        elif self.Ti_limit_low is not None and self.Ti_limit_high is None:
            stc_spec = lang_dict_stcs[tag_stc_Ti_limit_low_only].format(Ti_low=self.Ti_limit_low)
        elif self.Ti_limit_low is None and self.Ti_limit_high is not None:
            stc_spec = lang_dict_stcs[tag_stc_Ti_limit_high_only].format(Ti_high=self.Ti_limit_high)
        # Ti_limit_low == Ti_limit_high is not realistic.
        else:
            stc_spec = lang_dict_stcs[tag_stc_Ti_range].format(Ti_low=self.Ti_limit_low, Ti_high=self.Ti_limit_high)

        stc_target:str = None        
        if self.Ti_tgt_low is None and self.Ti_tgt_high is None:
            pass
        elif self.Ti_tgt_low is not None and self.Ti_tgt_high is None:
            stc_target = lang_dict_stcs[tag_stc_Ti_tgt_low].format(Ti_low=self.Ti_tgt_low)
        elif self.Ti_tgt_low is None and self.Ti_tgt_high is not None:
            stc_target = lang_dict_stcs[tag_stc_Ti_tgt_high].format(Ti_high=self.Ti_tgt_high)
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
            stc_spec_Ti = lang_dict_stcs[tag_stc_Ti_limit_low_only].format(Ti_low=self.Ti_limit_low)
        elif self.Ti_limit_low is None and self.Ti_limit_high is not None:
            stc_spec_Ti = lang_dict_stcs[tag_stc_Ti_limit_high_only].format(Ti_high=self.Ti_limit_high)
        # Ti_limit_low == Ti_limit_high is not realistic.
        else:
            stc_spec_Ti = lang_dict_stcs[tag_stc_Ti_range].format(Ti_low=self.Ti_limit_low, Ti_high=self.Ti_limit_high)

        stc_target_Ti:str = None        
        if self.Ti_tgt_low is None and self.Ti_tgt_high is None:
            pass
        elif self.Ti_tgt_low is not None and self.Ti_tgt_high is None:
            stc_target_Ti = lang_dict_stcs[tag_stc_Ti_tgt_low].format(Ti_low=self.Ti_tgt_low)
        elif self.Ti_tgt_low is None and self.Ti_tgt_high is not None:
            stc_target_Ti = lang_dict_stcs[tag_stc_Ti_tgt_high].format(Ti_high=self.Ti_tgt_high)
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
            instr_Ti_range = lang_dict_stcs[tag_stc_prog_terminal_Ti_range].format(Ti_low=self.Ti_limit_low, Ti_high=self.Ti_limit_high)

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
        self.flowsheet.linefeed()


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
            stc_spec_Ti = lang_dict_stcs[tag_stc_Ti_limit_low_only].format(Ti_low=self.Ti_limit_low)
        elif self.Ti_limit_low is None and self.Ti_limit_high is not None:
            stc_spec_Ti = lang_dict_stcs[tag_stc_Ti_limit_high_only].format(Ti_high=self.Ti_limit_high)
        else:
            stc_spec_Ti = lang_dict_stcs[tag_stc_Ti_range].format(Ti_low=self.Ti_limit_low, Ti_high=self.Ti_limit_high)

        stc_target_Ti:str = None        
        if self.Ti_tgt_low is None and self.Ti_tgt_high is None:
            pass
        elif self.Ti_tgt_low is not None and self.Ti_tgt_high is None:
            stc_target_Ti = lang_dict_stcs[tag_stc_Ti_tgt_low].format(Ti_low=self.Ti_tgt_low)
        elif self.Ti_tgt_low is None and self.Ti_tgt_high is not None:
            stc_target_Ti = lang_dict_stcs[tag_stc_Ti_tgt_high].format(Ti_high=self.Ti_tgt_high)
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