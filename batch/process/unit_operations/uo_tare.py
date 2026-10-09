#########################################################
# imports
#########################################################
import enum

import pandas as pd
import flow_draw.definitions as defs
import flow_draw.data_io.flowsheet as fsht
from typing import Optional
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

"""
Here, header items to hold pieces of information for the filter dryer set-up shall be placed. The following ithems have to be collected to complete the unit operation block:
-ID of the filtering equipment.
-Type/catalog code of the filter cloth.
-Number of the filter cloths.
-Type/catalog code of the bag filter.


""" 
hedr_location:str='Location'
"""Header for the taring location"""
hedr_pkg:str ="Package"
"""Header for the package information of the tare unit operation."""
hedr_num_pkg:int ="Num_Pkgs"
"""Header for the number of packages in the tare unit operation."""
list_hedr = [
    hedr_location,
    hedr_pkg,
    hedr_num_pkg
]
"""List of header items for the tare unit operation."""


#########################################################
# UO-specific options, list, header_item: list dictionry thereof (for data input and internalsignaling)
#########################################################
opt_pkg_polym_bag:str = "polymer bag"
"""Option for a polymer bag package."""
opt_pkg_pfa_bottle:str = "PFA bottle"
"""Option for a PFA bottle package."""
opt_pkg_pp_bottle:str = "PP bottle"
"""Option for a PP bottle package."""
opt_pkg_glass_bottle:str = "Glass bottle"
"""Option for a glass bottle package."""
opt_pkg_plchldr:str = "<placeholder: pkg>"
"""Placeholder for package."""

list_opt_pkg = [
    opt_pkg_polym_bag,
    opt_pkg_pfa_bottle,
    opt_pkg_pp_bottle,
    opt_pkg_glass_bottle,
    opt_pkg_plchldr
]
"""List of various packaging options for solid and liquid products/intermediates."""


dict_opt: dict[str, list[str]] = {
    hedr_pkg: list_opt_pkg
}

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

tag_part_id_balance:str = "tag_id_balance"
"""Tag for the balance ID in the tare unit operation."""
tag_stc_instr_tare:str = "tag_stc_instr_tare"
"""Tag for the tare instruction in the tare unit operation. Includes a placeholder "pkg" for the package."""
tag_stc_rec_tare:str = "tag_stc_rec_tare"
"""Tag for the tare record in the tare unit operation. Includes a placeholder "count_pkg" for the number of packages."""

dict_parts_stcs_jp:dict[str, str] = {
    opt_pkg_polym_bag: "ポリ袋",
    opt_pkg_pfa_bottle: "PFAボトル",
    opt_pkg_pp_bottle: "PPボトル",
    opt_pkg_glass_bottle: "ガラス瓶",
    opt_pkg_plchldr: "<placeholder: pkg>",
    tag_part_id_balance: "秤量器ID:_____________",
    tag_stc_instr_tare: "取り出しに用いる{pkg}の風袋を測定する。記載欄が足りなければ特記事項欄に記録する。",
    tag_stc_rec_tare: "風袋重量({count_pkg}):_____________kg",
}


