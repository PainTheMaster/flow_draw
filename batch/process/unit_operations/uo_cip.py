

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
#from flow_draw.data_io import json_io
from flow_draw.data_io import json_io
from flow_draw.data_io.json_io import JsonEntity, Array, Objason, Primitive
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
hedr_cip_tgt:str = "CIP_target"
"""header item: CIP target"""
hedr_solvent:str = "Cleaning_solvent"
"""header item: cleaning solvent"""
hedr_qty_kg:float = "solvent_QTY_(kg)"
"""header item: solvent suantity"""
hedr_via:str = "Via"
"""header item: path of the dirty solvent"""
# hedr_destination:str = "Destination"
# """header item: destination of the dirty solvent"""
list_hedr = [hedr_cip_tgt,
             hedr_solvent,
             hedr_qty_kg,
             hedr_via]
            #  hedr_destination]
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

tag_flow_part_solv_qty_arbit="instruction for arbitray solvent quantity"
"""Tag for a flowsheet component: instruction for an arbitrary solvent quantity"""
flow_part_solv_qty_arbit_jp="溶媒量現場調整"
"""A flowsheet component: instruction for an arbitrary solvent quantity"""

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
stc_instr_qty_jp= "溶媒量目安 {qty_kg} kg"
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
                                    tag_flow_part_solv_qty_arbit : flow_part_solv_qty_arbit_jp,
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
        self.cip_operations:list[UnitCleaning]=[]
    
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
            self.cip_operations.append(UnitCleaning(caller=self, sheet=self.flowsheet, ser_cip=subitem))


    def get_json_schema(caller:trdef.UniversalTrait = None)->json_io.Objason:
        # list_cmn = Agitation.json_common(arg_name_uo=Agitation.uo_tag)
        list_cmn = CIP.json_common()
        cip_tgt = Primitive(prim_type="string",
                            key=hedr_cip_tgt,
                            description='Target of CIP (cleaning in place), e.g., reaction vessel, tank, filter dryer, etc.',
                            required=True)
        cip_solvent = Primitive(prim_type='string',
                                key=hedr_solvent,
                                description='Solvent for CIP.',
                                required=True)
        cip_qty = Primitive(prim_type="number",
                            key=hedr_qty_kg,
                            description='Quantity of the solvent in kg for cleaning in place.',
                            required=False)
        cip_via = Primitive(prim_type='string',
                            key=hedr_via,
                            description='Transit point of the cleaning liquid. Optional',
                            required=False)
        json_cip = Objason(#key=defs.tag_uo_cip,
                           key=CIP.uo_tag,
                           props=list_cmn+[cip_tgt, cip_solvent, cip_qty, cip_via],
                           description='This is object for cleaning in place (CIP) during the process. '\
                            'CIP is done to carry out the process with limited number of pieces of equipment by avoiding contamination.'\
                            'Please work with this object if the given process flow explicitly indicates the need for CIP.')
        return json_cip


    def get_detail_header(self) -> list[str]:
        return list_hedr

    def get_detail_option_menu(self) -> Optional[dict[str, list[str]]]:
        list_mats:list[str] = None
        if self.materials is not None:
            list_mats = self.materials.get_list_mats()
        else:
            raise RuntimeError(f"{self.__class__.__name__}.get_detail_option_menu(): No material data is provided. \
                               The data is necessary to put the name of cleaning solvent. (Op. Nr. {self.operation_seq})")
        dict_option: dict[str, list[str]] = {hedr_solvent : list_mats}
        return dict_option

    
    def output_unit_operation(self):
        self.flowsheet.header_organizer(op_nr=self.operation_seq, title=lang_dict_uo_titles[self.uo_tag])
        if not (self.pre_comment == None or self.pre_comment == ''):
            self.flowsheet.put_body_comments(self.pre_comment)
            self.flowsheet.linefeed()        

        for unit_cln in self.cip_operations:
            unit_cln.put_unit_cleaning()
            self.flowsheet.linefeed()

        if not (self.post_comment == None or self.post_comment == ''):
            self.flowsheet.put_body_comments(self.post_comment)
            self.flowsheet.linefeed()

    @classmethod
    def generate_test_df(cls,
                       precomment:str=None,
                       postcomment:str=None,
                       cip_tgt:str=None,
                       solvent:str=None,
                       qty_kg:float=None,
                       via:str=None)->pd.DataFrame:
        hedr:list[str] = defs.list_hedr_cmn_io_dtil + list_hedr
        content: list[any] = [None]*len(hedr)
        s:pd.Series = pd.Series(data=content, index=hedr)
        df = s.to_frame().T
        df.at[df.index[0], hedr_precomment]=precomment
        df.at[df.index[0], hedr_postcomment]=postcomment
        df.at[df.index[0], hedr_cip_tgt]=cip_tgt
        df.at[df.index[0], hedr_solvent]=solvent
        df.at[df.index[0], hedr_qty_kg]=qty_kg
        df.at[df.index[0], hedr_via]=via

        return df
    
    @classmethod
    def add_to_test_df(cls,
                       df: pd.DataFrame=None,
                       precomment:str=None,
                       postcomment:str=None,
                       cip_tgt:str=None,
                       solvent:str=None,
                       qty_kg:float=None,
                       via:str=None)->None:
        width:int = len(df.columns)
        new_row:list[any] = [None]*width
        row:int = len(df)
        df.loc[row]=new_row
        df.at[row, hedr_precomment]=precomment
        df.at[row, hedr_postcomment]=postcomment
        df.at[row, hedr_cip_tgt]=cip_tgt
        df.at[row, hedr_solvent]=solvent
        df.at[row, hedr_qty_kg]=qty_kg
        df.at[row, hedr_via]=via


