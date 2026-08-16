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

hedr_origin = "origin"
"""Header item for uo_phase_discharge: origin of the discarded lower phase, e.g., reaction vessel, etc."""
hedr_via = "via"
"""Header item for uo_phase_discharge: way point of the discarded lower phase, e.g., multiplexker, etc"""
hedr_destin = "destination"
"""Header item for uo_phase_discharge: destination of the discarded lower phase, e.g., wate liqour tank, etc"""
list_hedr = [hedr_origin, hedr_via, hedr_destin]
"""list of  hader fields for the unit operation phase discharge"""

key_json_single_destin = "single_destination"
"""For JSON schema. Key for a single destination of the discharged phase."""

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

tag_part_flow_method_connection = "line connection"
"""Tag for a flowsheet component for a unit operation phase discharging: Discharging line connection"""
tag_part_flow_chk_connected = "check box line connected"
"""Tag for a flowsheet component for a unit operation phase discharging: check box for phase discharging line connected"""
tag_part_flow_method_disch = "instr (method col) disch"
"""Tag for a flowsheet component for a unit operation phase discharging: Instruction (method colum) for discharging."""
tag_part_flow_content_disch = "action (content col) disch"
"""Tag for a flowsheet component for a unit operation phase discharging: Description of action (content column) for discharging"""
tag_part_flow_chk_discharged = "check box phase discharged"
"""Tag for a flowsheet component for a unit operation phase discharging: check box for the completion of the phase discharging"""

dict_jp_part_flow:dict[str, str]={tag_part_flow_method_connection : "ライン構築",
                                  tag_part_flow_chk_connected : "□ ライン構築確認",
                                  tag_part_flow_method_disch : "下層排出",
                                  tag_part_flow_content_disch : "排出実施", 
                                  tag_part_flow_chk_discharged : "□ 実施確認"}

dict_part_flow = dict_jp_part_flow
"""Language dictionary for flowsheet parts for the unit operation phase discharging"""

                    #>>>>>>>>>>>>> Sentences <<<<<<<<<<<<<<<<<<<<<<<<<

tag_stc_origin = "sentence origin"
"""A tag for an instruction sentence for a unit operation phase discharging: sentence to designate the origon vessel of the discharged phase, includes placeholder {origin}"""
tag_stc_via = "sentence via"
"""A tag for an instruction sentence for a unit operation phase discharging: sentence to designate the way point, e.g., multiplexer, includes placeholder {via}"""
tag_stc_destin_single = "sentence single destination"
"""A tag for an instruction sentence for a unit operation phase discharging: sentence to designate the destination, includes placeholder {destination}"""
tag_stc_destin_multi = "sentence multiple destination"
"""A tag for an instruction sentence for a unit operation phase discharging: sentence to designate multiple destinations, includes placeholder {destination}--singular!"""

dict_jp_stcs = {tag_stc_origin : "移送元: {origin}",
                tag_stc_via : "経由: {via}",
                tag_stc_destin_single : "移送先: {destination}",
                tag_stc_destin_multi : "移送先: {destination} (使用したものを〇)"}

dict_stcs = dict_jp_stcs
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
        return list_hedr

    def get_detail_option_menu(self) -> Optional[dict[str, list[str]]]:
        return None

    def get_json_schema(caller: trdef.UniversalTrait=None)->Objason:
        common_schema:list[Primitive] = PhaseDisch.json_common()
        origin = Primitive(prim_type='string',
                           key=hedr_origin,
                           description='Origin vessel of the discharged process liquid. If not specified in the data source, please put <placeholder>.',
                           )
        via = Primitive(prim_type='string',
                        key=hedr_via,
                        description='Way point of the discharged process liquid, e.g., multiplexer. Nullable if not specified in the data source.',
                        nullable=True,
                        required = True)
        single_destin = Primitive(prim_type='string',
                                  key=key_json_single_destin,
                                  description='Destination of the discharged process liquid. E.g., waste tank, etc.'
                                  'Multiple destinations are allowed, as well as a sole destination. '
                                  'If not specified in the data source, please put <placeholder>.',
                                  nullable=False,
                                  required=True)
        
        destin = Array(key=hedr_destin,
                       content=single_destin,
                       description=f'An array of destination(s) {key_json_single_destin} of the discharged process liquid. E.g., waste tank, etc.',
                       nullable=False,
                       required=True)
        
        obj_schema = Objason(key = PhaseDisch.uo_tag,
                            description = 'Unit operation: phase discharge',
                            props = common_schema + [origin, via, destin],
                            nullable = False)
        return obj_schema

    def load_from_json_dict(self, json_dict: dict[str, any]):
        super().load_from_json_dict(json_dict)
        self.origin = json_dict.get(hedr_origin, None)
        self.via = json_dict.get(hedr_via, None)
        self.destin = json_dict.get(hedr_destin, [])

        
    def output_unit_operation(self):
        self.flowsheet.header_organizer(op_nr=self.operation_seq, title=lang_dict_uo_titles[self.uo_tag])
        if not (self.pre_comment == None or self.pre_comment == ''):
            self.flowsheet.put_body_comments(self.pre_comment)
            self.flowsheet.linefeed()        
        if len(self.destin) >= 1:
            self.__put_line_connection()
            self.flowsheet.linefeed()
        
        self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                method=dict_part_flow[tag_part_flow_method_disch],
                                content=dict_part_flow[tag_part_flow_content_disch],
                                record=dict_part_flow[tag_part_flow_chk_discharged],
                                operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
        self.flowsheet.linefeed()

        if not (self.post_comment == None or self.post_comment == ''):
            self.flowsheet.put_body_comments(self.post_comment)
            self.flowsheet.linefeed()

    def __put_line_connection(self):
        stc_destin:str = ''
        if len(self.destin) == 1:
            stc_destin = dict_stcs[tag_stc_destin_single].format(destination=self.destin[0])
        else:
            destin_combi:str = ''
            for single_destin in self.destin:
                destin_combi += (single_destin+'/')
            destin_combi = destin_combi.removesuffix('/')
            stc_destin = dict_stcs[tag_stc_destin_multi].format(destination=destin_combi)
        
        if self.origin is not None:
            self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                    method=dict_part_flow[tag_part_flow_method_connection],
                                    content=dict_stcs[tag_stc_origin].format(origin=self.origin),
                                    record=dict_part_flow[tag_part_flow_chk_connected],
                                    operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
            if self.via is not None:
                self.flowsheet.put_line(content=dict_stcs[tag_stc_via].format(via=self.via))
            self.flowsheet.put_line(content=stc_destin)
        elif self.via is not None:
            self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                    method=dict_part_flow[tag_part_flow_method_connection],
                                    content=dict_stcs[tag_stc_via].format(via=self.via),
                                    record=dict_part_flow[tag_part_flow_chk_connected],
                                    operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
            self.flowsheet.put_line(content=stc_destin)
        else:
            self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                    method=dict_part_flow[tag_part_flow_method_connection],
                                    content=stc_destin,
                                    record=dict_part_flow[tag_part_flow_chk_connected],
                                    operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
                