dict_parts_stcs = dict_parts_stcs_jp
"""Switchable dictionary flowsheet parts and sentence templates."""


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
class Tare(uo.UnitOperation, uo_tag=defs.tag_uo_tare_pkg):
    def __init__(self,
                 caller: type[trdef.UniversalTrait] =None,
                 flowsheet:fsht.Flowsheet=None,
                 operation_seq: int=None,
                 num_subitems: int = None,
                 edit_comment:str=None):
        super().__init__(caller=caller, flowsheet=flowsheet, operation_seq=operation_seq, num_subitems=num_subitems, edit_comment=edit_comment)
        self.location:str = None
        self.pkg_material: str = None
        self.num_pkg:int = None

    
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
        #     pass
        if not pd.isna(first_row[hedr_location]):
            self.location = first_row[hedr_location]
        if not pd.isna(first_row[hedr_pkg]):
            self.pkg_material = first_row[hedr_pkg]
        if not pd.isna(first_row[hedr_num_pkg]):
            self.num_pkg = int(first_row[hedr_num_pkg])



    def get_detail_header(self) -> list[str]:
        """UO-specific items only."""
        return list_hedr

    def get_detail_option_menu(self) -> Optional[dict[str, list[str]]]:
        return dict_opt
    
    def get_json_schema(caller: trdef.UniversalTrait=None)->Objason:
        common_schema:list[Primitive] = Tare.json_common()
        pkg_location = Primitive(prim_type='string',
                                 key=hedr_location,
                                 description='Place where the pacaging material(s) is tared. E.g, an isolator. If not specified in the data source, null is acceptable.',
                                 nullable=True,
                                 required=True)
        pkg_mat = Primitive(prim_type='string',
                             key=hedr_pkg,
                             enum=list_opt_pkg,
                             description = f'Packaging material. Mandatory and non-nullable field. If no information is proviced, pelase select "{opt_pkg_plchldr}". ',
                             nullable = False,
                             required = True)
        num_pkg = Primitive(prim_type='integer',
                            key=hedr_num_pkg,
                            description='Number of packaging materials. Depending on the amount/volume of the product/intermediate and the capacity of the packaging material, '
                            'multiple pieces of mackaging materials is necessary. If no data is provided in the document, please put 1 as the default value.',
                            nullable=None,
                            required=True)
        obj_tare = Objason(key=Tare.uo_tag,
                           props=common_schema+[pkg_location, pkg_mat, num_pkg],
                           description='This object is to formulate taring operation of the packaging material for API or its intermediate. '
                           f'The content can be either liquid or solid. Normally, this operation is needed just before an instance of "{defs.tag_uo_prod_disch}".',
                           required=True,
                           nullable=False)
        return obj_tare

    def load_from_json_dict(self, json_dict: dict[str, any]):
        super().load_from_json_dict(json_dict)
        self.location = json_dict.get(hedr_location, None)
        self.pkg_material = json_dict.get(hedr_pkg, '<placeholder: pkg material>')
        self.num_pkg = json_dict.get(hedr_num_pkg, 1)


    def output_unit_operation(self):
        self.flowsheet.header_organizer(op_nr=self.operation_seq, title=lang_dict_uo_titles[self.uo_tag])
        if not (self.pre_comment == None or self.pre_comment == ''):
            self.flowsheet.put_body_comments(self.pre_comment)
            self.flowsheet.linefeed()

        if self.location is not None:
            self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                    method=self.location,
                                    content=dict_parts_stcs[tag_stc_instr_tare].format(pkg=self.pkg_material),
                                    record=dict_parts_stcs[tag_part_id_balance],
                                    operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    witness=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    )
        else:
            self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                    method='',
                                    content=self.dict_parts_stcs[tag_stc_instr_tare].format(pkg=self.pkg_material),
                                    record=dict_parts_stcs[tag_part_id_balance],
                                    operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    witness=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    )
        for i in range(1, self.num_pkg+1):
            self.flowsheet.put_line(record=dict_parts_stcs[tag_stc_rec_tare].format(count_pkg=i))

        self.flowsheet.linefeed()

        if not (self.post_comment == None or self.post_comment == ''):
            self.flowsheet.put_body_comments(self.post_comment)
            self.flowsheet.linefeed()
    
    @classmethod
    def generate_test_df(cls,
                         precomment='',
                         pkg_location="isolator",
                         pkg_material=dict_parts_stcs[opt_pkg_polym_bag],
                         num_pkg=1,
                         postcomment='')->pd.DataFrame:
        hedr:list[str] = defs.list_hedr_cmn_io_dtil + list_hedr
        content: list[any] = [None]*len(hedr)
        s:pd.Series = pd.Series(data=content, index=hedr)
        df = s.to_frame().T
        df.at[df.index[0], hedr_precomment]=precomment
        df.at[df.index[0], hedr_location]=pkg_location
        df.at[df.index[0], hedr_pkg]=pkg_material
        df.at[df.index[0], hedr_num_pkg]=num_pkg
        df.at[df.index[0], hedr_postcomment]=postcomment

        return df
    
    @classmethod
    def add_to_test_df(cls,
                       df: pd.DataFrame=None,
                       precomment='',
                       pkg_location="isolator",
                       pkg_material=dict_parts_stcs[opt_pkg_polym_bag],
                       num_pkg=1,
                       postcomment='')->None:
        width:int = len(df.columns)
        new_row:list[any] = [None]*width
        row:int = len(df)
        df.loc[row]=new_row
        df.at[row, hedr_precomment]=precomment
        df.at[row, hedr_location]=pkg_location
        df.at[row, hedr_pkg]=pkg_material
        df.at[row, hedr_num_pkg]=num_pkg
        df.at[row, hedr_postcomment]=postcomment
