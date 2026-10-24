#########################################################
# imports
#########################################################
import pandas as pd
import flow_draw.definitions as defs
import flow_draw.data_io.flowsheet as fsht

from typing import Optional, Any
from flow_draw.batch.process.unit_operations import unit_operation as uo
from flow_draw.data_io import process_io as procio
from flow_draw.materials import materials as mats
from flow_draw.trait_def import trait_def as trdef
from flow_draw.trait_def.trait_def import GetMats, GetInputs, MaterialReceiver
import flow_draw.batch.process.unit_operations.material_input as matin
from flow_draw.batch.process.unit_operations.material_input import Input
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
hedr_equipment:str = 'Equipment'
"""Header item for the equipment used in the crystallization washing unit operation."""
hedr_mode_washing = 'Crystal_Washing_Mode'
"""Header item for the crystal washing mode."""
hedr_duration_washing_minutes:str = 'Washing_Duration_minutes'
"""Header item for the duration of the crystal washing."""
hedr_agitation_rpm:str = 'Agitation_rpm'
"""Header item for the agitation speed in revolutions per minute."""
key_arr_solvent_json:str = 'Solvent_Input_Array'
"""Key for the material input JSON object in the crystallization washing unit operation."""


list_hedr = [hedr_equipment,
             hedr_mode_washing,
             hedr_duration_washing_minutes,
             hedr_agitation_rpm]


#########################################################
# UO-specific options, list, header_item: list dictionry thereof (for data input and internalsignaling)
#########################################################

opt_washmode_reslurry:str = "mode_reslurry"
"""Option for the crystal washing mode: reslurry."""
opt_washmode_soak:str = "mode_static_soak_washing"
"""Option for the crystal washing mode: static."""
opt_washmode_displacement:str = "mode_static_displacement_washing"
"""Option for the crystal washing mode: plug flow."""
opt_washmode_placeholder:str = "mode_placeholder"

list_opt_mode_washing = [opt_washmode_reslurry, opt_washmode_soak, opt_washmode_displacement, opt_washmode_placeholder]
"""list of menues for hedr_mode_washing"""

dict_opt: dict[str, list[str]]={hedr_mode_washing: list_opt_mode_washing}

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

tag_part_val_equipment_plchldr:str = "tag_placeholder_equipment"
"""The key to a flowsheet part: placeholder for equipment."""
tag_part_val_agit_rate_arbit:str = "tag_opt_agit_rate_arbit"
"""The key to a flowsheet part: arbitrary agitation rate."""
tag_part_val_agit_time_plchldr:str = "tag_placeholder_washing_time"
"""The key to a flowsheet part: placeholder for washing time."""
tag_part_unit_agit_rpm:str = "tag_unit_agit_rpm"
"""The key to a flowsheet part: rpm, an unit of agitation rate."""
tag_part_mthd_reslurry:str = "tag_method_reslurry"
"""The key to a flowsheet part: subtitle for reslurry washing."""
tag_part_mthd_soaking:str = "tag_method_soaking"
"""The key to a flowsheet part: subtitle for soaking."""
tag_part_mthd_displ_wash:str = "tag_method_displ_wash"
"""The key to a flowsheet part: subtitle for displacement washing."""
tag_part_cntnt_instr_obs:str = "tag_content_instr_observation"
"""The key to a flowsheet part: instruction for observation during agitation."""
tag_part_cntnt_instr_init_agit:str = "tag_content_instr_init_agit"
"""The key to a flowsheet part: instruction to start agitation."""
tag_part_cntnt_instr_init_soaking:str = "tag_content_instr_init_soaking"
"""The key to a flowsheet part: instruction to start soaking."""
tag_part_cntnt_instr_init_displwash:str = "tag_content_instr_init_displacement_washing"
"""The key to a flowsheet part: instruction to start displacement washing."""
tag_part_cntnt_instr_end_agit:str = "tag_content_instr_end_agit"
"""The key to a flowsheet part: instruction to stop agitation."""
tag_part_cntnt_instr_end_soaking:str = "tag_content_instr_end_soaking"
"""The key to a flowsheet part: instruction to stop soaking."""
tag_part_cntnt_instr_end_displwash:str = "tag_content_instr_end_displacemet_washing"
"""The key to a flowsheet part: instruction to stop displacement washing."""
tag_part_cntnt_instr_displ_wash:str = 'tag_content_instr_displacementwash'
"""The key to a flowsheet part: instruction to carry out displacement washing."""
tag_part_rec_check_wash_ini:str = "tag_reach_agit_complt"
"""The key to a flowsheet part: record field component. Check box to record the completion of agitation."""
tag_part_rec_rot_rate:str = "tag_rec_agitation_rpm"
"""The key to a flowsheet part: record field for agitation rate"""

