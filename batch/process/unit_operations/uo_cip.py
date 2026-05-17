

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
hedr_cip_tgt:str = "CIP target"
"""header item: CIP target"""
hedr_solvent:str = "Cleaning solvent"
"""header item: cleaning solvent"""
hedr_qty_kg:float = "solvent QTY"
"""header item: solvent suantity"""
hedr_via:str = "Via"
"""header item: path of the dirty solvent"""
hedr_destination:str = "Destination"
"""header item: destination of the dirty solvent"""
list_hedr = [hedr_cip_tgt,
             hedr_solvent,
             hedr_qty_kg,
             hedr_via,
             hedr_destination]
"""List of header items"""


#########################################################
# UO-specific options, list, header_item: list dictionry thereof (for data input and internalsignaling)
#########################################################

#Dictionary for options can't be composed here. It is done in get_detail_option_menu().


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

tag_flow_part_rec_method_disch= "method disch"
"""Tag for a flowsheet component: item for the method column discharge"""
flow_part_rec_method_disch_jp= "廃棄"
"""A flowsheet component:  item for the method column discharge"""

tag_flow_part_instr_disch_direct= "instruction for direct disch"
"""Tag for a flowsheet component: instruction item in the content, direct discharge"""
flow_part_instr_disch_direct_jp= "直接廃棄する。"
"""A flowsheet component: instruction item in the content, direct discharge"""

tag_flow_part_rec_input_qty= "tag rec field input qty"
"""Tag for a flowsheet component: record field for input quantity (kg)"""
flow_part_rec_input_qty_jp= "仕込み量__________kg"
"""A flowsheet component: record field for input quantity (kg) in JP"""
tag_flow_part_rec_lot_nr= "tag rec lot nr"
"""Tag for a flowsheet component: record field for the lot number of the cleaning solvent"""
flow_part_rec_lot_nr_jp= "ロット番号__________"
"""A flowsheet component: record field for the lot number of the cleaning solvent in JP"""
tag_flow_part_rec_flexhose= "tag rec hose ID"
"""Tag for a flowsheet component: record field for the flexible hose ID"""
flow_part_rec_flexhose_jp= "溶媒用フレキID__________"
"""A flowsheet component: record field for the flexible hose ID in JP"""
tag_flow_part_rec_chk_compl= "check box completion"
"""Tag for a flowsheet component: check-box for cleaning completion"""
flow_part_rec_chk_compl_jp= "□ 実施確認"
"""A flowsheet component: check-box for cleaning completion in JP"""

tag_stc_part_instr_qty= "instr stc quantity kg"
"""Tag for a sentence template: instruction for approx quantity; includes a placeholder {qty_kg}"""
stc_instr_qty_jp= "目安 {qty_kg} kg"
"""A sentence template: instruction for approx quantity; includes a placeholder {qty_kg}"""
tag_stc_part_cip_tgt= "instr CIP target"
"""Tag for a sentence template: instruction CIP target; includes a placeholder {tgt}"""
stc_cip_tgt_jp= "{tgt}に仕込む"
"""A sentence template:  includes a placeholder {tgt}"""

tag_stc_part_instr_disch_via= "instr stc disch via point"
"""Tag for a sentence template: instruction sentence to discharge through a specified point; includes placeholder {via} """
stc_rec_instr_disch_via_jp= "{via}経由で廃棄する。"
"""A sentence template: instruction sentence to discharge through a specified point; includes placeholder {via}"""

dict_flow_part_jp:dict[str, str] = {tag_flow_part_rec_method_disch : flow_part_rec_method_disch_jp,
                                     tag_flow_part_instr_disch_direct : flow_part_instr_disch_direct_jp,
                                     tag_flow_part_rec_input_qty : flow_part_rec_input_qty_jp,
                                     tag_flow_part_rec_lot_nr : flow_part_rec_lot_nr_jp,
                                     tag_flow_part_rec_flexhose : flow_part_rec_flexhose_jp,
                                     tag_flow_part_rec_chk_compl : flow_part_rec_chk_compl_jp,
                                     tag_stc_part_instr_qty : stc_instr_qty_jp,
                                     tag_stc_part_cip_tgt : stc_cip_tgt_jp,
                                     tag_stc_part_instr_disch_via : stc_rec_instr_disch_via_jp}

dict_flow_parts:dict[str, str] = dict_flow_part_jp

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
class CIP(uo.UnitOperation, uo_tag=defs.tag_uo_cip):
    def __init__(self,
                 caller: trdef.GetMats =None,
                 flowsheet:fsht.Flowsheet=None,
                 operation_seq: int=None,
                 num_subitems: int = None,
                 edit_comment:str=None):
        super().__init__(caller=caller, flowsheet=flowsheet, operation_seq=operation_seq, num_subitems=num_subitems, edit_comment=edit_comment)
        self.materials = caller.get_mats()
    
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
        for _, subitem in df.iterrows():
            pass#<uo-specific process>



    def get_detail_header(self) -> list[str]:
        return list_hedr

    def get_detail_option_menu(self) -> Optional[dict[str, list[str]]]:
        list_mats:list[str] = None
        if self.materials is not None:
            list_mats = self.materials.get_list_mats()
        else:
            raise RuntimeError(f"{self.__class__.__name__}.get_detail_option_menu(): No material daat is provided. \
                               The data is necessary to put the name of cleaning solvent. (Op. Nr. {self.operation_seq})")
        dict_option: dict[str, list[str]] = {hedr_solvent : list_mats}
        return dict_option

    
    def output_unit_operation(self):
        self.flowsheet.header_organizer(op_nr=self.operation_seq, title=lang_dict_uo_titles[self.uo_tag])
        if not (self.pre_comment == None or self.pre_comment == ''):
            self.flowsheet.put_body_comments(self.pre_comment)
            self.flowsheet.linefeed()        

        #<Operation-specific processes here>

        if not (self.post_comment == None or self.post_comment == ''):
            self.flowsheet.put_body_comments(self.post_comment)
            self.flowsheet.linefeed()

class UnitCleaning:
    def __init__(self):
        self.target:str = None
        self.mat:str = None
        self.qty_kg:float = None
        self.via:str=None
    
