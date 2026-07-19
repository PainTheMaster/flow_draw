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
from flow_draw.data_io.json_io import Objason, Array, Primitive
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
hedr_Tj_min = defs.hedr_uo_evap_Tj_min
"""header item for the unit operation evaporation: Tj lower limit for evaporation"""
hedr_Tj_max = defs.hedr_uo_evap_Tj_max
"""header item for the unit operation evaporation: Tj higher limit for evaporation"""
hedr_T_brine_cond_min = defs.hedr_uo_evap_T_brine_cond_min
"""header item for the unit operation evaporation: lower limit of brine temperature for cndenser"""
hedr_T_brine_cond_max = defs.hedr_uo_evap_T_brine_cond_max
"""header item for the unit operation evaporation: upper limit of brine temperature for cndenser"""
hedr_press_ctrl = defs.hedr_uo_evap_press_ctrl
"""header item for the unit operation evaporation: pressure specification; arbitrary or specific"""
hedr_press_min = defs.hedr_uo_evap_press_min
"""header item for the unit operation evaporation: lower limit for the evaporation pressure"""
hedr_press_max = defs.hedr_uo_evap_press_max
"""header item for the unit operation evaporation: upper limit for the evaporation pressure"""
hedr_press_unit = defs.hedr_uo_evap_press_unit
"""header item for the unit operation evaporation: pressure unit for the evaporation"""
hedr_agit_spec = defs.hedr_uo_evap_agit_spec
"""header item for the unit operation evaporation: agitation specification; Specific RPM/Guidance RPM/arbitrary"""
hedr_agit_rpm = defs.hedr_uo_evap_agit_rpm
"""header item for the unit operation evaporation: agitation rate"""
hedr_val_endpoint_spec_min = defs.hedr_uo_evap_val_endpoint_spec_min
"""header item for the unit operation evaporation: minimum spec value for the evaporation end point"""
hedr_val_endpoint_spec_max = defs.hedr_uo_evap_val_endpoint_spec_max
"""header item for the unit operation evaporation: maximum spec value for the evaporation end point"""
hedr_val_endpoint_guide_min = defs.hedr_uo_evap_val_endpoint_guide_min
"""header item for the unit operation evaporation: minimum guideline value for the evaporation end point"""
hedr_val_endpoint_guide_max = defs.hedr_uo_evap_val_endpoint_guide_max
"""header item for the unit operation evaporation: maximum guideline value for the evaporation end point"""
list_hedr = defs.list_hedr_uo_evap
"""list of header fields for the uo_evap"""


#########################################################
# UO-specific options, list, header_item: list dictionry thereof (for data input and internalsignaling)
#########################################################




opt_press_ctrl_specific = "Specific_pressure"
"""option item for the attribute paress_spec_ for uo_evap: Specific pressure value"""
opt_press_ctrl_arbitrary_with_guide = "Arbitrary_with_optional_guideline"
"""option item for the attribute press_spec for uo_evap: Arbitrary with optional guideline"""
opt_press_ctrl_arbitrary = "Arbitrary"
"""option item for the attribute press_spec for uo_evap: Arbitrary without a guieline"""
opt_press_ctrl_full_vac = "Full_vacuum_(FV)"
"""list of options for the parameter press_unit for uo_evap"""

list_opt_press = [opt_press_ctrl_specific,
                  opt_press_ctrl_arbitrary_with_guide,
                  opt_press_ctrl_arbitrary,
                  opt_press_ctrl_full_vac]


opt_press_unit_MPaA = "MPaA"
"""option item for the attribute press_unit for uo_evap: MPaA"""
opt_press_unit_kPaA = "kPaA"
"""option item for the attribute press_unit for uo_evap: kPaA"""
opt_press_unit_MPaG = "MPaG"
"""option item for the attribute press_unit for uo_evap: MPaG"""
opt_press_unit_kPaG = "kPaG"
"""option item for the attribute press_unit for uo_evap: kPaG"""
list_opt_press_unit = [opt_press_unit_MPaA,
                       opt_press_unit_kPaA,
                       opt_press_unit_MPaG,
                       opt_press_unit_kPaG]

opt_agit_spec_specif = "Specific_RPM"
"""option item for the attribute agitation spec for uo_evap: A specific RPM is provided by the user"""
opt_agit_spec_guide = "Guidance_RPM"
"""option item for the attribute agitation spec for uo_evap: A guidance RPM is provided by the user"""
opt_agit_spec_arbitrary = "arbitrary_RPM"
"""option item for the attribute agitation spec for uo_evap: Totally discretional RPM for evaporation"""
list_opt_agit_spec = [opt_agit_spec_specif,
                      opt_agit_spec_guide,
                      opt_agit_spec_arbitrary]

#dict_opt = defs.dict_opt_uo_evap
dict_opt = {hedr_press_ctrl:list_opt_press,
            hedr_press_unit:list_opt_press_unit,
            hedr_agit_spec:list_opt_agit_spec}
"""Dictionary of <header item>:<drop-down options>"""


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


                #>>>>>>>>>>>>>>>>Tags for flowsheet components <<<<<<<<<<<<<<<<<<<<<<<<<