class UnitCleaning:
    def __init__(self, caller:trdef.UniversalTrait=None, sheet:fsht.Flowsheet=None, ser_cip:pd.Series=None):
        self.flowsheet:fsht.Flowsheet = sheet
        self.target:str = None
        self.solvent:str = None
        self.qty_kg:float = None
        self.via:str = None
        #self.destination:str = None

        if not pd.isna(ser_cip[hedr_cip_tgt]):
            self.target = ser_cip[hedr_cip_tgt]
        else:
            raise ValueError(f"Op. Seq. {caller.operation_seq}, {caller.__class__.__name__}: No cleaning target provided.")
        
        if not pd.isna(ser_cip[hedr_solvent]):
            self.solvent = ser_cip[hedr_solvent]
        else:
            raise ValueError(f"Op. Seq. {caller.operation_seq}, {caller.__class__.__name__}: No cleaning solvent provided.")
        
        if not pd.isna(ser_cip[hedr_qty_kg]):
            self.qty_kg = ser_cip[hedr_qty_kg]
        
        if not pd.isna(ser_cip[hedr_via]):
            self.via = ser_cip[hedr_via]

        # if not pd.isna(ser_cip[hedr_destination]):
        #     self.destination = ser_cip[hedr_destination]
    
    def put_unit_cleaning(self):
        self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                method=self.target,
                                content=self.solvent,
                                record=dict_flow_parts[tag_flow_part_rec_input_qty],
                                operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
        sentence_solv:str = None
        if self.qty_kg is not None:
            sentence_solv = dict_flow_parts[tag_stc_part_instr_qty].format(qty_kg=self.qty_kg)
        else:
            sentence_solv = dict_flow_parts[tag_flow_part_solv_qty_arbit]
        self.flowsheet.put_line(content=sentence_solv,
                                record=dict_flow_parts[tag_flow_part_rec_lot_nr])
        
        sentence_tgt:str = dict_flow_parts[tag_stc_part_cip_tgt].format(tgt=self.target)
        self.flowsheet.put_line(content=sentence_tgt,
                                record=dict_flow_parts[tag_flow_part_rec_flexhose])
        sentence_path:str = None
        if self.via is not None:
            sentence_path = dict_flow_parts[tag_stc_part_instr_disch_via].format(via=self.via)
        else:
            sentence_path = dict_flow_parts[tag_flow_part_instr_disch_direct]
        self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                method=dict_flow_parts[tag_flow_part_rec_method_disch],
                                content=sentence_path,
                                record=dict_flow_parts[tag_flow_part_rec_chk_compl],
                                operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
        

    
