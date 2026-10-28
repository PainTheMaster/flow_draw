
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
hedr_precomment = defs.hedr_cmn_io_dtil_precmnt #Don't include this in the specific header list!!!
hedr_postcomment = defs.hedr_cmn_io_dtil_postcmnt #Don't include this in the specific header list!!!


#########################################################
# UO-specific hader items and list thereof
#########################################################
hedr_sop = "SOP_title"
list_hedr = [hedr_sop]



#########################################################
# UO-specific options, list, header_item: list dictionry thereof (for data input and internalsignaling)
#########################################################

"""No UO-specific options for this unit operation."""




#########################################################
# signal -> local language dictionary and tags for it
#########################################################

lang_dict_uo_titles = defs.dict_jp_part_uo_titles
"""language dictionary for the unit operation, line clearance in this case."""

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

#language dictionary for lne-clearance-specific componen and keys (tags) thereof
tag_cntnt_check_cleaned = "content_instruction_cleaning_check"
"""Tag for a flowsheet component: instruction to check the cleaning status"""
tag_cntnt_check_items = 'content_instr_check_items'
"""Tag for a flowsheet component: check items for line clearance, e.g., unnecessary docs, records, equip, product, etc."""
tag_rec_lnclrnc_compltd = "record_checkbox_line_clearance_completed"
"""Tag for a flowsheet component: check box to record line clearance"""
tag_rec_clean_check = "record_checkbox_cleaned"
"""Tag for a flowsheet component: check box to record cleaning status"""

dict_jp_parts = {tag_cntnt_check_cleaned:'洗浄が完了していること。',
                 tag_cntnt_check_items : '他検体の文書、点検等の記録、用具、機器、製品、部品等がないことを確認する。',
                    tag_rec_lnclrnc_compltd:"□ラインクリアランス完了",
                    tag_rec_clean_check : "□洗浄済み"}

lang_dict_parts = dict_jp_parts
"""Multilingual language dictionary for fixed flowsheet components"""


#Language dictionary for line-clearance-specific sentence(s) with placeholder
tag_stc_instr = "tag_line_clearance_instruction"
"""Tag for a instruction sentence: instruction to carry out line clearance operation. Includes a placeholder {sop}."""

dict_jp_stcs_flow_lnclrnc = {tag_stc_instr : "{sop}に従ってラインクリアランスを実施する。"}

lang_dict_stcs_lnclrnc = dict_jp_stcs_flow_lnclrnc



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
# load_params_from_df(self, df: pd.DataFrame)
# output_unit_operation(self)
#
#########################################################

class LineClearance(uo.UnitOperation, uo_tag=defs.tag_uo_line_clearance):
    def __init__(self,
                 caller:trdef.UniversalTrait = None,
                 flowsheet:fsht.Flowsheet  = None,
                 operation_seq:int = None,
                 num_subitems:int = None,
                 edit_comment:str = None):
        super().__init__(caller=caller, flowsheet=flowsheet, operation_seq=operation_seq, num_subitems=1, edit_comment=edit_comment)
        self.sop:str = None

    def load_params_from_df(self, df: pd.DataFrame):
        """
        Loads necessary parameters from a DataFrame object.
        The header items must be in line with the definition the module uo_line_clearance.
        The header items can be passed from the get_detail_header() of each UnitOperation-drived class.
        This is the overriding mehtod in the class Charging..
        """

        first_row = df.iloc[0]
        if not pd.isna(first_row[hedr_precomment]):
            self.pre_comment = first_row[hedr_precomment]
        if not pd.isna(first_row[hedr_postcomment]):
            self.post_comment = first_row[hedr_postcomment]
        for _, subitem in df.iterrows():
            self.sop = subitem[hedr_sop]


    def get_detail_header(self) -> list[str]:
        return list_hedr
    
    def get_detail_option_menu(self) -> Optional[dict[str, list[str]]]:
        return None

    @staticmethod
    def get_json_schema(caller: trdef.UniversalTrait=None)->Objason:
        common_schema:list[Primitive] = LineClearance.json_common()
        sop = Primitive(prim_type = "string",
                        key=hedr_sop,
                        description='Title of the SOP document. If valid information is not provided, please put <placeholder> in the field.',
                        nullable=False)
        obj_clearance = Objason(key=LineClearance.uo_tag,
                                props=common_schema+[sop],
                                description="Unit operation for line clearance in a process workflow. This unit operation is used to instruct the line clearance before the start of production. "
                                "Please consider putting this step even if line clearance is not mentioned explicitly in the process documentation, as this activity is required on the production side.")
        return obj_clearance

    def load_from_json_dict(self, json_dict: dict[str, any]):
        super().load_from_json_dict(json_dict)
        #self.sop = json_dict.get(key=hedr_sop, default='<placeholder>')        
        self.sop = json_dict.get(hedr_sop, '<placeholder>')

    def print_unit_operation(self):
        # self.flowsheet.header_organizer(op_nr=self.operation_seq, title=lang_dict_uo_titles[self.uo_tag])
        self.flowsheet.header_organizer(title=lang_dict_uo_titles[self.uo_tag])

        if not (self.pre_comment == None or self.pre_comment == ''):
            self.flowsheet.put_body_comments(self.pre_comment)
            self.flowsheet.linefeed()

        sentence = lang_dict_stcs_lnclrnc[tag_stc_instr].format(sop=self.sop)
        self.flowsheet.put_line(time = lang_dict_cmn[tag_flow_cmn_rec_time],
                                content=sentence,
                                record=lang_dict_parts[tag_rec_lnclrnc_compltd],
                                operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
        self.flowsheet.put_line(content=lang_dict_parts[tag_cntnt_check_items])
        self.flowsheet.put_line(content=lang_dict_parts[tag_cntnt_check_cleaned],
                                record=lang_dict_parts[tag_rec_clean_check])
        
        self.flowsheet.linefeed()

        if not (self.post_comment == None or self.post_comment == ''):
            self.flowsheet.put_body_comments(self.post_comment)
            self.flowsheet.linefeed()