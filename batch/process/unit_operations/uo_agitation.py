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
from flow_draw.trait_def import trait_def as trdef
from flow_draw.data_io import json_io
from flow_draw.data_io.json_io import JsonEntity, Array, Objason, Primitive



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
list

#########################################################
# UO-specific hader items and list thereof
#########################################################
#hedr_<something> = defs.hedr_<unit operation>_<specification item>
#list_hedr = defs.list_hedr_<list of header items for the uo>
#dict_dtil_drpdwn = defs.dict_opt_<unit operation>
hedr_spec_agit = "Specification"
"""header item for the unit operation Agitation, the way the rotation rate is specified: specific rpm, guidance rpm, or discretion"""
hedr_rpm = "Rotation_(rpm)"
"""header item for the unit operation Agitation, specific rotation rate"""
hedr_Ti_min = "Ti_min_(deg-C)"
"""header item for the unit operation Agitation, specific Ti_min during agitation, optional"""
hedr_Ti_max = "Ti_max_(deg-C)"
"""header item for the unit operation Agitation, specific Ti_max during agitation, optional"""
hedr_time_min = "Minimum_time"
"""header item for the unit operation Agitation, minimum agitation time, optional"""
hedr_time_max = "Maximum_time"
"""header item for the unit operation Agitation, maximum agitation time, optional"""
hedr_time_unit = "Time_unit"
"""header item for the unit operation Agitation, second, minute, hour"""
hedr_dissolution_check = "Dissolution_check"
"""header item for the unit operation Agitation, need for dissolution check. bool"""
list_hedr = [hedr_spec_agit,
            hedr_rpm,
            hedr_Ti_min,
            hedr_Ti_max,
            hedr_time_min,
            hedr_time_max,
            hedr_time_unit,
            hedr_dissolution_check]
"""List of uo-specific heder items for the unit operation Agitation"""


        ##### UO-specific option items for the detail input table #######
opt_spec_specif = "Specific RPM"
"""option for the header item 'spec'. Specifi RPM is provided by the user."""
opt_spec_guide = "Guidance RPM"
"""option for the header item 'spec'. A guidance RPM is provided by the user."""
opt_spec_arbitrary = "arbitrary"
"""option for the header item 'spec'. Agitation rate is adjuested on the shop floor at the operator's discretion."""

list_opt_spec:list[str]=[opt_spec_specif,
                        opt_spec_guide,
                        opt_spec_arbitrary]
"""List of options for the agitation specification"""

list_opt_uo_agitation_time_unit = defs.list_time_unit
"""List of options for the header item agitation_time_unit"""

list_opt_uo_agitation_dissolution_check = defs.list_yesno
"""List of options for the header item agitation_dissolution_check"""


dict_opt = {hedr_spec_agit : list_opt_spec,
            hedr_time_unit : list_opt_uo_agitation_time_unit,
            hedr_dissolution_check : list_opt_uo_agitation_dissolution_check}
"""Dictionary of headear items and """



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

tag_part_flow_title_disslnck = "agit dissolution check"
"""Tag for a flowsheet component for uo_agitation: title for combined agitation and dissoltion check operation"""
part_flow_title_disslnck_jp = "攪拌・溶解確認"
"""A flowsheet component for uo_agitation: title for combined agitation and dissoltion check operation"""

tag_part_flow_instr_rpm_arbitrary = "rpm_arbitrary"
"""Tag for a flowsheet component for uo_agitation: instruction for totally arbitrary agitation rate"""
part_flow_instr_rpm_arbitrary_jp = "回転数: 現場調整"
"""A flowsheet component for uo_agitation: instruction for totally arbitrary agitation rate"""

tag_part_flow_rec_rpm_act = "rpm_record_act"
"""Tag for a flowsheet component for uo_agitation: record field for agitation rate"""
part_flow_rec_rpm_act_jp= "回転数:_________rpm"
"""A flowsheet component for uo_agitation: record field for agitation rate"""

tag_part_flow_rec_chk_agit_ini = "agit ini"
"""Tag for a flowsheet component for uo_agitation: check box for agitation initiation"""
part_flow_rec_chk_agit_ini_jp = "□ 攪拌開始"
"""A flowsheet component for uo_agitation: check box for agitation initiation"""