tag_part_flow_method_ini = defs.tag_part_flow_uo_evap_method_ini
"""the tag for a flowsheet component for uo_evap: a sub title to commense evaporation in the method column"""
tag_part_flow_instr_chronol_rec = defs.tag_part_flow_uo_evap_instr_chronol_rec
"""the tag for a flowsheet component for uo_evap: instruction to take a chronological record"""
tag_part_flow_Tj_artibrary = defs.tag_part_flow_uo_evap_Tj_artibrary
"""the tag for a flowhsheet component for uo_evap: instruction for arbitrary Tj for evaporation"""
tag_part_flow_T_brine_artibrary = defs.tag_part_flow_uo_evap_T_brine_artibrary
"""the tag for a flowhsheet component for uo_evap: instruction for arbitrary brine temperature for evaporation"""
tag_part_flow_pres_arbitrary = defs.tag_part_flow_uo_evap_pres_arbitrary
"""the tag for a flowsheet component for uo_evap: instruction for arbitrary pressure for evaporation"""
tag_part_flow_pres_full_vac = defs.tag_part_flow_uo_evap_pres_full_vac
"""the tag for a flowhsheet component for uo_evap: instruction for full vacuume for evaporation"""
tag_part_flow_agitation_arbitray = defs.tag_part_flow_uo_evap_agitation_arbitray
"""the tag for a flowsheet component for uo_evap: agitation at an arbitrary rotation"""
tag_part_flow_method_end = defs.tag_part_flow_uo_evap_method_end
"""the tag for a flowsheet component for uo_evap: end of evaporation"""
tag_part_flow_rec_Tj_sp = defs.tag_part_flow_uo_evap_rec_Tj_sp
"""the tag for a flowsheet component for uo_evap: record field for Tj"""
tag_part_flow_rec_T_brine_sp = defs.tag_part_flow_uo_evap_rec_T_brine_sp
"""the tag for a flowsheet component for uo_evap: record field for brine temperature"""
tag_part_flow_rec_rpm = defs.tag_part_flow_uo_evap_rec_rpm
"""the tag for a flowsheet component for uo_evap: record field for agitation rate"""
tag_part_flow_rec_Ti_ini = defs.tag_part_flow_uo_evap_rec_Ti_ini
"""the tag for a flowsheet component for uo_evap: recorod field for Ti at the beginning of evaporation"""
tag_part_flow_rec_Ti_max = defs.tag_part_flow_uo_evap_rec_Ti_max
"""the tag for a flowsheet component for uo_evap: record field for the maximum Ti during evaporation"""
tag_part_flow_rec_Ti_end = defs.tag_part_flow_uo_evap_rec_Ti_end
"""the tag for a flowhsheet component for uo_evap: record field for the Ti at the end"""
tag_part_flow_rec_vol_end = defs.tag_part_flow_uo_evap_rec_vol_end
"""the tag for a flowhsheet component for uo_evap: record field for the volume (L) at the end"""

dict_part_flow = defs.dict_jp_part_flow_uo_evap
"""Language dictionary for flowsheet components"""


                #>>>>>>>>>>>>>>>Tags for flowsheet sentence templates <<<<<<<<<<<<<<<<<<<