tag_stc_cntnt_instr_reslurry:str = "tag_stc_instr_reslurry"
"""The key to a flowsheet sentence template: instruction for reslurry. Includes place holders "{time_value}" and "{time_unit}". """
tag_stc_cntnt_instr_soaking: str = 'tag_stc_instr_soaking'
"""The key to a flowsheet sentence template: instruction for soaking. Includes place holders "{time_value}" and "{time_unit}". """
tag_stc_cntnt_agit_rate:str = "tag_stc_agit_rate"
"""The key to a flowsheet sentence template: instruction for agitation rate. Includes place holders "{rot_value}" and "{rot_unit}". """
tag_stc_rec_agit_duration:str = "tag_stc_agit_duration"
"""The key to a flowsheet sentence template: record field for agitation duration. Includes a place holder "{time_unit}". """
tag_stc_rec_soaking_duration:str = 'tag_stc_soak_duration'
"""The key to a flowsheet sentence template: record field for soaking duration. Includes a place holder "{time_unit}". """
tag_stc_rec_displ_duration:str = 'tag_stc_displwash_duration'
"""The key to a flowsheet sentence template: record field for dislwash duration. Includes a place holder "{time_unit}". """

dict_parts_stcs_jp = {tag_part_val_equipment_plchldr : '<placeholder: 機器>',
                      tag_part_val_agit_rate_arbit: '現場調整',
                      tag_part_val_agit_time_plchldr : '<placeholder: 攪拌時間>',
                      tag_part_unit_agit_rpm: 'rpm',
                      tag_part_mthd_reslurry : '懸濁攪拌',
                      tag_part_mthd_soaking : '浸漬洗浄',
                      tag_part_mthd_displ_wash : 'かけ洗い',                      
                      tag_part_cntnt_instr_obs : 'FD内の状態を確認しながら操作すること',
                      tag_part_cntnt_instr_displ_wash: '洗浄溶媒を供給してかけ洗いする。',
                      tag_part_cntnt_instr_init_agit : '攪拌開始',
                      tag_part_cntnt_instr_init_soaking: '浸漬開始',
                      tag_part_cntnt_instr_init_displwash: 'かけ洗い開始',
                      tag_part_cntnt_instr_end_agit : '攪拌終了',
                      tag_part_cntnt_instr_end_soaking : '浸漬終了',
                      tag_part_cntnt_instr_end_displwash: 'かけ洗い終了',
                      tag_part_rec_check_wash_ini : '□ 洗浄開始',
                      tag_part_rec_rot_rate : '回転数:__________rpm',
                      tag_stc_cntnt_instr_reslurry :'最下端まで攪拌しながら掘り下げ後{time_value}{time_unit}以上攪拌して攪拌翼を最上端まで上げて次ステップに移行する。',
                      tag_stc_cntnt_instr_soaking : 'ケークを{time_value}{time_unit}以上、洗浄溶媒に浸漬して次のステップに移行する。',
                      tag_stc_cntnt_agit_rate : '攪拌数: {rot_value}{rot_unit}',
                      tag_stc_rec_agit_duration : '攪拌時間:__________{time_unit}',
                      tag_stc_rec_soaking_duration: '浸漬時間:__________{time_unit}',
                      tag_stc_rec_displ_duration: 'かけ洗い時間:__________{time_unit}'}

