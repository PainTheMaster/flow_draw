
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
hedr_precomment = defs.hedr_cmn_io_dtil_precmnt #Don't include this in the specific header list!!!
hedr_postcomment = defs.hedr_cmn_io_dtil_postcmnt #Don't include this in the specific header list!!!


#########################################################
# UO-specific hader items and list thereof
#########################################################
hedr_sop = defs.hedr_uo_lnclrnc_sop
list_hedr = defs.list_hedr_uo_lnclrnc



#########################################################
# UO-specific options, list, header_item: list dictionry thereof (for data input and internalsignaling)
#########################################################






#########################################################
# signal -> local language dictionary and tags for it
#########################################################

lang_dict_uo_titles = defs.dict_jp_part_uo_titles


#Tags for translation of common parts 
tag_flow_cmn_rec_time = defs.tag_flow_cmn_rec_time
tag_flow_cmn_rec_sign = defs.tag_flow_cmn_rec_sign
#language dictionary for common flowsheet items
lang_dict_cmn = defs.dict_jp_part_flow_cmn
"""
tag_flow_cmn_rec_time : part_flow_cmn_rec_time_jp,
tag_flow_cmn_rec_sign : part_flow_cmn_rec_sign_jp
"""

#language dictionary for lne-clearance-specific componen and keys (tags) thereof
tag_lnclrnc_compltd = defs.tag_part_flow_lnclrnc_rec_cmpltd
lang_dict_parts = defs.dict_jp_part_lnclrnce

#Language dictionary for line-clearance-specific sentence(s) with placeholder
tag_stc_instr = defs.tag_stc_flow_lnclrnc_instr
lang_dict_stcs_lnclrnc = defs.dict_jp_stcs_flow_lnclrnc



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

class LineClearance(uo.UnitOperation, uo_name=defs.tag_uo_line_clearance):
    def __init__(self,
                 caller:trdef.UniversalTrait = None,
                 flowsheet:fsht.Flowsheet  = None,
                 operation_seq:int = None,
                 num_subitems:int = None,
                 edit_comment:str = None):
        super().__init__(caller=caller, flowsheet=flowsheet, operation_seq=operation_seq, num_subitems=num_subitems, edit_comment=edit_comment)
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

    def output_unit_operation(self):
        self.flowsheet.header_organizer(op_nr=self.operation_seq, title=lang_dict_uo_titles[self.uo_name])
        if not (self.pre_comment == None or self.pre_comment == ''):
            self.flowsheet.put_body_comments(self.pre_comment)
            self.flowsheet.linefeed()

        sentence = lang_dict_stcs_lnclrnc[tag_stc_instr].format(sop=self.sop)
        self.flowsheet.put_line(time = lang_dict_cmn[tag_flow_cmn_rec_time],
                                content=sentence,
                                record=lang_dict_parts[tag_lnclrnc_compltd],
                                operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
        self.flowsheet.linefeed()

        if not (self.post_comment == None or self.post_comment == ''):
            self.flowsheet.put_body_comments(self.post_comment)
            self.flowsheet.linefeed()