#########################################################
# imports
#########################################################
import pandas as pd
import flow_draw.definitions as defs
import flow_draw.data_io.flowsheet as fsht
from typing import Optional, Literal
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

hedr_equip = "Equipment"
"""Header item for filtration equipment, e.g., filte dryer, buchner filter, etc."""
hedr_filter_cloth = "Filter_cloth_type"
"""Header item for filter cloth type"""
hedr_num_filter = "Number_cloth"
"""Header item for number of filter cloth"""
hedr_bag_filter = "Bag_filter_type"
"""Header item for bag filter type"""
hedr_press_leak_test="App_press_leak_test"
"""Hedr item for applied pressure for leak test"""
hedr_press_drop_leak_test="Permiss_press_leak_test"
"""Hedr item for permissible pressure drop during the leak test"""
hedr_time_leak_test="Time_leak_test"
"""Hedr item for duration of the leak test"""
hedr_press_unit="Pressure_unit"
"""Hedr item for the pressure unit"""
list_hedr:list[str]=[hedr_equip,
                     hedr_filter_cloth,
                     hedr_num_filter,
                     hedr_bag_filter,
                     hedr_press_leak_test,
                     hedr_press_drop_leak_test,
                     hedr_time_leak_test,
                     hedr_press_unit]
"""List of header items"""


#########################################################
# UO-specific options, list, header_item: list dictionry thereof (for data input and internalsignaling)
#########################################################

list_opt_press_unit: list[str] = [defs.opt_press_kPa, defs.opt_press_MPa]

dict_opt = {hedr_press_unit: list_opt_press_unit}


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
tag_part_flow_title_filt_setup:str = "title_filt_setup"
"""Tag for the title of the filter dryer set-up unit operation"""
part_flow_title_filt_setup_jp:str = "ろ過準備"
"""A flowsheet compoenent for the title of the filter dryer set-up unit operation, in JP"""

tag_part_flow_instr_prep:str = "instr_prep"
"""Tag for the instruction for the filter dryer set-up unit operation"""
part_flow_instr_prep_jp:str = "準備"
"""A flowsheet component for the instruction for the filter dryer set-up unit operation, in JP"""

tag_part_flow_instr_leak_test:str = "instr_leak_test"
"""Tag for the instruction for the filter dryer set-up unit operation: leak test"""
part_flow_instr_leak_test_jp:str = "気密確認"
"""A flowsheet component for the instruction for the filter dryer set-up unit operation: leak test, in JP"""

tag_flow_content_chrono_rec:str = "content_chrono_rec"
"""Tag for the instruction comment: make a chronological record of the operation"""
part_flow_content_chrono_rec_jp:str = "*作業詳細は経時的な作業記録に記載すること"
"""A flowsheet component for the instruction comment: make a chronological record of the operation, in JP"""

tag_flow_content_gas_exhaust:str = "content_gas_exhaust"
"""Tag for the instruction comment: exhaust the gas from the waste liquor tank"""
part_flow_content_gas_exhaust_jp:str = "*WGはろ布の浮き上がり防止の為ろ過液タンク側を開とすること"
"""A flowsheet component for the instruction comment: exhaust the gas from the waste liquor tank, in JP"""

tag_flow_rec_lot_cloth:str = "rec_lot_filter_cloth"
"""Tag for a flowsheet component: lot number of the filter cloth"""
part_flow_rec_lot_cloth_jp:str = "ロット番号:____________"
"""A flowsheet component for the lot number of the filter cloth, in JP"""

tag_flow_rec_num_cloth:str = "rec_num_filter_cloth"
"""Tag for a flowsheet component: number of the filter cloth"""
part_flow_rec_num_cloth_jp:str = "ろ布:_______枚"
"""A flowsheet component for the number of the filter cloth, in JP"""

tag_flow_rec_leak_test_result:str = "rec_leak_test_result"
"""Tag for a flowsheet component: result of the leak test"""
part_flow_rec_leak_test_result_jp:str = "判定: 適 / 不適"
"""A flowsheet component for the result of the leak test, in JP"""


tag_stc_flow_equip_id:str = "stc_equip_id"
"""Tag for the text template for the equipment ID: includes a placeholder {equip_id}"""
stc_flow_equip_id_jp:str = "ろ過乾燥機{equip_id}"
"""Text template to designate the equipment."""

tag_stc_flow_filter_cloth:str = "stc_filter_cloth"
"""Tag for the text template for the filter cloth type: includes a placeholder {filter_type}"""
stc_flow_filter_cloth_jp:str = "ろ布:{filter_type}"
"""Text template to designate the filter cloth type.""" 