tag_stc_flow_Tj_range = defs.tag_stc_flow_uo_evap_Tj_range
"""the tag for a sentence for component for uo_evap: Tj range for evaporation, includes placeholders {Tj_min} and {Tj_max}"""
tag_stc_flow_Tj_min = defs.tag_stc_flow_uo_evap_Tj_min
"""the tag for a sentence for component for uo_evap: minimum Tj for evaporation; includes placeholders {Tj_min}"""
tag_stc_flow_Tj_max = defs.tag_stc_flow_uo_evap_Tj_max
"""the tag for a sentence for component for uo_evap: maximum Tj for evaporation; includes placeholders {Tj_max}"""
tag_stc_flow_T_brine_range = defs.tag_stc_flow_uo_evap_T_brine_range
"""the tag for a sentence for component for uo_evap: T_brine range for evaporation, includes placeholders {Tbr_min} and {Tbr_max}"""
tag_stc_flow_T_brine_min = defs.tag_stc_flow_uo_evap_T_brine_min
"""the tag for a sentence for component for uo_evap: minimum T_brine for evaporation; includes placeholders {Tbr_min}"""
tag_stc_flow_T_brine_max = defs.tag_stc_flow_uo_evap_T_brine_max
"""the tag for a sentence for component for uo_evap: maximum T_brine for evaporation; includes placeholders {Tbr_max}"""
tag_stc_flow_press_spec_range = defs.tag_stc_flow_uo_evap_press_spec_range
"""the tag for a sentence for component for uo_evap: instruction for pressure range; includes placeholders {P_min}, {P_max}, {P_unit}"""
tag_stc_flow_press_spec_min = defs.tag_stc_flow_uo_evap_press_spec_min
"""the tag for a sentence for component for uo_evap: instruction for minimum pressure; includes placeholders {P_min} and {P_unit}"""
tag_stc_flow_press_spec_max = defs.tag_stc_flow_uo_evap_press_spec_max
"""the tag for a sentence for component for uo_evap: instruction for maximum pressure; includes placeholders {P_max} and {P_unit}"""
tag_stc_flow_press_guide_range = defs.tag_stc_flow_uo_evap_press_guide_range
"""the tag for a sentence for component for uo_evap: guideline for pressure range; includes placeholders {P_min}, {P_max}, {P_unit}"""
tag_stc_flow_press_guide_singlepoint = defs.tag_stc_flow_uo_evap_press_guide_singlepoint
"""the tag for a sentence for component for uo_evap: guideline for a single point pressure; includes placeholders {P}, {P_unit}"""
tag_stc_flow_press_guide_min = defs.tag_stc_flow_uo_evap_press_guide_min
"""the tag for a sentence for component for uo_evap: guideline for minimum pressure; includes placeholders {P_min} and {P_unit}"""
tag_stc_flow_press_guide_max = defs.tag_stc_flow_uo_evap_press_guide_max
"""the tag for a sentence for component for uo_evap: guideline for maximum pressure; includes placeholders {P_max} and {P_unit}"""
tag_stc_flow_agitation_spec = defs.tag_stc_flow_uo_evap_agitation_spec
"""the tag for a sentence for component for uo_evap: agitation at a specific agitation rate; includes placeholders {rpm}"""
tag_stc_flow_agitation_arbitrary_with_guide = defs.tag_stc_flow_uo_evap_agitation_arbitrary_with_guide
"""the tag for a sentence for component for uo_evap: agitation at a specific agitation rate; includes placeholders {rpm}"""
tag_stc_flow_endpoint_spec_range = defs.tag_stc_flow_uo_evap_endpoint_spec_range
"""the tag for a sentence for component for uo_evap: instruction for the evaporation endpoint; includes placeholders {L_min}, {L_max}, {vw_min}, {vw_max}"""
tag_stc_flow_endpoint_spec_min = defs.tag_stc_flow_uo_evap_endpoint_spec_min
"""the tag for a sentence for component for uo_evap: instruction for minimum spec endpoint; includes placeholders {L_min}, {vw_min}"""
tag_stc_flow_endpoint_spec_max = defs.tag_stc_flow_uo_evap_endpoint_spec_max
"""the tag for a sentence for component for uo_evap: instruction for maximum spec endpoint; includes placeholders {L_max}, {vw_max}"""
tag_stc_flow_endpoint_guide_range = defs.tag_stc_flow_uo_evap_endpoint_guide_range
"""the tag for a sentence for component for uo_evap: instruction for the evaporation endpoint; includes placeholders {L_min}, {L_max}, {vw_min}, {vw_max}"""
tag_stc_flow_endpoint_guide_single = defs.tag_stc_flow_uo_evap_endpoint_guide_single
"""the tag for a sentence for component for uo_evap: instruction for the evaporation single point endpoint; includes placeholders {L_single}, {vw_single}"""
tag_stc_flow_endpoint_guide_min = defs.tag_stc_flow_uo_evap_endpoint_guide_min
"""the tag for a sentence for component for uo_evap: instruction for minimum guideline endpoint; includes placeholders {L_min}, {vw_min}"""
tag_stc_flow_endpoint_guide_max = defs.tag_stc_flow_uo_evap_endpoint_guide_max
"""the tag for a sentence for component for uo_evap: instruction for maximum guideline endpoint; includes placeholders {L_max}, {vw_max}"""
tag_stc_flow_rec_press = defs.tag_stc_flow_uo_evap_rec_press
"""the tag for a sentence for component for uo_evap: recording field for vacuum; includes placeholders {P_unit}"""

dict_stcs_flow = defs.dict_jp_stcs_flow_uo_evap
"""Language dictionary for sentences for the unit operation evaporation"""


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