tag_part_flow_rec_Tj_ini = "rec Tj ini"
"""Tag for a flowsheet component for uo_agitation: recording field for initial Tj"""
part_flow_rec_Tj_ini_jp = "開始時外温:_________℃"
"""A flowsheet component for uo_agitation: recording field for initial Tj"""

tag_part_flow_rec_Ti_ini = "rec Ti ini"
"""Tag for a flowsheet component for uo_agitation: recording field for initial Ti"""
part_flow_rec_Ti_ini_jp = "開始時内温:_________℃"
"""A flowsheet component for uo_agitation: recording field for initial Ti"""

tag_part_flow_instr_dissoln_check_visual = "instruction dissolution check by visual"
"""Tag for a flowsheet component for uo_agitation: instruction for dissolution chec by visual"""
part_flow_instr_dissoln_check_visual_jp = "溶解確認:目視"
"""A flowsheet component for uo_agitation: instruction for dissolution chec by visual"""

tag_part_flow_rec_chk_dissoln = "check box dissolution"
"""Tag for a flowsheet component for uo_agitation: check box for dissolution"""
part_flow_rec_chk_dissoln_jp = "□ 溶解確認"
"""A flowsheet component for uo_agitation: check box for dissolution"""

tag_part_flow_rec_final_Tj = "rec Tj agitation end"
"""Tag for a flowsheet component for uo_agitation: recording field for final Tj"""
part_flow_rec_final_Tj_jp = "攪拌終了時外温:_________℃"
"""A flowsheet component for uo_agitation: recording field for final Tj"""

tag_part_flow_rec_final_Ti = "rec Ti agitation end"
"""Tag for a flowsheet component for uo_agitation: recording field for final Ti"""
part_flow_rec_final_Ti_jp = "攪拌終了時内温:_________℃"
"""A flowsheet component for uo_agitation: recording field for final Ti"""

tag_part_flow_rec_dissoln_Tj = "rec Tj at complete dissolution"
"""Tag for a flowsheet component for uo_agitation: recording field for Tj at the time of dissolution"""
part_flow_rec_dissoln_Tj_jp = "溶解確認時外温:_________℃"
"""A flowsheet component for uo_agitation: recording field for Tj at the time of dissolution"""

tag_part_flow_rec_dissoln_Ti = "rec Ti at complete dissolution"
"""Tag for a flowsheet component for uo_agitation: recording field for Ti at the time of dissolution"""
part_flow_rec_dissoln_Ti_jp = "溶解確認時内温:_________℃"
"""A flowsheet component for uo_agitation: recording field for Ti at the time of dissolution"""

tag_part_flow_rec_chk_agit_compl = "agit completed"
"""Tag for a flowsheet component for uo_agitation: check box for agitation completion"""
part_flow_rec_chk_agit_compl_jp = "□ 攪拌完了"
"""A flowsheet component for uo_agitation: check box for agitation completion"""

dict_part_flow_jp = {tag_part_flow_title_disslnck : part_flow_title_disslnck_jp,
                    tag_part_flow_instr_rpm_arbitrary : part_flow_instr_rpm_arbitrary_jp,
                    tag_part_flow_rec_rpm_act : part_flow_rec_rpm_act_jp,
                    tag_part_flow_rec_chk_agit_ini : part_flow_rec_chk_agit_ini_jp,
                    tag_part_flow_rec_Tj_ini : part_flow_rec_Tj_ini_jp,
                    tag_part_flow_rec_Ti_ini : part_flow_rec_Ti_ini_jp,
                    tag_part_flow_instr_dissoln_check_visual : part_flow_instr_dissoln_check_visual_jp,
                    tag_part_flow_rec_chk_dissoln : part_flow_rec_chk_dissoln_jp,
                    tag_part_flow_rec_final_Tj : part_flow_rec_final_Tj_jp,
                    tag_part_flow_rec_final_Ti : part_flow_rec_final_Ti_jp,
                    tag_part_flow_rec_dissoln_Tj : part_flow_rec_dissoln_Tj_jp,
                    tag_part_flow_rec_dissoln_Ti : part_flow_rec_dissoln_Ti_jp,
                    tag_part_flow_rec_chk_agit_compl : part_flow_rec_chk_agit_compl_jp}

dict_part_flow = dict_part_flow_jp
"""Japanese lanugae dictionary for flowsheet part for the unit operation Agitation"""