tag_stc_num_filter_cloth:str = "stc_num_filter_cloth"
"""Tag for the text template for the number of filter cloths: includes a placeholder {num}"""
stc_num_filter_cloth_jp:str = "ろ布枚数:{num}枚"
"""Text template to designate the number of filter cloths."""

tag_stc_bag_filter:str = "stc_bag_filter"
"""Tag for the text template for the bag filter type: includes a placeholder {bag_filter_type}"""
stc_bag_filter_jp:str = "バグフィルター:{bag_filter_type}"
"""Text template to designate the bag filter type."""

tag_stc_press_leak_test:str = "stc_press_leak_test"
"""Tag for the text template for the applied pressure for leak test: includes a placeholder {press_appl}, {press_unit},{time}, and {press_drop}"""
stc_flow_press_leak_test_jp:str = "{press_appl}{press_unit}に加圧し、{time}分間で{press_drop}{press_unit}以上の圧力降下がないことを確認する。"
"""Text template to designate the applied pressure for leak test."""


dict_flow_part_jp ={tag_part_flow_title_filt_setup : part_flow_title_filt_setup_jp,
                    tag_part_flow_instr_prep : part_flow_instr_prep_jp,
                    tag_part_flow_instr_leak_test : part_flow_instr_leak_test_jp,
                    tag_flow_content_chrono_rec : part_flow_content_chrono_rec_jp,
                    tag_flow_content_gas_exhaust : part_flow_content_gas_exhaust_jp,
                    tag_flow_rec_lot_cloth : part_flow_rec_lot_cloth_jp,
                    tag_flow_rec_num_cloth : part_flow_rec_num_cloth_jp,
                    tag_flow_rec_leak_test_result : part_flow_rec_leak_test_result_jp,
                    tag_stc_flow_equip_id : stc_flow_equip_id_jp,
                    tag_stc_flow_filter_cloth : stc_flow_filter_cloth_jp,
                    tag_stc_num_filter_cloth : stc_num_filter_cloth_jp,
                    tag_stc_bag_filter : stc_bag_filter_jp,
                    tag_stc_press_leak_test : stc_flow_press_leak_test_jp}