dict_parts_stcs = dict_parts_stcs_jp


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
class CrystWashing(uo.UnitOperation, MaterialReceiver, uo_tag=defs.tag_uo_cryst_wash):
    def __init__(self,
                 caller: GetMats|GetInputs =None,
                 flowsheet:fsht.Flowsheet=None, 
                 operation_seq: int=None,
                 num_subitems: int = None,
                 edit_comment:str=None):
        super().__init__(caller=caller, flowsheet=flowsheet, operation_seq=operation_seq, num_subitems=num_subitems, edit_comment=edit_comment)
        if caller is None:
            raise ValueError(f'{self.__class__.__name__}._init_: "caller: GetMats|GetInputs"is required')
        self.mats_data = caller.get_mats()
        self.equipment:str = None
        self.mode_washing:str = None
        self.duration_washing_minutes:float = None
        self.rpm_agit:float = None
        self.arr_inputs:list[Input] = []



    
    def load_params_from_df(self, df: pd.DataFrame):
        """
        Loads necessary parameters from a DataFrame object.
        The header items must be in line with the definition the class CrystWashing.
        The first row holds the UO-specific parameters as well as the first solvent input.
        Each row, including the first one, corresponds to a solvent input.
        This is the overriding mehtod in the class CrystWashing.
        """
        def __val_or_none(ser: pd.Series, hedr: str):
            val = ser.get(hedr, None)
            if val is None or (not isinstance(val, (list, tuple)) and pd.isna(val)):
                return None
            return val

        first_row = df.iloc[0]
        if not pd.isna(first_row[hedr_precomment]):
            self.pre_comment = first_row[hedr_precomment]
        if not pd.isna(first_row[hedr_postcomment]):
            self.post_comment = first_row[hedr_postcomment]
        self.equipment = __val_or_none(first_row, hedr_equipment)
        if not self.equipment:
            self.equipment = dict_parts_stcs[tag_part_val_equipment_plchldr]
        self.mode_washing = __val_or_none(first_row, hedr_mode_washing)
        self.duration_washing_minutes = __val_or_none(first_row, hedr_duration_washing_minutes)
        self.rpm_agit = __val_or_none(first_row, hedr_agitation_rpm)

        self.arr_inputs.clear()
        for _, subitem in df.iterrows():
            #Rows without a material name are regarded as empty.
            if __val_or_none(subitem, matin.hedr_material_name) is None:
                continue
            new_input = Input(get_mats=self.caller,
                              get_inputs=self.caller,
                              flowsheet=self.flowsheet)
            new_input.load_params_from_series(subitem)
            vessel_train:list[str] = new_input.get_vessel_train()
            if not vessel_train or vessel_train[-1] != self.equipment:
                vessel_train.append(self.equipment)
            self.arr_inputs.append(new_input)



    def get_detail_header(self) -> list[str]:
        """UO-specific items only."""
        return list_hedr

    def get_detail_option_menu(self) -> Optional[dict[str, list[str]]]:
        return dict_opt
    
    @staticmethod
    def get_json_schema(caller: GetMats=None)->Objason:
        common_schema = CrystWashing.json_common()
        equipment = Primitive(prim_type='string',
                        key=hedr_equipment,
                        description='Equipment used for the crystal washing operation. Normally, it is a filter dryer, but please follow the given information source. '
                        'If cannot be specified, please put a placeholder "<placeholder: equipment>"',
                        nullable=True,
                        required=True)
        mode_washing = Primitive(prim_type='string',
                        key=hedr_mode_washing,
                        description='Mode of the crystal washing operation.'
                        f'"{opt_washmode_reslurry}": The mixture of the crystals and the washing solvent is agitated to form a slurry again. The most common mode of crystal wahing. '
                        f'"{opt_washmode_soak}": The crystals are washed without agitation, typically by simply adding the washing solvent and '
                        'soaking the wet cake in it for a certain period of time. '
                        f'"{opt_washmode_displacement}": The washing solvent is supplied to the filtration device where the crystals are retained and pressurized to flow through the crystals. '
                        f'"{opt_washmode_placeholder}": Placeholder for the crystal washing operation mode. If the mode cannot be specified, please select this option.',
                        enum=list_opt_mode_washing,
                        nullable=False,
                        required=True)
        washing_duration_minutes = Primitive(prim_type='number',
                        key=hedr_duration_washing_minutes,
                        description='Duration of the crystal washing operation expressed in minute unit. '
                        f'Nullable if the "{hedr_mode_washing}" is "{opt_washmode_displacement}" or "{opt_washmode_placeholder}". '
                        f'Please put null if the necessary duration cannot be specified from the given data source.',
                        nullable=True,
                        required=True)
        agitation_rpm = Primitive(prim_type='number',
                        key=hedr_agitation_rpm,
                        description='Agitation speed in revolutions per minute during the crystal washing operation. '
                        f'This property is read if "{hedr_mode_washing}"=="{opt_washmode_reslurry}", but nullable. '
                        'In that case, if a specific vale cannot be extracted from the data source, please put null. The user will take a necessary action. '
                        f'If other options are chosen for "{hedr_mode_washing}", this property will be ignored.',
                        nullable=True,
                        required=True)
        input_entry = Input.get_json_schema(caller=caller)
        arr_input = Array(key=key_arr_solvent_json,
                          content=input_entry,
                          description='A list of material input entries for solvents used in incrystal washing operation. '
                          f'Material input can be a part of this unit operations or can be an independed "{defs.tag_uo_charging}" before this step if more appropriate.',
                          required=False)
        obj_uo = Objason(key=CrystWashing.uo_tag,
                         props=common_schema+[equipment, mode_washing, washing_duration_minutes, agitation_rpm, arr_input],
                         description='Crystal washing unit operation. This is typically carried out once or multiple times after the filtration of the recrystallized slurry of the intermediate or API.',
                         required=False,
                         nullable=False)
        return obj_uo


    def load_from_json_dict(self, json_dict: dict[str, Any]):
        super().load_from_json_dict(json_dict)
        self.equipment = json_dict.get(hedr_equipment, None)
        if not self.equipment:
            self.equipment = dict_parts_stcs[tag_part_val_equipment_plchldr]
        self.mode_washing = json_dict.get(hedr_mode_washing, None)
        self.duration_washing_minutes = json_dict.get(hedr_duration_washing_minutes, None)
        self.rpm_agit = json_dict.get(hedr_agitation_rpm, None)

        self.arr_inputs.clear()
        solvents_json = json_dict.get(key_arr_solvent_json, None)
        if solvents_json is None:
            solvents_json = []
        for solvent in solvents_json:
            new_input = Input(get_mats=self.caller,
                              get_inputs=self.caller,
                              flowsheet=self.flowsheet)
            new_input.load_from_json_dict(solvent)
            vessel_train:list[str]=new_input.get_vessel_train()
            if vessel_train is None:
                raise RuntimeError(f'{self.__class__.__name__}.load_from_json_dict(): Vessel train of the new input ({new_input.get_name_this()}) is empty.')
            if not vessel_train or vessel_train[-1] != self.equipment:
                vessel_train.append(self.equipment)
            self.arr_inputs.append(new_input)



    def print_unit_operation(self):

        def print_reslurry():
            time_unit = lang_dict_cmn[tag_flow_cmn_time_unit_minute]
        
            if isinstance(self.duration_washing_minutes, (int, float)) and not isinstance(self.duration_washing_minutes, bool):
                duration = self.duration_washing_minutes
            else:
                duration = dict_parts_stcs[tag_part_val_agit_time_plchldr]
            stc_instr = dict_parts_stcs[tag_stc_cntnt_instr_reslurry].format(time_value=duration, time_unit=time_unit)
            if isinstance(self.rpm_agit, (int, float)) and not isinstance(self.rpm_agit, bool):
                stc_rot = dict_parts_stcs[tag_stc_cntnt_agit_rate].format(rot_value=self.rpm_agit, rot_unit=' '+dict_parts_stcs[tag_part_unit_agit_rpm])
            else:
                stc_rot = dict_parts_stcs[tag_stc_cntnt_agit_rate].format(rot_value=dict_parts_stcs[tag_part_val_agit_rate_arbit], rot_unit='')
            self.flowsheet.put_line(content=stc_instr)
            self.flowsheet.put_line(content=stc_rot,
                                    record=dict_parts_stcs[tag_part_rec_rot_rate])
            self.flowsheet.put_line(content=dict_parts_stcs[tag_part_cntnt_instr_obs])
            self.flowsheet.linefeed()
            self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                    method=dict_parts_stcs[tag_part_mthd_reslurry],
                                    content=dict_parts_stcs[tag_part_cntnt_instr_init_agit],
                                    record=dict_parts_stcs[tag_part_rec_check_wash_ini],
                                    operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
            self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                    content=dict_parts_stcs[tag_part_cntnt_instr_end_agit],
                                    record=dict_parts_stcs[tag_stc_rec_agit_duration].format(time_unit=time_unit),
                                    operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    witness=lang_dict_cmn[tag_flow_cmn_rec_sign])

        def print_soaking():
            time_unit = lang_dict_cmn[tag_flow_cmn_time_unit_minute]
        
            if isinstance(self.duration_washing_minutes, (int, float)) and not isinstance(self.duration_washing_minutes, bool):
                duration = self.duration_washing_minutes
            else:
                duration = dict_parts_stcs[tag_part_val_agit_time_plchldr]
            stc_instr = dict_parts_stcs[tag_stc_cntnt_instr_soaking].format(time_value=duration, time_unit=time_unit)
            self.flowsheet.put_line(content=stc_instr)
            self.flowsheet.put_line(content=dict_parts_stcs[tag_part_cntnt_instr_obs])
            self.flowsheet.linefeed()
            self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                    method=dict_parts_stcs[tag_part_mthd_soaking],
                                    content=dict_parts_stcs[tag_part_cntnt_instr_init_soaking],
                                    record=dict_parts_stcs[tag_part_rec_check_wash_ini],
                                    operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
            self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                    content=dict_parts_stcs[tag_part_cntnt_instr_end_soaking],
                                    record=dict_parts_stcs[tag_stc_rec_soaking_duration].format(time_unit=time_unit),
                                    operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    witness=lang_dict_cmn[tag_flow_cmn_rec_sign])

        def print_diplwash():
            time_unit = lang_dict_cmn[tag_flow_cmn_time_unit_minute]
                    
            self.flowsheet.put_line(content=dict_parts_stcs[tag_part_cntnt_instr_displ_wash])
            self.flowsheet.put_line(content=dict_parts_stcs[tag_part_cntnt_instr_obs])
            self.flowsheet.linefeed()
            self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                    method=dict_parts_stcs[tag_part_mthd_displ_wash],
                                    content=dict_parts_stcs[tag_part_cntnt_instr_init_displwash],
                                    record=dict_parts_stcs[tag_part_rec_check_wash_ini],
                                    operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
            self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                    content=dict_parts_stcs[tag_part_cntnt_instr_end_displwash],
                                    record=dict_parts_stcs[tag_stc_rec_displ_duration].format(time_unit=time_unit),
                                    operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
                


        ################################################################################################
        ################################################################################################

        self.flowsheet.header_organizer(op_nr=self.operation_seq, title=lang_dict_uo_titles[self.uo_tag])
        if not (self.pre_comment == None or self.pre_comment == ''):
            self.flowsheet.put_body_comments(self.pre_comment)
            self.flowsheet.linefeed()        
        for input_item in self.arr_inputs:
            input_item.print_input()

        if self.mode_washing == opt_washmode_reslurry:
            print_reslurry()
        elif self.mode_washing == opt_washmode_soak:
            print_soaking()
        elif self.mode_washing == opt_washmode_displacement:
            print_diplwash()
        else:
            print_soaking()

        if not (self.post_comment == None or self.post_comment == ''):
            self.flowsheet.put_body_comments(self.post_comment)
            self.flowsheet.linefeed()
    
    @staticmethod
    def generate_test_df(precomment:str|None=None,
                       postcomment:str|None=None,
                       equipment:str|None=None,
                       mode_washing:str|None=opt_washmode_reslurry,
                       duration_minutes:float|None=None,
                       agitation_rpm:float|None=None,
                       material_name:str=None,
                       metrics_val:float=None,
                       metrics_unit:str=None,
                       error_pct:float=matin.error_pct_default,
                       method:str=None,
                       vessel_train:list[str]=None,
                       time_control:str=matin.timectrl_none,
                       time_min:float=None,
                       time_max:float=None,
                       temp_control:str=matin.temprctrl_none,
                       temp_min:float=None,
                       temp_max:float=None,
                       id_input:int=None,
                       list_id_basis_input:list[int]=None)->pd.DataFrame:
        #The first row holds both the UO-specific parameters and the first solvent input.
        df_inpt = Input.generate_test_df(material_name=material_name,
                                         metrics_val=metrics_val,
                                         metrics_unit=metrics_unit,
                                         error_pct=error_pct,
                                         method=method,
                                         vessel_train=vessel_train,
                                         time_control=time_control,
                                         time_min=time_min,
                                         time_max=time_max,
                                         temp_control=temp_control,
                                         temp_min=temp_min,
                                         temp_max=temp_max,
                                         id_input=id_input,
                                         list_id_basis_input=list_id_basis_input)
        hedr:list[str] = defs.list_hedr_cmn_io_dtil + list_hedr + matin.list_hedr
        df = df_inpt.reindex(columns=hedr).astype(object)
        df = df.where(pd.notna(df), None)

        df.at[df.index[0], hedr_precomment] = precomment
        df.at[df.index[0], hedr_postcomment] = postcomment
        df.at[df.index[0], hedr_equipment] = equipment
        df.at[df.index[0], hedr_mode_washing] = mode_washing
        df.at[df.index[0], hedr_duration_washing_minutes] = duration_minutes
        df.at[df.index[0], hedr_agitation_rpm] = agitation_rpm

        return df
    
    @staticmethod
    def add_to_test_df(df: pd.DataFrame=None,
                       material_name:str=None,
                       metrics_val:float=None,
                       metrics_unit:str=None,
                       error_pct:float=matin.error_pct_default,
                       method:str=None,
                       vessel_train:list[str]=None,
                       time_control:str=matin.timectrl_none,
                       time_min:float=None,
                       time_max:float=None,
                       temp_control:str=matin.temprctrl_none,
                       temp_min:float=None,
                       temp_max:float=None,
                       id_input:int=None,
                       list_id_basis_input:list[int]=None)->None:
        """Adds another solvent input as a new row. The UO-specific parameters are held only in the first row."""
        Input.add_to_test_df(df=df,
                             material_name=material_name,
                             metrics_val=metrics_val,
                             metrics_unit=metrics_unit,
                             error_pct=error_pct,
                             method=method,
                             vessel_train=vessel_train,
                             time_control=time_control,
                             time_min=time_min,
                             time_max=time_max,
                             temp_control=temp_control,
                             temp_min=temp_min,
                             temp_max=temp_max,
                             id_input=id_input,
                             list_id_basis_input=list_id_basis_input)

    def get_list_inputs(self) -> list[Input]:
        return self.arr_inputs