tag_stc_flow_rpm_spec = "component_tag_rpm_spec"
"""Tag for a sentence for the unit operation Agitation: instruction for agitation at an specified agitation rate, includes a placeholder {rpm}"""
stc_flow_rpm_spec_jp = "攪拌速度:{rpm}rpm"
"""Sentence for the unit operation Agitation: instruction for agitation at an specified agitation rate, includes a placeholder {rpm}"""

tag_stc_flow_rpm_guidance = "component_tag_rpm_guidance"
"""Tag for a sentence for the unit operation Agitation: instruction for agitation with a guideline rate, includes a placeholder {rpm}"""
stc_flow_rpm_guidance_jp = "攪拌速度:現場調整(目安{rpm}rpm)"
"""Sentence for the unit operation Agitation: instruction for agitation with a guideline rate, includes a placeholder {rpm}"""

tag_stc_flow_Ti_range = "agitation Ti range"
"""Tag for a sentence for the unit operation Agitation: Instrction on temperature range. Includes placeholders {Ti_min} and {Ti_max}"""
stc_flow_temp_range_jp = "内温範囲:{Ti_min}～{Ti_max}℃"
"""Sentence for the unit operation Agitation: Instrction on temperature range. Includes placeholders {Ti_min} and {Ti_max}"""

tag_stc_flow_Ti_min = "agigation Ti minimum" 
"""Tag for a sentence for the unit operation Agitation: Instruction on minimum temperature. Includes placeholder {Ti_min}"""
stc_flow_temmp_min_jp = "内温{Ti_min}以上"
"""Sentence for the unit operation Agitation: Instruction on minimum temperature. Includes placeholder {Ti_min}"""

tag_stc_flow_Ti_max = "agitation Ti max"
"""Tag for a sentence for the unit operation Agitation: Instruction on maximum temperature. Includes placeholder {Ti_max}"""
stc_flow_temp_max_jp = "内温{Ti_min}以下"
"""Sentence for the unit operation Agitation: """

tag_stc_flow_time_range = "agitation time range"
"""Tag for a sentence for the unit operation Agitation: Instruction on agitation time range. Includes placeholders {time_min}, {time_max} , and {time_unit}"""
stc_flow_time_range_jp = "攪拌継続:{time_min}～{time_max} {time_unit}"
"""Sentence for the unit operation Agitation: Instruction on agitation time range. Includes placeholders {time_min}, {time_max}, and {time_unit}"""

tag_stc_flow_time_min = "agitation minimum time"
"""Tag for a sentence for the unit operation Agitation: Instruction on minimum agitation time. Includes placeholders {time_min} and {time_unit}"""
stc_flow_time_min_jp = "攪拌継続:{time_min} {time_unit}以上"
"""Sentence for the unit operation Agitation: Instruction on minimum agitation time. Includes {time_min} and {time_unit}"""

tag_stc_flow_time_max = "agitation maximum time"
"""Tag for a sentence for the unit operation Agitation: Instruction on maximum agitation time. Includes {time_max} and {time_unit}"""
stc_flow_time_max_jp = "攪拌継続:{time_max} {time_unit}以下"
"""Sentence for the unit operation Agitation:  Instruction on maximum agitation time. Includes {time_max} and {time_unit}"""

tag_stc_flow_time_single_point = "agitation time single point"
"""Tag for a sentence for the unit operation Agitation: Instruction on agitation time (single point). Includes a placeholder {time} and {time_unit}"""
stc_flow_time_single_point_jp = "攪拌時間:{time} {time_unit}"
"""Sentence for the unit operation Agitation:  Instruction on maximum agitation time. Includes a placeholder {time} and {time_unit}"""

tag_stc_flow_rec_duration = "record agitation duration"
"""Tag for a sentence for the unit operation Agitation: Record field for agitation duration, includes a placeholder {time_unit}"""
stc_flow_rec_duration_jp = "攪拌時間:_________{time_unit}"
"""Sentence for the unit operation Agitation: Record field for agitation duration, includes a placeholder {time_unit}"""