dict_flow_part = dict_flow_part_jp
"""Local language dictionary for flowsheet parts of the filter set-up operation."""

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
class FiltSetup(uo.UnitOperation, uo_tag=defs.tag_uo_filt_setup):
    def __init__(self,
                 caller: type[trdef.UniversalTrait] =None,
                 flowsheet:fsht.Flowsheet=None,
                 operation_seq: int=None,
                 num_subitems: int = None,
                 edit_comment:str=None):
        super().__init__(caller=caller, flowsheet=flowsheet, operation_seq=operation_seq, num_subitems=num_subitems, edit_comment=edit_comment)
        self.equip_id:str = None
        """Filtration equipment ID"""
        self.filter_cloth_type:str = None
        """Filter cloth type"""
        self.num_filter_cloths:int = None
        """Number of filter cloths"""
        self.bag_filter_type:str = None
        """Bag filter type"""
        self.press_leak_test:float = None
        """Applied pressure for leak test"""
        self.press_drop_leak_test:float = None
        """Permissible pressure drop during the leak test"""
        self.time_leak_test:float = None
        """Duration of the leak test"""
        self.unit_press:str = None
        """Unit for the leak test pressure"""
    
    def load_params_from_df(self, df: pd.DataFrame):
        """
        Loads necessary parameters from a DataFrame object.
        The header items must be in line with the definition the class Charging.
        The header items can be passed from the get_detail_header() of each UnitOperation-drived class.
        """

        first_row = df.iloc[0]
        if not pd.isna(first_row[hedr_precomment]):
            self.pre_comment = first_row[hedr_precomment]
        if not pd.isna(first_row[hedr_postcomment]):
            self.post_comment = first_row[hedr_postcomment]
        if not pd.isna(first_row[hedr_equip]):
            self.equip_id = first_row[hedr_equip]
        if not pd.isna(first_row[hedr_filter_cloth]):
            self.filter_cloth_type = first_row[hedr_filter_cloth]
        if not pd.isna(first_row[hedr_num_filter]):
            self.num_filter_cloths = first_row[hedr_num_filter]
        if not pd.isna(first_row[hedr_bag_filter]):
            self.bag_filter_type = first_row[hedr_bag_filter]
        if not pd.isna(first_row[hedr_press_leak_test]):
            self.press_leak_test = first_row[hedr_press_leak_test]
        if not pd.isna(first_row[hedr_press_drop_leak_test]):
            self.press_drop_leak_test = first_row[hedr_press_drop_leak_test]
        if not pd.isna(first_row[hedr_time_leak_test]):
            self.time_leak_test = first_row[hedr_time_leak_test]
        if not pd.isna(first_row[hedr_press_unit]):
            self.unit_press = first_row[hedr_press_unit]



    def get_detail_header(self) -> list[str]:
        return list_hedr

    def get_detail_option_menu(self) -> Optional[dict[str, list[str]]]:
        return dict_opt
    

    def get_json_schema(caller: trdef.UniversalTrait=None)->Objason:
        pass


    def load_from_json_dict(self, json_dict: dict[str, any]):
        pass



    def output_unit_operation(self):
        self.flowsheet.header_organizer(op_nr=self.operation_seq, title=lang_dict_uo_titles[self.uo_tag])
        if not (self.pre_comment == None or self.pre_comment == ''):
            self.flowsheet.put_body_comments(self.pre_comment)
            self.flowsheet.linefeed()
        self.flowsheet.put_line(content=dict_flow_part[tag_flow_content_chrono_rec])
        self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                method=dict_flow_part[tag_stc_flow_equip_id].format(equip_id=self.equip_id),
                                content=dict_flow_part[tag_stc_flow_filter_cloth].format(filter_type=self.filter_cloth_type),
                                record=dict_flow_part[tag_flow_rec_lot_cloth],
                                operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
        self.flowsheet.put_line(method=dict_flow_part[tag_part_flow_instr_prep],
                                content=dict_flow_part[tag_stc_num_filter_cloth].format(num=self.num_filter_cloths),
                                record=dict_flow_part[tag_flow_rec_num_cloth])
        self.flowsheet.put_line(content=dict_flow_part[tag_stc_bag_filter].format(bag_filter_type=self.bag_filter_type))
        self.flowsheet.linefeed()
        self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                method=dict_flow_part[tag_part_flow_instr_leak_test],
                                content=dict_flow_part[tag_stc_press_leak_test].format(press_appl=self.press_leak_test,
                                                                                       press_unit=self.unit_press,
                                                                                       time=self.time_leak_test,
                                                                                       press_drop=self.press_drop_leak_test),
                                record=dict_flow_part[tag_flow_rec_leak_test_result],
                                operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
        self.flowsheet.put_line(content=dict_flow_part[tag_flow_content_gas_exhaust])
        self.flowsheet.linefeed()

        if not (self.post_comment == None or self.post_comment == ''):
            self.flowsheet.put_body_comments(self.post_comment)
            self.flowsheet.linefeed()
    
    @classmethod
    def generate_test_df(cls,
                         equip_id:str=None,
                         filt_cloth:str=None,
                         num_cloth:int=None,
                         bag_filter:str=None,
                         press_leak_test:float=None,
                         press_drop_leak_test:float=None,
                         time_leak_test:float=None,
                         unit_press:Literal['kPa', 'MPa', None]= None)->pd.DataFrame:
        hedr:list[str] = defs.list_hedr_cmn_io_dtil + list_hedr
        content: list[any] = [None]*len(hedr)
        s:pd.Series = pd.Series(data=content, index=hedr)
        df = s.to_frame().T
        df.at[df.index[0], hedr_equip]=equip_id
        df.at[df.index[0], hedr_filter_cloth]=filt_cloth
        df.at[df.index[0], hedr_num_filter]=num_cloth
        df.at[df.index[0], hedr_bag_filter]=bag_filter
        df.at[df.index[0], hedr_press_leak_test]=press_leak_test
        df.at[df.index[0], hedr_press_drop_leak_test]=press_drop_leak_test
        df.at[df.index[0], hedr_time_leak_test]=time_leak_test
        df.at[df.index[0], hedr_press_unit]=unit_press

        return df
    
    @classmethod
    def add_to_test_df(cls,
                       df: pd.DataFrame=None,
                       equip_id:str=None,
                       filt_cloth:str=None,
                       num_cloth:int=None,
                       bag_filter:str=None,
                       press_leak_test:float=None,
                       press_drop_leak_test:float=None,)->None:
        width:int = len(df.columns)
        new_row:list[any] = [None]*width
        row:int = len(df)
        df.loc[row]=new_row
        df.at[row, hedr_equip]=equip_id
        df.at[row, hedr_filter_cloth]=filt_cloth
        df.at[row, hedr_num_filter]=num_cloth
        df.at[row, hedr_bag_filter]=bag_filter
        df.at[row, hedr_press_leak_test]=press_leak_test
        df.at[row, hedr_press_drop_leak_test]=press_drop_leak_test

    
