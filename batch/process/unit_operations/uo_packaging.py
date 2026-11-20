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

key_name_division = 'Subdivision_name'
"""Key to the name of subdivision"""
key_cat_division = 'Subdivision_category'
"""Key to the category of subdivision"""
key_pkg_division = 'Packaging_material'
"""Key to the packaging material of a division"""
key_arr_pkg_division = 'Array_packaging_material'
"""Key to the array of packaging material of a division"""
key_val_qty_division = 'Subdivision_quantity_value'
"""Key to the quantity value of a division"""
key_unit_qty_division = 'Subdivision_quantity_unit'
"""Key to the quantity unit of a division"""
key_single_division = 'Single_subdivision'
"""Key to an object for a single subdivision."""
key_arr_division = 'Array_of_subdivisions'
"""Key to an array of subdivision objects"""
key_obj_dispens_op = 'Dispensing'

list_hedr = []


#########################################################
# UO-specific options, list, header_item: list dictionry thereof (for data input and internalsignaling)
#########################################################

opt_cat_sample = 'category_sample'
"""Option for division category: sample"""
opt_cat_bulk = 'category_bulk'
"""Option for division category: bulk"""
list_opt_cat = [opt_cat_sample,
                opt_cat_bulk]
"""List of options for category"""


opt_pkg_PE_bag:str = "Polyethylen bag"
"""Option for a polymer bag package."""
opt_pkg_Al_bag:str = "Aluminum laminate heat-sealing bag"
"""Option for a aluminium laminate bag."""
opt_pkg_polym_bottle = 'Polymer bottle'
opt_pkg_pfa_bottle:str = "PFA bottle"
"""Option for a PFA bottle package."""
opt_pkg_pp_bottle:str = "PP bottle"
"""Option for a PP bottle package."""
opt_pkg_glass_bottle:str = "Glass bottle"
"""Option for a glass bottle package."""
opt_pkg_plchldr:str = "<placeholder: pkg>"
"""Placeholder for package."""

list_opt_pkg = [
    opt_pkg_PE_bag,
    opt_pkg_Al_bag,
    opt_pkg_pfa_bottle,
    opt_pkg_pp_bottle,
    opt_pkg_polym_bottle,
    opt_pkg_glass_bottle,
    opt_pkg_plchldr
]

list_opt_something = []

dict_opt: dict[str, list[str]]={}

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

tag_part_something:str = "tag_part_something"

tag_stc_something:str = "tag_stc_something"

