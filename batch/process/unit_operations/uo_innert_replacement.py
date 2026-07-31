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




#########################################################
# Common items: headers etc
#########################################################
header_precomment = defs.hedr_cmn_io_dtil_precmnt #Don't include this in the specific header list!!!
header_postcomment = defs.hedr_cmn_io_dtil_postcmnt #Don't include this in the specific header list!!!


#########################################################
# UO-specific hader items and list thereof
#########################################################

#hedr_<something> = defs.hedr_<unit operation>_<specification item>
#list_hedr = defs.list_hedr_<list of header items for the uo>
#dict_dtil_drpdwn = defs.dict_opt_<unit operation>
hedr_gas = "Innert_Gas"
"""Detail header item: Innert gas used for replacement"""
hedr_neg_pres = "Negative_Press(MPaG)"
"""Detail header item: Negative pressure before innert gas compensation"""
hedr_num_repeat = "Repetition"
"""Detail header item: Times the replacement (vaccum then compensation) repeated"""
list_hedr = [hedr_gas,
            hedr_neg_pres,
            hedr_num_repeat]
"""Detail header list: List of header items for detail input form for innert gas relacement"""

#########################################################
# UO-specific options, list, header_item: list dictionry thereof (for data input and internalsignaling)
#########################################################

opt_gas_N2 = "N2"
"""Drop-down option item: choice of gas for innertization. Nitrogen gas"""
opt_gas_Ar = "Ar"
"""Drop-down option item: choice of gas for innertization. Argon gas"""
opt_gas_He = "He"
"""Drop-down option item: choice of gas for innertization. Helium gas"""
opt_gas_plchldr = "(placeholder)"
"""Drop-down option item: choice of gas for innertization. Placeholer"""
list_opt_gas = [opt_gas_N2,
                opt_gas_Ar,
                opt_gas_He,
                opt_gas_plchldr]
"""List for a drop-down list in the detail input table"""

dict_opt = {hedr_gas:list_opt_gas}
"""Dictionary for drop-down lists in detail input form"""


#########################################################
# signal -> local language dictionary and tags for it
#########################################################
lang_dict_uo_titles = defs.dict_jp_part_uo_titles
"""dict[<tag>:<unit operation name] for unit operation name in local language}"""


#Tags (keys) for translation of common parts 
tag_flow_cmn_rec_time = defs.tag_flow_cmn_rec_time
"""The key to the time-recording field for the flowsheet, a common item."""
tag_flow_cmn_rec_sign = defs.tag_flow_cmn_rec_sign
"""The key to the ignature field for the flowsheet, a common item."""
lang_dict_cmn = defs.dict_jp_part_flow_cmn
"""
Language dictionary for common parts.
    tag_flow_cmn_rec_time : part_flow_cmn_rec_time_jp,
    tag_flow_cmn_rec_sign : part_flow_cmn_rec_sign_jp
"""

#lang_dict_<this unit operation> = defs.dict_jp_part_<this unit operation>
tag_part_flow_gas_N2 = defs.opt_uo_innert_gas_N2
"""Tag for replacing gas N2 on the flowsheet"""
tag_part_flow_gas_Ar = defs.opt_uo_innert_gas_Ar
"""Tag for replacing gas argon on the flowsheet"""
tag_part_flow_gas_plchldr = defs.opt_uo_innert_gas_plchldr
"""Tag for replacing gas placeholder on the flowsheet"""
tag_part_flow_rplace_complete = "replacement_complete"
"""tag for innert gas replacement complete check-box"""
dict_jp_part_flow = [tag_part_flow_gas_N2,
                     tag_part_flow_gas_Ar,
                     tag_part_flow_gas_plchldr,
                     tag_part_flow_rplace_complete]
"""JP language dictionary for flowsheet parts for the unit operation innert gas replacement"""


tag_stc_flow_instr = "innert replacement instruction"
"""Tag for the instruction sentence for innert gas replacement, the sentence has 3 placeholders: {press}, {gas}, {rep}"""
dict_jp_stcs_instr = {tag_stc_flow_instr : "到達内圧目安:{press} MPaG, {gas}置換回数{rep}回"}
"""Instruction sentece for innert gas replacement in Japanese"""


