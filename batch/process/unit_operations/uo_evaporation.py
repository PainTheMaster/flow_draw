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
hedr_agitation = defs.hedr_uo_evap_agitation
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

opt_press_ctrl_specific = defs.opt_uo_evap_press_ctrl_specific
"""option item for the attribute paress_spec_ for uo_evap: Specific pressure value"""
opt_press_ctrl_arbitrary_with_guide = defs.opt_uo_evap_press_ctrl_arbitrary_with_guide
"""option item for the attribute press_spec for uo_evap: Arbitrary with optional guideline"""
opt_press_ctrl_arbitrary = defs.opt_uo_evap_press_ctrl_arbitrary
"""option item for the attribute press_spec for uo_evap: Arbitrary without a guieline"""
opt_press_ctrl_full_vac = defs.opt_uo_evap_press_ctrl_full_vac
"""list of options for the parameter press_unit for uo_evap"""

opt_press_unit_MPaA = defs.opt_uo_evap_press_unit_MPaA
"""option item for the attribute press_unit for uo_evap: MPaA"""
opt_press_unit_kPaA = defs.opt_uo_evap_press_unit_kPaA
"""option item for the attribute press_unit for uo_evap: kPaA"""
opt_press_unit_MPaG = defs.opt_uo_evap_press_unit_MPaG
"""option item for the attribute press_unit for uo_evap: MPaG"""
opt_press_unit_kPaG = defs.opt_uo_evap_press_unit_kPaG
"""option item for the attribute press_unit for uo_evap: kPaG"""


dict_opt = defs.dict_opt_uo_evap
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
"""the tag for a sentence for component for uo_evap: instruction for the evaporation endpoint; includes placeholders {L_min}, {L_max}, {vol_min}, {vol_max}"""
tag_stc_flow_endpoint_spec_min = defs.tag_stc_flow_uo_evap_endpoint_spec_min
"""the tag for a sentence for component for uo_evap: instruction for minimum spec endpoint; includes placeholders {L_min}, {vol_min}"""
tag_stc_flow_endpoint_spec_max = defs.tag_stc_flow_uo_evap_endpoint_spec_max
"""the tag for a sentence for component for uo_evap: instruction for maximum spec endpoint; includes placeholders {L_max}, {vol_max}"""
tag_stc_flow_endpoint_guide_range = defs.tag_stc_flow_uo_evap_endpoint_guide_range
"""the tag for a sentence for component for uo_evap: instruction for the evaporation endpoint; includes placeholders {L_min}, {L_max}, {vol_min}, {vol_max}"""
tag_stc_flow_endpoint_guide_single = defs.tag_stc_flow_uo_evap_endpoint_guide_single
"""the tag for a sentence for component for uo_evap: instruction for the evaporation single point endpoint; includes placeholders {L_single}, {vol_single}"""
tag_stc_flow_endpoint_guide_min = defs.tag_stc_flow_uo_evap_endpoint_guide_min
"""the tag for a sentence for component for uo_evap: instruction for minimum guideline endpoint; includes placeholders {L_min}, {vol_min}"""
tag_stc_flow_endpoint_guide_max = defs.tag_stc_flow_uo_evap_endpoint_guide_max
"""the tag for a sentence for component for uo_evap: instruction for maximum guideline endpoint; includes placeholders {L_max}, {vol_max}"""
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
        self.Tj_min = None
        self.Tj_max = None
        self.Tbr_min = None
        self.Tbr_max:float = None
        self.P_ctrl:str = None
        self.P_min:float = None
        self.P_max:float = None
        self.P_unit:str = None
        self.agitation:float = None
        self.end_vw_spec_min:float = None
        self.end_vw_spec_max:float = None
        self.end_vw_guide_min:float = None
        self.end_vw_guide_max:float = None

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
            raise ValueError(f"{self.__class__.__name__}: Pressure unit not specified for Op. Seq. {self.operation_seq} although min and/or max pressure is provided.")

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
            raise ValueError(f"{self.__class__.__name__}: Pressure control method not specified for Op. Seq. {self.operation_seq} although min and/or max pressure is provided.")
        if not pd.isna(first_row[hedr_agitation]):
            self.agitation = first_row[hedr_agitation]
        if not pd.isna(first_row[hedr_val_endpoint_spec_min]):
            self.end_vw_spec_min = first_row[hedr_val_endpoint_spec_min]
        if not pd.isna(first_row[hedr_val_endpoint_spec_max]):
            self.end_vw_spec_max = first_row[hedr_val_endpoint_spec_max]
        if not pd.isna(first_row[hedr_val_endpoint_guide_min]):
            self.end_vw_guide_min = first_row[hedr_val_endpoint_guide_min]
        if not pd.isna(first_row[hedr_val_endpoint_guide_max]):
            self.end_vw_guide_max = first_row[hedr_val_endpoint_guide_max]

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

        if not (self.post_comment == None or self.post_comment == ''):
            self.flowsheet.put_body_comments(self.post_comment)
            self.flowsheet.linefeed()
    
    def __put_Tj(self):
        pass

    def __put_press(self):
        """
        Compatible with all cases. If information, e.g., min/max press or control method, is provided, put the necessary items on the flowsheet.
        Otherwise, put nothing on the flowsheet. Safe to incorporate in any case.
        """
        #Pressure control method specif and P_min and/or P_max
        sentence:str = None
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
                                   P_ctrol==opt_press_ctrl_specific; P_min is None; P_max is None.")
            self.flowsheet.put_line(content=sentence,
                                    record=dict_stcs_flow[tag_stc_flow_rec_press].format(P_unit=self.P_unit))
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
                                   P_ctrol==opt_press_ctrl_arbitrary_with_guide; P_min is None; P_max is None.")
            self.flowsheet.put_line(content=sentence,
                                    record=dict_stcs_flow[tag_stc_flow_rec_press].format(P_unit=self.P_unit))
        elif self.P_ctrl == opt_press_ctrl_arbitrary:
            sentence = dict_part_flow[tag_part_flow_pres_arbitrary]
            temp_P_unit:str = None
            if self.P_unit is not None:
                temp_P_unit = self.P_unit
            else:
                temp_P_unit = opt_press_unit_MPaG
            self.flowsheet.put_line(content=sentence,
                                    record=dict_stcs_flow[tag_stc_flow_rec_press].format(P_unit=temp_P_unit))            
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
            sentence = ""


    def __put_endpoint(self):
        pass