dict_parts_stcs_jp = {}

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
class Packaging(uo.UnitOperation, uo_tag=defs.tag_uo_packaging):
    def __init__(self,
                 caller: type[trdef.UniversalTrait] =None,
                 flowsheet:trdef.FlowsheetTrait=None,
                 operation_seq: int=None,
                 num_subitems: int = None,
                 edit_comment:str=None):
        super().__init__(caller=caller, flowsheet=flowsheet, operation_seq=operation_seq, num_subitems=num_subitems, edit_comment=edit_comment)
        self.list_samples = []
    
    def load_params_from_df(self, df: pd.DataFrame):
        """
        Loads necessary parameters from a DataFrame object.
        The header items must be in line with the definition the class Charging.
        The header items can be passed from the get_detail_header() of each UnitOperation-drived class.
        This is the overriding mehtod in the class Charging..
        """

        pass
            



    def get_detail_header(self) -> list[str]:
        """UO-specific items only."""
        return list_hedr

    def get_detail_option_menu(self) -> Optional[dict[str, list[str]]]:
        return dict_opt

    @staticmethod
    def get_json_schema(caller: trdef.UniversalTrait=None)->Objason:
        common_schema:list[Primitive] = Packaging.json_common()

        json_name_div = Primitive(prim_type='string',
                                  key=key_name_division,
                                  description='Name of the division. E.g., バルク (bulk), ユーステスト用 (use test), プロセス研究用 (for process development lab), 製剤開発用 (for formulation trial), etc.')
        json_category_div = Primitive(prim_type='string',
                                      key=key_cat_division,
                                      enum=list_opt_cat,
                                      description='Property for division categories.\n'
                                      f'"{opt_cat_sample}": Dispensing for a sample. Normally, small protion in the order of grams.\n'
                                      f'"{opt_cat_bulk}": Dispensing as bulk. Normally, in the order of kilo-grams.')
        json_pkg_material = Primitive(prim_type='string',
                                      key=key_pkg_division,
                                      enum=list_opt_pkg,
                                      description='Packaging type of the division.\n'
                                      f'"{opt_pkg_PE_bag}": Polyethlen bag. Suitable for bulk.\n'
                                      f'"{opt_pkg_Al_bag}": Aluminium laminated heat-sealing laminate bag. Good to protect the product from the environment (moisture and oxygen). '
                                      f'Normally for secondary or tertially packaging. The internal packaging should be "{opt_pkg_PE_bag}" or bottles.\n'
                                      f'"{opt_pkg_pfa_bottle}": Fluorinated plolymer bottle. Suitable for a smaller portion. Air-tight and good to protect the product from the environment. '
                                      'Chemically stable and resistant to various content.\n'
                                      f'"{opt_pkg_pp_bottle}": Polypropylen bottle. Suitable for a smaller portion. Air-tight and good to protect the product from the environment.\n'
                                      f'"{opt_pkg_polym_bottle}": Polymer bottle. Air-tight and good to protect product from the environment. Material of construct is not specified. '
                                      'Normally, this is sufficient if a non-glass bottle is required. Air-tight and good to protect the product from the environment.\n'
                                      f'"{opt_pkg_glass_bottle}": Glass bottle. Air-tight and good to protect the product from the environment.\n'
                                      f'"{opt_pkg_plchldr}": Placeholder for packaging material. If the suitable one cannot be specified from the given information, please select this.\n',)
                                      
        json_arr_pkg_material = Array(key=key_arr_pkg_division,
                                      content=json_pkg_material,
                                      description='An array of packaging material(s). In many cases, an API or its intermediates are packaged with multiple layers of protection. '
                                      'For example, when a PE bag is the primary layer (inner-most package), it will be contained in another PE bag. '
                                      'Additionally, often an aluminium-laminated bag protects the from ambient oxygen and moisture as the outer-most layer. '
                                      'Even bottles are sometimes contained in a aluminium-laminated bag for long-term stability. '
                                      'Please follow the instruction document. Please put the packaging material from the inner layer. ',
                                      required = False,
                                      nullable = True)
        json_val_qty_div = Primitive(prim_type='number',
                                     key=key_val_qty_division,
                                     description='Quantity value of a single package. The unit is spcified separately. ',
                                     nullable=False,
                                     required=True)
        json_unit_val_div = Primitive(prim_type='string',
                                      key=key_unit_qty_division,
                                      description='Quantity value of a singe package. The value is specified separately. ',
                                      nullable=False,
                                      required=True)
        json_single_div = Objason(key=key_single_division,
                                  props=[json_name_div, json_category_div, json_arr_pkg_material, json_val_qty_div, json_unit_val_div],
                                  description='A single subdivision of the product of the process. A subdivision object shall hold:\n'
                                  '- Name\n- Category\n- Array (layers) of packaging materials\n- Quantity value of the subdivision\n- Quantity unit of the subdivision.')
        arr_divs = Array(key=key_arr_division,
                         content=json_single_div,
                         description='An array of objects for subdivisions of the product. From a bulk of intermediate or active pharmaceutical ingredients, '
                         'multiple samples and subdivided bulks can be taken.')
        json_dispensing_operation = Objason(key=Packaging.uo_tag,
                                            props=common_schema+[arr_divs],
                                            description='An operation of subdivision (dispensing) of the product or intermediates and packaging thereof.'
                                            required=False)
        return json_dispensing_operation
        
                                        

    def load_from_json_dict(self, json_dict: dict[str, Any]):
        super().load_from_json_dict(json_dict)
        pass

    def print_unit_operation(self):
        self.flowsheet.header_organizer(op_nr=self.operation_seq, title=lang_dict_uo_titles[self.uo_tag])
        if not (self.pre_comment == None or self.pre_comment == ''):
            self.flowsheet.put_body_comments(self.pre_comment)
            self.flowsheet.linefeed()        

        #<Operation-specific processes here>

        if not (self.post_comment == None or self.post_comment == ''):
            self.flowsheet.put_body_comments(self.post_comment)
            self.flowsheet.linefeed()
    
    @staticmethod
    def generate_test_df(precomment:str=None,
                         postcomment:str=None, 
                         PARAMETER=DEFALUT_VALUE)->pd.DataFrame:
        hedr:list[str] = defs.list_hedr_cmn_io_dtil + list_hedr
        content: list[any] = [None]*len(hedr)
        s:pd.Series = pd.Series(data=content, index=hedr)
        df = s.to_frame().T
        df.at[df.index[0], hedr_precomment] = precomment
        df.at[df.index[0], hedr_postcomment] = postcomment
        df.at[df.index[0], HEDR_ITEM]=PARAMETER
        ...

        return df
    
    @staticmethod
    def add_to_test_df(df: pd.DataFrame=None,
                       PARAMETER=DEFALUT_VALUE)->None:
        width:int = len(df.columns)
        new_row:list[any] = [None]*width
        row:int = len(df)
        df.loc[row]=new_row
        df.at[row, HEADER_ITEM]=PARAMETER
        ...

class Dividions:
    def __init__(self):
        self.name:str = ''
        self.pkg_material:str = ''
        self.qty:float = ''