class Evaporation(uo.UnitOperation, uo_tag=defs.tag_uo_evap):
    def __init__(self,
                 caller: trdef.GetMats =None,
                 flowsheet:fsht.Flowsheet=None,
                 operation_seq: int=None,
                 num_subitems: int = None,
                 edit_comment:str=None):
        super().__init__(caller=caller, flowsheet=flowsheet, operation_seq=operation_seq, num_subitems=num_subitems, edit_comment=edit_comment)
        self.materials: mats.Materials = self.caller.get_mats()
        self.Tj_min:float = None
        self.Tj_max:float = None
        self.Tbr_min:float = None
        self.Tbr_max:float = None
        self.P_ctrl:str = None
        self.P_min:float = None
        self.P_max:float = None
        self.P_unit:str = None
        self.agit_spec:str = None
        self.agit_rpm:float = None
        self.end_vw_spec_min:float = None
        self.end_volume_spec_min:float = None
        self.end_vw_spec_max:float = None
        self.end_volume_spec_max:float = None
        self.end_vw_guide_min:float = None
        self.end_volume_guide_min:float = None
        self.end_vw_guide_max:float = None
        self.end_volume_guide_max:float = None

    def get_json_schema(caller = None):
        json_common = Evaporation.json_common()
        Tj_min = Primitive(prim_type='number',
                           key=hedr_Tj_min,
                           description='Lower limit of the jacket temperature of the reactor or evaporator. Optional. Please follow the given instruction.',
                           nullable=True)
        Tj_max = Primitive(prim_type='number',
                           key=hedr_Tj_max,
                           description='Upper limit of the jacket temperature of the reactor or evaporator. Optional. Please follow the given instruction.',
                           nullable=True)
        Tbr_cond_min = Primitive(prim_type='number',
                           key=hedr_T_brine_cond_min,
                           description='Lower limit of the temperature of the brine supplied to the condenser. Optional. Please follow the given instruction.',
                           nullable=True)
        Tbr_cond_max = Primitive(prim_type='number',
                           key=hedr_T_brine_cond_max,
                           description='Upper limit of the temperature of the brine supplied to the condenser. Optional. Please follow the given instruction.',
                           nullable=True)
        press_ctrl = Primitive(prim_type='string',
                               key=hedr_press_ctrl,
                               enum=list_opt_press,
                               description=f'Pressure control. '
                               f'"{opt_press_ctrl_specific}" means the evaporation must happen under a specific pressrue range. At least one one from "{hedr_press_min}" and "{hedr_press_max}" must be specified. '
                               f'"{opt_press_ctrl_arbitrary_with_guide}" shuld be chosen when recommended pressure range is specified by using at least one one from "{hedr_press_min}" and "{hedr_press_max}". '
                               f'If the pressure is at the operator\'s discretion, please select "{opt_press_ctrl_arbitrary}". Pressures ("{hedr_press_min}" and )doesn\'t have to be specified in this case. '
                               f'For evaporation at the lowet possible pressure, please select "{opt_press_ctrl_full_vac}".')
        press_min = Primitive(prim_type='number',
                              key=hedr_press_min,
                              description=f'Lower limit of the distillation pressure. '
                              f'At least on of this or "{hedr_press_max}" is needed if "{hedr_press_ctrl}" is "{opt_press_ctrl_specific}" or "{opt_press_ctrl_arbitrary_with_guide}". '
                              f'The unit of the pressure is specified by "{hedr_press_unit}".',
                              nullable=True,
                              required=True)
        press_max = Primitive(prim_type='number',
                              key=hedr_press_max,
                              description=f'Upper limit of the distillation pressure. '
                              f'At least on of this or "{hedr_press_min}" is needed if "{hedr_press_ctrl}" is "{opt_press_ctrl_specific}" or "{opt_press_ctrl_arbitrary_with_guide}". '
                              f'The unit of the pressure is specified by "{hedr_press_unit}".',
                              nullable=True,
                              required=True)
        press_unit = Primitive(prim_type='string',
                               key=hedr_press_unit,
                               enum=list_opt_press_unit,
                               nullable=True,
                               description=f'Pressure unit. This property is associated with "{hedr_press_min}" and "{hedr_press_max}". This property is mandatory if either of them has a value.')
        spec_agit = Primitive(prim_type='string',
                              key=hedr_agit_spec,
                              enum=list_opt_agit_spec,
                              description=f'Specification of the agitation during evaporation. '
                              f'With "{opt_agit_spec_specif}", specific agitation rate (rpm) shall be designated. '
                              f'Non-binding guidance agitation rate will be given when "{opt_agit_spec_guide}" is selected. '
                              f'If "{opt_agit_spec_arbitrary}" chosen, agitation rate is at operator\'s discretion.')
        agit_rate = Primitive(prim_type='number',
                              key=hedr_agit_rpm,
                              description=f'Agitation rate in rpm during condensation. This property must be filled if "{hedr_agit_spec} is "{opt_agit_spec_specif}" or "{opt_agit_spec_guide}".',
                              nullable=True)
        endpoint_spec_min = Primitive(prim_type='number',
                                      key=hedr_val_endpoint_spec_min,
                                      description='Specification. Lower limit of the liquid volume at the end of the condensation. Please specify the volume in volume-per-weight (v/w) unit.',
                                      nullable=True)
        endpoint_spec_max = Primitive(prim_type='number',
                                      key=hedr_val_endpoint_spec_max,
                                      description='Specification. Upper limit of the liquid volume at the end of the condensation. Please specify the volume in volume-per-weight (v/w) unit.',
                                      nullable=True)
        endpoint_guide_max = Primitive(prim_type='number',
                                       key=hedr_val_endpoint_guide_max,
                                       description='Non-binding guidance. Upper limit of the liquid volume at the end of the condensation. Please specify the volume in volume-per-weight (v/w) unit.',
                                       nullable=True)
        endpoint_guide_min = Primitive(prim_type='number',
                                       key=hedr_val_endpoint_guide_min,
                                       description='Non-binding guidance. Lower limit of the liquid volume at the end of the condensation. Please specify the volume in volume-per-weight (v/w) unit.',
                                       nullable=True)
        obj_evap = Objason(key=Evaporation.uo_tag,
                           description='Evaporation unit operation. Please follow the given instruction for each property.',
                           props=[Tj_min, Tj_max, Tbr_cond_min, Tbr_cond_max,
                                  press_ctrl, press_min, press_max, press_unit,
                                  spec_agit, agit_rate,
                                  endpoint_spec_min, endpoint_spec_max,
                                  endpoint_guide_min, endpoint_guide_max])
        return obj_evap


    def load_from_json_dict(self, json_dict: dict=None):
        """
        Loads necessary parameters from a JSON object.
        The header items must be in line with the definition the class Evaporation.
        The header items can be passed from the get_json_schema() of each UnitOperation-drived class.
        This is the overriding mehtod in the class Evaporation..
        """
        self.Tj_min = json_dict.get(hedr_Tj_min, None)
        self.Tj_max = json_dict.get(hedr_Tj_max, None)
        self.Tbr_min = json_dict.get(hedr_T_brine_cond_min, None)
        self.Tbr_max = json_dict.get(hedr_T_brine_cond_max, None)
        self.P_ctrl = json_dict.get(hedr_press_ctrl, None)
        self.P_min = json_dict.get(hedr_press_min, None)
        self.P_max = json_dict.get(hedr_press_max, None)
        self.P_unit = json_dict.get(hedr_press_unit, None)
        self.agit_spec = json_dict.get(hedr_agit_spec, None)
        self.agit_rpm = json_dict.get(hedr_agit_rpm, None)
        self.end_vw_spec_min = json_dict.get(hedr_val_endpoint_spec_min, None)
        self.end_vw_spec_max = json_dict.get(hedr_val_endpoint_spec_max, None)
        self.end_volume_spec_min = json_dict.get(hedr_val_endpoint_spec_min, None)
        self.end_volume_spec_max = json_dict.get(hedr_val_endpoint_spec_max, None)
        self.end_volume_guide_min = json_dict.get(hedr_val_endpoint_guide_min, None)
        self.end_volume_guide_max = json_dict.get(hedr_val_endpoint_guide_max, None)


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
        # for _, subitem in df.iterrows():
            #<uo-specific process>
        if not pd.isna(first_row[hedr_Tj_min]):
            self.Tj_min = first_row[hedr_Tj_min]
        if not pd.isna(first_row[hedr_Tj_max]):
            self.Tj_max = first_row[hedr_Tj_max]
        if not pd.isna(first_row[hedr_T_brine_cond_min]):
            self.Tbr_min = first_row[hedr_T_brine_cond_min]
        if not pd.isna(first_row[hedr_T_brine_cond_max]):
            self.Tbr_max = first_row[hedr_T_brine_cond_max]
        if not pd.isna(first_row[hedr_press_min]):
            self.P_min = first_row[hedr_press_min]
        if not pd.isna(first_row[hedr_press_max]):
            self.P_max = first_row[hedr_press_max]

        if not pd.isna(first_row[hedr_press_unit]): #no pressure value, no pressure unit -> Ok; pressure value provided, no pressure unit -> error
            self.P_unit = first_row[hedr_press_unit]
        elif self.P_min is not None or self.P_max is not None: #No pressure unit but some pressure value
            raise ValueError(f"{self.__class__.__name__}: Pressure unit not specified for Op. Seq. {self.operation_seq} \
                             although min and/or max pressure is provided.")

        if not pd.isna(first_row[hedr_press_ctrl]):
            # press_ctrl defined and P_min and/or P_max are provided. OK
            if self.P_min is not None or self.P_max is not None:
                self.P_ctrl = first_row[hedr_press_ctrl]
            # press ctrl is arbit or FV, in the meantime,  both P_min and P_max empty -> also OK
            elif first_row[hedr_press_ctrl] == opt_press_ctrl_arbitrary or first_row[hedr_press_ctrl] == opt_press_ctrl_full_vac: #if press_ctrl is arbitrary and P_min or P_max are not provided.
                self.P_ctrl = first_row[hedr_press_ctrl]
            #Pressure ctrl needs sonme specifi value, but not provided -> error
            else: #if press_ctrl is not arbitrary and P_min or P_max are not provided.
                raise ValueError(f"{self.__class__.__name__}: No of of Press_min and Press_max is provided for Op. Seq. {self.operation_seq}\
                                  although \"specific pressure\" or \"full vacuum\" is selectd for pressure control method.")
        #pressure control not defined, values not provided -> control on the shopfloor.
        elif self.P_min is None and self.P_max is None: #pressure control method not specified and pressure limits not provided -> arbitrary
            self.P_ctrl = opt_press_ctrl_arbitrary
        #pressure control not defined, but some pressure values are provided -> Not definitive=error
        else: #pressure control method not speficied, but pressure lmit(s) provided -> value error
            raise ValueError(f"{self.__class__.__name__}: Pressure control method not specified for Op. Seq. {self.operation_seq} \
                             although min and/or max pressure is provided.")

        if not pd.isna(first_row[hedr_agit_spec]):
            self.agit_spec = first_row[hedr_agit_spec]

        if not pd.isna(first_row[hedr_agit_rpm]):
            #rpm value provided, agitation specification selected -> OK
            if self.agit_spec == opt_agit_spec_specif or self.agit_spec == opt_agit_spec_guide:
                self.agit_rpm = first_row[hedr_agit_rpm]
            #rpm value provided, agitation specification not selected -> NOK
            else:
                raise ValueError(f"{self.__class__.__name__}: Agitation specification (specific rpm or guideline rpm) not selected \
                                 for Op. Seq. {self.operation_seq} although an agitation rpm value is provided.")                

        #No rpm value provided in the mean time the agitation spec requires some rpm value -> error
        elif self.agit_spec == opt_agit_spec_specif or self.agit_spec == opt_agit_spec_guide:
            raise ValueError(f"{self.__class__.__name__}: Agitation rate (rpm) not provided for Op. Seq. {self.operation_seq} \
                             although the user's selection for the agitation spec requires a specification or guidance value.")
        else:
            self.agit_spec = opt_agit_spec_arbitrary

        if not pd.isna(first_row[hedr_val_endpoint_spec_min]):
            self.end_vw_spec_min = first_row[hedr_val_endpoint_spec_min]
            self.end_volume_spec_min = self.materials.to_litre(self.end_vw_spec_min)
        if not pd.isna(first_row[hedr_val_endpoint_spec_max]):
            self.end_vw_spec_max = first_row[hedr_val_endpoint_spec_max]
            self.end_volume_spec_max = self.materials.to_litre(self.end_vw_spec_max)
        if not pd.isna(first_row[hedr_val_endpoint_guide_min]):
            self.end_vw_guide_min = first_row[hedr_val_endpoint_guide_min]
            self.end_volume_guide_min = self.materials.to_litre(self.end_vw_guide_min)
        if not pd.isna(first_row[hedr_val_endpoint_guide_max]):
            self.end_vw_guide_max = first_row[hedr_val_endpoint_guide_max]
            self.end_volume_guide_max = self.materials.to_litre(self.end_vw_guide_max)

    def get_detail_header(self) -> list[str]:
        return list_hedr

    def get_detail_option_menu(self) -> Optional[dict[str, list[str]]]:
        return dict_opt
    
    def output_unit_operation(self):
        self.flowsheet.header_organizer(op_nr=self.operation_seq, title=lang_dict_uo_titles[self.uo_tag])
        if not (self.pre_comment == None or self.pre_comment == ''):
            self.flowsheet.put_body_comments(self.pre_comment)
            self.flowsheet.linefeed()        

        #<Operation-specific processes here>
        self.__put_Tj()
        self.__put_Tbr()
        self.__put_press()
        self.__put_agitaion()
        self.flowsheet.put_line(record=dict_part_flow[tag_part_flow_rec_Ti_ini])
        self.flowsheet.linefeed()
        self.__put_endpoint()

        if not (self.post_comment == None or self.post_comment == ''):
            self.flowsheet.put_body_comments(self.post_comment)
            self.flowsheet.linefeed()
    
    def __put_Tj(self)->None:
        """
        Puts Tj confgiguration. Compatible with all Tj configuration pattern. Safe to place any case.
        Both Tj_min and Tj_max provided => Tj range
        Tj_min only or Tj_max only => TJ lower or upper limint only
        No value provided => arbitrary.
        This it the top component in the unit operation, just below the uo header. Therefore, places time recordl field,
        instruction to commense, temperature cofinguration record field, signature fields,
        together with the temeperature configuration instruction.
        """
        sentence:str = None
        if self.Tj_min is not None and self.Tj_max is not None:
            sentence = dict_stcs_flow[tag_stc_flow_Tj_range].format(Tj_min=self.Tj_min, Tj_max=self.Tj_max)
        elif self.Tj_min is not None:
            sentence = dict_stcs_flow[tag_stc_flow_Tj_min].format(Tj_min=self.Tj_min)
        elif self.Tj_max is not None:
            sentence = dict_stcs_flow[tag_stc_flow_Tj_max].format(Tj_max=self.Tj_max)
        else:
            sentence = dict_part_flow[tag_part_flow_Tj_artibrary]
        self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                method=dict_part_flow[tag_part_flow_method_ini],
                                content=sentence,
                                record=dict_part_flow[tag_part_flow_rec_Tj_sp],
                                operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                witness=lang_dict_cmn[tag_flow_cmn_rec_sign])


    def __put_Tbr(self) -> None:
        """
        Put brine temeperature configuration instruction.
        Compatible with all instruction pattern. If no value is provided, instruction for arbitrary temperature control is put.
        """
        sentence:str = None
        if self.Tbr_min is not None and self.Tbr_max is not None:
            sentence = dict_stcs_flow[tag_stc_flow_T_brine_range].format(Tbr_min=self.Tbr_min, Tbr_max=self.Tbr_max)
        elif self.Tbr_min is not None:
            sentence = dict_stcs_flow[tag_stc_flow_T_brine_min].format(Tbr_min=self.Tbr_min)
        elif self.Tbr_max is not None:
            sentence = dict_stcs_flow[tag_stc_flow_T_brine_max].format(Tbr_max=self.Tbr_max)
        else:
            sentence = dict_part_flow[tag_part_flow_T_brine_artibrary]
        self.flowsheet.put_line(content=sentence,
                                record=dict_part_flow[tag_part_flow_rec_T_brine_sp])

    def __put_press(self)->None:
        """
        Compatible with all cases. If information, e.g., min/max press or control method, is provided, put the necessary items on the flowsheet.
        Otherwise, put nothing on the flowsheet. Safe to incorporate in any case.
        """
        sentence:str = None
        #Pressure control method specif and P_min and/or P_max
        if self.P_ctrl == opt_press_ctrl_specific:
            if self.P_min is not None and self.P_max is not None:
                sentence = dict_stcs_flow[tag_stc_flow_press_spec_range].format(P_min=self.P_min, P_max=self.P_max, P_unit=self.P_unit)
            elif self.P_min is not None:
                sentence = dict_stcs_flow[tag_stc_flow_press_spec_min].format(P_min=self.P_min, P_unit=self.P_unit)
            elif self.P_max is not None:
                sentence = dict_stcs_flow[tag_stc_flow_press_spec_max].format(P_min=self.P_max, P_unit=self.P_unit)
            else:
                raise RuntimeError(f"{self.__class__.__name__}.__put_press(): This branch is not supposed to be reached.\
                                   This runtime error is raised for the sake of debug.\
                                   P_ctrol==opt_press_ctrl_specific; P_min is None; P_max is None for Op. Seq. {self.operation_seq}.")
            self.flowsheet.put_line(content=sentence,
                                    record=dict_stcs_flow[tag_stc_flow_rec_press].format(P_unit=self.P_unit))
        #Pressure control method guideline pressure only.
        elif self.P_ctrl == opt_press_ctrl_arbitrary_with_guide:
            if self.P_min is not None and self.P_max is not None:
                sentence = dict_stcs_flow[tag_stc_flow_press_guide_range].format(P_min=self.P_min, P_max=self.P_max, P_unit=self.P_unit)
            elif self.P_min is not None:
                sentence = dict_stcs_flow[tag_stc_flow_press_guide_min].format(P_min=self.P_min, P_unit=self.P_unit)
            elif self.P_max is not None:
                sentence = dict_stcs_flow[tag_stc_flow_press_guide_max].format(P_min=self.P_max, P_unit=self.P_unit)
            else:
                raise RuntimeError(f"{self.__class__.__name__}__put_press(): This branch is not supposed to be reached.\
                                   This runtime error is raised for the sake of debug. \
                                   P_ctrol==opt_press_ctrl_arbitrary_with_guide; P_min is None; P_max is None for Op. Seq. {self.operation_seq}.")
            self.flowsheet.put_line(content=sentence,
                                    record=dict_stcs_flow[tag_stc_flow_rec_press].format(P_unit=self.P_unit))
        #Pressure control method at complete discretion.
        elif self.P_ctrl == opt_press_ctrl_arbitrary:
            sentence = dict_part_flow[tag_part_flow_pres_arbitrary]
            temp_P_unit:str = None
            if self.P_unit is not None:
                temp_P_unit = self.P_unit
            else:
                temp_P_unit = opt_press_unit_MPaG
            self.flowsheet.put_line(content=sentence,
                                    record=dict_stcs_flow[tag_stc_flow_rec_press].format(P_unit=temp_P_unit))            
        #Full vacuum.
        elif self.P_ctrl == opt_press_ctrl_full_vac:
            sentence = dict_part_flow[tag_part_flow_pres_full_vac]
            temp_P_unit:str = None
            if self.P_unit is not None:
                temp_P_unit = self.P_unit
            else:
                temp_P_unit = opt_press_unit_MPaG
            self.flowsheet.put_line(content=sentence,
                                    record=dict_stcs_flow[tag_stc_flow_rec_press].format(P_unit=temp_P_unit))                                   
        else:
            raise RuntimeError(f"{self.__class__.__name__}__put_press(): This branch is not supposed to be reached.\
                                This runtime error is raised for the sake of debug. \
                                P_ctrol doesn't match any given option for Op. Seq. {self.operation_seq}.")
        
    def __put_agitaion(self)->None:
        """
        Compatible with all instruction/input pattern. If no value is provided, puts sentence for arbitrary agitation rate.
        Safe for all cases.
        """
        sentence:str = None
        if self.agit_spec == opt_agit_spec_specif:
            sentence = dict_stcs_flow[tag_stc_flow_agitation_spec].format(rpm=self.agit_rpm)
        elif self.agit_spec == opt_agit_spec_guide:
            sentence = dict_stcs_flow[tag_stc_flow_agitation_arbitrary_with_guide].format(rpm=self.agit_rpm)
        else:
            sentence = dict_part_flow[tag_part_flow_agitation_arbitray]
        self.flowsheet.put_line(content=sentence,
                                record=dict_part_flow[tag_part_flow_rec_rpm])
        
    def __put_endpoint(self)->None:
        """
        Compatible with all (decent) instruction patterns: Both spec and guideline, spec only, guideline only.
        If neither is provided, raises a ValueError.
        Together with the endpoint volume-related instruction and record fields, instruction to termination,
        Ti at the end, Ti_max, and signature fields are put on the flowsheet.
        """
        sentence_spec:str = None
        if self.end_vw_spec_min is not None and self.end_vw_spec_max is not None:
            sentence_spec = dict_stcs_flow[tag_stc_flow_endpoint_spec_range].format(L_min=self.end_volume_spec_min,
                                                                                    L_max=self.end_volume_spec_max,
                                                                                    vw_min=self.end_vw_spec_min,
                                                                                    vw_max=self.end_vw_spec_max)
        elif self.end_vw_spec_min is not None:
            sentence_spec = dict_stcs_flow[tag_stc_flow_endpoint_spec_min].format(L_min=self.end_volume_spec_min, vw_min=self.end_vw_spec_min)
        elif self.end_vw_spec_max is not None:
            sentence_spec = dict_stcs_flow[tag_stc_flow_endpoint_spec_max].format(L_max=self.end_volume_spec_max, vw_max=self.end_vw_spec_max)
        else:
            sentence_spec = None
        
        sentence_guide:str = None
        if self.end_vw_guide_min is not None and self.end_vw_guide_max is not None:
            if self.end_vw_guide_min != self.end_vw_guide_max:
                sentence_guide = dict_stcs_flow[tag_stc_flow_endpoint_guide_range].format(L_min=self.end_volume_guide_min,
                                                                                          L_max=self.end_volume_guide_max,
                                                                                          vw_min=self.end_vw_guide_min,
                                                                                          vw_max=self.end_vw_guide_max)
            else:
                sentence_guide = dict_stcs_flow[tag_stc_flow_endpoint_guide_single].format(L_single=self.end_volume_guide_min,
                                                                                           vw_single=self.end_vw_guide_min)
        elif self.end_vw_guide_min is not None:
            sentence_guide = dict_stcs_flow[tag_stc_flow_endpoint_guide_min].format(L_min=self.end_volume_guide_min, vw_min=self.end_vw_guide_min)
        elif self.end_vw_guide_max is not None:
            sentence_guide = dict_stcs_flow[tag_stc_flow_endpoint_guide_max].format(L_max=self.end_volume_guide_max, vw_max=self.end_vw_guide_max)
        else:
            sentence_guide = None

        if sentence_spec is None and sentence_guide is None:
            raise ValueError(f"{self.__class__.__name__}.__put_endpoint(): No one of guideline or specification lower or upper limit \
                             for the distillation endpoint has been provided for Op. Seq. {self.operation_seq}.")
        elif sentence_spec is not None and sentence_guide is not None:
            self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                    method=dict_part_flow[tag_part_flow_method_end],
                                    content=sentence_spec,
                                    record=dict_part_flow[tag_part_flow_rec_vol_end],
                                    operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
            self.flowsheet.put_line(content=sentence_guide,
                                    record=dict_part_flow[tag_part_flow_rec_Ti_max])
            self.flowsheet.put_line(record=dict_part_flow[tag_part_flow_rec_Ti_end])
        elif sentence_spec is not None:
            self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                    method=dict_part_flow[tag_part_flow_method_end],
                                    content=sentence_spec,
                                    record=dict_part_flow[tag_part_flow_rec_vol_end],
                                    operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
            self.flowsheet.put_line(record=dict_part_flow[tag_part_flow_rec_Ti_max])
            self.flowsheet.put_line(record=dict_part_flow[tag_part_flow_rec_Ti_end])
        else: #Only guide line value(s) is provided.
            self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                    method=dict_part_flow[tag_part_flow_method_end],
                                    content=sentence_guide,
                                    record=dict_part_flow[tag_part_flow_rec_vol_end],
                                    operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
            self.flowsheet.put_line(record=dict_part_flow[tag_part_flow_rec_Ti_max])
            self.flowsheet.put_line(record=dict_part_flow[tag_part_flow_rec_Ti_end])

    @classmethod
    def generate_test_df(cls,
                         precomment:str=None,
                         postcomment:str=None,
                         Tj_min:float=None,
                         Tj_max:float=None,
                         Tbr_min:float=None,
                         Tbr_max:float=None,
                         press_ctrl:str=None,
                         press_min:float=None,
                         press_max:float=None,
                         unit_press:str=None,
                         agit_spec:str=None,
                         agit_rpm:float=None,
                         vw_spec_min:float=None,
                         vw_spec_max:float=None,
                         vw_guide_min:float=None,
                         vw_guide_max:float=None)->pd.DataFrame:
        hedr:list[str] = defs.list_hedr_cmn_io_dtil + list_hedr
        content: list[any] = [None]*len(hedr)
        s:pd.Series = pd.Series(data=content, index=hedr)
        df = s.to_frame().T
        df.at[df.index[0], hedr_precomment]=precomment
        df.at[df.index[0], hedr_postcomment]=postcomment
        df.at[df.index[0], hedr_Tj_min]=Tj_min
        df.at[df.index[0], hedr_Tj_max]=Tj_max
        df.at[df.index[0], hedr_T_brine_cond_min]=Tbr_min
        df.at[df.index[0], hedr_T_brine_cond_max]=Tbr_max
        df.at[df.index[0], hedr_press_ctrl]=press_ctrl
        df.at[df.index[0], hedr_press_min]=press_min
        df.at[df.index[0], hedr_press_max]=press_max
        df.at[df.index[0], hedr_press_unit]=unit_press
        df.at[df.index[0], hedr_agit_spec]=agit_spec
        df.at[df.index[0], hedr_agit_rpm]=agit_rpm
        df.at[df.index[0], hedr_val_endpoint_spec_min]=vw_spec_min
        df.at[df.index[0], hedr_val_endpoint_spec_max]=vw_spec_max
        df.at[df.index[0], hedr_val_endpoint_guide_min]=vw_guide_min
        df.at[df.index[0], hedr_val_endpoint_guide_max]=vw_guide_max

        return df