dict_stcs_jp = {tag_stc_flow_rpm_spec : stc_flow_rpm_spec_jp,
                tag_stc_flow_rpm_guidance : stc_flow_rpm_guidance_jp,
                tag_stc_flow_Ti_range : stc_flow_temp_range_jp,
                tag_stc_flow_Ti_min : stc_flow_temmp_min_jp,
                tag_stc_flow_Ti_max : stc_flow_temp_max_jp,
                tag_stc_flow_time_range : stc_flow_time_range_jp,
                tag_stc_flow_time_min : stc_flow_time_min_jp,
                tag_stc_flow_time_max : stc_flow_time_max_jp,
                tag_stc_flow_time_single_point : stc_flow_time_single_point_jp,
                tag_stc_flow_rec_duration : stc_flow_rec_duration_jp}


dict_stcs = dict_stcs_jp
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
        super().__init__(caller=caller, flowsheet=flowsheet, operation_seq=operation_seq, num_subitems=1, edit_comment=edit_comment)
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
                warnings.warn(
                    message=f"{self.__class__.__name__}: \"{hedr_time_unit}\" not selected in the detail input worksheet "
                                     f"for Op. Seq. {self.operation_seq} although minimum and/or maximum agitation time has been provided "
                                     f"in the worksheet. Time unit of \"min\" is used to keep the ball rolling.",
                    category=RuntimeWarning)

                # raise RuntimeWarning(f"{self.__class__.__name__}: \"{hedr_time_unit}\" not selected in the detail input worksheet"\
                #                      f"for Op. Seq. {self.operation_seq} although minimum and/or maximum agitation time has benn provided"\
                #                      f"in the worksheet. Time unit of \"min\" is used to keep the ball rolling.")
        
        if first_row[hedr_dissolution_check] == opt_yes:
            self.dissolution_check = True


    def get_detail_header(self) -> list[str]:
        return list_hedr

    def get_detail_option_menu(self) -> Optional[dict[str, list[str]]]:
        return dict_opt
    

    def get_json_schema(caller:trdef.UniversalTrait = None)->json_io.Objason:
        # list_cmn = Agitation.json_common(arg_name_uo=Agitation.uo_tag)
        list_cmn = Agitation.json_common()
        spec_agit = Primitive(prim_type='string',
                            key=hedr_spec_agit,
                            enum=dict_opt[hedr_spec_agit],
                            description="The way the rotation rate is specified: specific rpm, guidance rpm, or arbitrary",
                            required=True)
        rpm = Primitive(prim_type='number',
                        key=hedr_rpm,
                        description=f'Rotation (rpm) of agitation. If "{hedr_spec_agit}"=="{opt_spec_arbitrary}", this property is not required.',
                        required=False)
        ti_min = Primitive(prim_type='number',
                           key=hedr_Ti_min,
                           description=f'Lower limit of reactor inner temperature (Ti) during agitation. Optional. Ti_min should not exceed Ti_max. '\
                            f'If only a single point is specified on the source, please make this value equal to "{hedr_Ti_max}"',
                           required=False)
        
        ti_max = Primitive(prim_type='number',
                           key=hedr_Ti_max,
                           description=f'Upper limit of reactor inner temperature (Ti) during agitation. Optional. Ti_max should not be lower than Ti_min. '\
                           f'If only a single point is specified on the source, please make this value equal to "{hedr_Ti_min}"',
                           required=False)
        time_min = Primitive(prim_type='number',
                            key=hedr_time_min,
                            description="Minimum required time for agitation, optional",
                            required=False)
        time_max = Primitive(prim_type='number',
                            key=hedr_time_max,
                            description="Upper limit of agitation time, optional",
                            required=False)
        time_unit = Primitive(prim_type='string',
                              key=hedr_time_unit,
                              enum=list_opt_uo_agitation_time_unit,
                              description=f'Time unit to specify the lower/upper limits of the agitation time: second, minute, hour. If either of {hedr_time_min} or {hedr_time_max} is given, this is essential.',
                              required=False)
        dissolution_check = Primitive(prim_type='string',
                                      key=hedr_dissolution_check,
                                      enum=list_opt_uo_agitation_dissolution_check,
                                      description=f'Need for dissolution check. In some cases, dissolution of a solid material in the solvent has to be checked. Please make a choice from "{opt_yes}"/"{opt_no}".',
                                      required=True)
        json_agitation = Objason(#key=defs.tag_uo_agitation,
                                 key=Agitation.uo_tag,
                                 props=list_cmn+[spec_agit, ti_min, ti_max, time_min, time_max, dissolution_check],
                                 description='This is the object to store information for an unit operation of "agitation" extracted from the source.'\
                                    '"agitation" is an unit operation where a solution/reaction mixture/slurry is agitated.',
                                 required=False)
        json_agitation.if_then_else(prop = spec_agit.key,
                                    val_if= [opt_spec_specif, opt_spec_guide],
                                    props_then=[rpm])
        json_agitation.if_then_else(prop=time_min.key,
                                    props_then=[time_unit])
        json_agitation.if_then_else(prop=time_max.key,
                                    props_then=[time_unit])
        return json_agitation
        
        
        
    def load_from_json_dict(self, json_dict: dict[str, any]):
        self.operation_seq=json_dict[defs.hedr_cmn_io_dtil_seq]
        if defs.hedr_cmn_io_dtil_edt_cmnt in json_dict:
            self.edit_comment = json_dict[defs.hedr_cmn_io_dtil_edt_cmnt]
        if defs.hedr_cmn_io_dtil_precmnt in json_dict:
            self.pre_comment = json_dict[defs.hedr_cmn_io_dtil_precmnt]
        if defs.hedr_cmn_io_dtil_postcmnt in json_dict:
            self.post_comment = json_dict[defs.hedr_cmn_io_dtil_postcmnt]
        self.spec_agit = json_dict[hedr_spec_agit]
        if hedr_rpm in json_dict:
            self.rpm = json_dict[hedr_rpm]
        if hedr_Ti_min in json_dict:
            self.Ti_min = json_dict[hedr_Ti_min]
        if hedr_Ti_max in json_dict:
            self.Ti_max = json_dict[hedr_Ti_max]
        if hedr_time_min in json_dict:
            self.time_min = json_dict[hedr_time_min]
        if hedr_time_max in json_dict:
            self.time_max = json_dict[hedr_time_max]
        if hedr_time_unit in json_dict:
            self.time_unit = json_dict[hedr_time_unit]
        
        if json_dict[hedr_dissolution_check] == opt_yes:
            self.dissolution_check = True
        else:
            self.dissolution_check = False
        #TODO please continue
        


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
                stc_time_ctrl = dict_stcs[tag_stc_flow_time_range].format(time_min=self.time_min, time_max=self.time_max, time_unit=lang_dict_cmn[self.time_unit])
            else:
                stc_time_ctrl = dict_stcs[tag_stc_flow_time_single_point].format(time=self.time_min, time_unit=lang_dict_cmn[self.time_unit])
        elif self.time_min is not None:
            stc_time_ctrl = dict_stcs[tag_stc_flow_time_min].format(time_min=self.time_min, time_unit=lang_dict_cmn[self.time_unit])
        elif self.time_max is not None:
            stc_time_ctrl = dict_stcs[tag_stc_flow_time_max].format(time_max=self.time_max, time_unit=lang_dict_cmn[self.time_unit])
        else:
            warnings.warn(message=f"{__class__.__name__}: Wrong call for __put_time_control() in Op. Seq. {self.operation_seq}.",
                          category=RuntimeWarning)
            #raise RuntimeWarning(f"{__class__.__name__}: Wrong call for __put_time_control() in Op. Seq. {self.operation_seq}.")
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
            warnings.warn(message=f"{__class__.__name__}: Wrong call for __put_temp_control() in Op. Seq. {self.operation_seq}.",
                          category=RuntimeWarning)
            #raise RuntimeWarning(f"{__class__.__name__}: Wrong call for __put_temp_control() in Op. Seq. {self.operation_seq}.")

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
                self.flowsheet.put_line(record=dict_stcs[tag_stc_flow_rec_duration].format(time_unit=lang_dict_cmn[self.time_unit]))
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
                self.flowsheet.put_line(record=dict_stcs[tag_stc_flow_rec_duration].format(time_unit=lang_dict_cmn[self.time_unit]))
        else:
            self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                    record=dict_part_flow[tag_part_flow_rec_chk_agit_compl],
                                    operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
            if self.time_min is not None or self.time_max is not None:
                self.flowsheet.put_line(record=dict_stcs[tag_stc_flow_rec_duration].format(time_unit=lang_dict_cmn[self.time_unit]))


    