dict_stcs_instr = dict_jp_stcs_instr
"""Instruction sentece for innert gas replacement"""



#########################################################
# Class (uo.UnitOperation, uo_name=defs.tag_uo_<UO_NAME>)
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



class InnertReplacement(uo.UnitOperation, uo_tag=defs.tag_uo_innert_replace):
    def __init__(self,
                 caller:type[trdef.UniversalTrait] = None, 
                 flowsheet:fsht.Flowsheet = None,
                 operation_seq:int = None,
                 num_subitems:int = None,
                 edit_comment:str = None):
        super().__init__(caller=caller, flowsheet=flowsheet, operation_seq=operation_seq, num_subitems=1, edit_comment=edit_comment)
        self.innert_gas:str = None
        self.neg_pressure:float = None
        self.num_repeat:int = None


    def load_params_from_df(self, df: pd.DataFrame):
        """
        Loads necessary parameters from a DataFrame object.
        The header items must be in line with the definition the class Charging.
        The header items can be passed from the get_detail_header() of each UnitOperation-drived class.
        This is the overriding mehtod in the class Charging..
        """

        first_row = df.iloc[0]
        if not pd.isna(first_row[header_precomment]):
            self.pre_comment = first_row[header_precomment]
        if not pd.isna(first_row[header_postcomment]):
            self.post_comment = first_row[header_postcomment]
        self.innert_gas = first_row[hedr_gas]
        self.neg_pressure = first_row[hedr_neg_pres]
        self.num_repeat = first_row[hedr_num_repeat]

    def get_detail_header(self) -> list[str]:
        return list_hedr

    def get_detail_option_menu(self) -> Optional[dict[str, list[str]]]:
        return dict_opt


    def get_json_schema(caller: trdef.UniversalTrait=None)->procio.Objason:
        common_schema:list = InnertReplacement.json_common()
        innert_gas = Primitive(prim_type='string',
                               key=hedr_gas,
                               description=f"Innert gas for replacement of the air in the reactor for safety and quality."
                               f"If no gas is selected, please use {opt_gas_N2} as default.",
                               enum=list_opt_gas,
                               nullable=False)
        
        neg_pressure =Primitive(prim_type='number',
                                key=hedr_neg_pres,
                                description=f"Negative pressure (MPaG) to be reached before innert gas compensation."
                                "If nor information is available, please use -0.08 MPaG as default.",
                                nullable=False)
        
        num_repeat =Primitive(prim_type='integer',
                              key=hedr_num_repeat,
                              description=f"Number of times the replacement (vaccum then compensation) is repeated."
                              "If no information is available, please use 2 as default.",
                              nullable=False)
        
        obj_schema = Objason(key=InnertReplacement.uo_tag,
                             props=common_schema+[innert_gas, neg_pressure, num_repeat],
                             description=f"Unit operation for innert gas replacement in the reactor.")
        return obj_schema        


    def load_from_json_dict(self, json_dict: dict[str, any]):
        super().load_from_json_dict(json_dict)
        self.innert_gas = json_dict[hedr_gas]
        self.neg_pressure = json_dict[hedr_neg_pres]
        self.num_repeat = json_dict[hedr_num_repeat]

    def output_unit_operation(self):
        self.flowsheet.header_organizer(op_nr=self.operation_seq, title=lang_dict_uo_titles[self.uo_tag])
        if not (self.pre_comment == None or self.pre_comment == ''):
            self.flowsheet.put_body_comments(self.pre_comment)
            self.flowsheet.linefeed()        

        instruction = dict_stcs_instr[tag_stc_flow_instr].format(press=self.neg_pressure,
                                                                    gas=dict_jp_part_flow[self.innert_gas],
                                                                    rep=self.num_repeat )
        self.flowsheet.put_line(time = lang_dict_cmn[tag_flow_cmn_rec_time],
                                content=instruction,
                                record=dict_jp_part_flow[tag_part_flow_rplace_complete],
                                operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
        self.flowsheet.linefeed()

        if not (self.post_comment == None or self.post_comment == ''):
            self.flowsheet.put_body_comments(self.post_comment)
            self.flowsheet.linefeed()