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
import flow_draw.batch.process.unit_operations.material_input as matin
from flow_draw.batch.process.unit_operations.material_input import Input
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
hedr_solvent_via:str = 'solvent_via'
"""Header item for the vessels via which the solvent is added."""




# hedr_material_name
# hedr_metrics_value
# hedr_metrics_unit'
# hedr_error_pct
# hedr_method = 'Charging_Method'
# hedr_time_control = 'Time_Control'
# hedr_time_min = 'Minimum_Time(min)'
# hedr_time_max = 'Maximum_Time(min)'
# hedr_temp_control = 'Temp_Control'
# hedr_temp_min = 'Minimum_Temp(deg-C)'
# hedr_temp_max = 'Maximum_Temp(deg-C)'


list_hedr = []


#########################################################
# UO-specific options, list, header_item: list dictionry thereof (for data input and internalsignaling)
#########################################################

opt_something:str = "something"

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

tag_part_rec_qty_input:str = "tag_input_qty"
"""The key to a flowsheet part: the input quantity of washing solvent."""
tag_part_rec_qty_lot:str = 'tag_lot'
"""The key to a flowsheet part: the lot number of the input material."""
tag_part_rec_id_balance:str = "tag_balance_id"
"""The key to a flowsheet part: the ID of the balance."""
tag_part_rec_id_cntnr:str = "tag_container_id"
"""The key to a flowsheet part: the ID of the container of the input material."""
tag_part_rec_hose:str = "tag_hose_id"
"""The key to a flowsheet part: the hose of the input material."""
tag_part_val_agit_rate_arbit:str = "tag_opt_agit_rate_arbit"
"""The key to a flowsheet part: arbitrary agitation rate."""
tag_part_unit_agit_rpm:str = "tag_unit_agit_rpm"
"""The key to a flowsheet part: rpm, an unit of agitation rate."""
tag_part_mthd_agitation:str = "tag_method_agit"
"""The key to a flowsheet part: subtitle for reslurry washing."""
tag_part_cntnt_instr_obs:str = "tag_content_instr_observation"
"""The key to a flowsheet part: instruction for observation during agitation."""
tag_part_cntnt_instr_init_agit:str = "tag_content_instr_init_agit"
"""The key to a flowsheet part: instruction to start agitation."""
tag_part_cntnt_instr_end_agit:str = "tag_content_instr_end_agit"
"""The key to a flowsheet part: instruction to stop agitation."""
tag_part_rec_rech_agit_complt:str = "tag_reach_agit_complt"
"""The key to a flowsheet part: record field component. Check box to record the completion of agitation."""


tag_stc_cntnt_instr_detail:str = "tag_stc_instr_detail"
"""The key to a flowsheet sentence template: detailed instruction. Includes place holders "{time_val}" and "{time_unit}". """
tag_stc_cntnt_agit_rate:str = "tag_stc_agit_rate"
"""The key to a flowsheet sentence template: instruction for agitation rate. Includes place holders "{rot_value}" and "{rot_unit}". """
tag_stc_rec_agit_duration:str = "tag_stc_agit_duration"
"""The key to a flowsheet sentence template: record field for agitation duration. Includes a place holder "{time_unit}". """


dict_parts_stcs_jp = {tag_part_rec_qty_input : '仕込み量__________kg',
                      tag_part_rec_qty_lot : 'ロット番号__________',
                      tag_part_rec_id_balance : '秤量器ID__________',
                      tag_part_rec_id_cntnr : '容器ID__________',
                      tag_part_rec_hose: 'フレキID__________',
                      tag_part_val_agit_rate_arbit: '現場調整',
                      tag_part_unit_agit_rpm: 'rpm',
                      tag_part_mthd_agitation : '懸濁攪拌',
                      tag_part_cntnt_instr_obs : 'FD内の状態を確認しながら操作すること',
                      tag_part_cntnt_instr_init_agit : '攪拌開始',
                      tag_part_cntnt_instr_end_agit : '攪拌終了',
                      tag_part_rec_rech_agit_complt : '□ 実施確認',
                      tag_stc_cntnt_instr_detail :'再下端まで攪拌しながら掘り下げ後{time_val}{time_unit}以上攪拌して攪拌翼を最上端まで上げて次ステップに移行する。',
                      tag_stc_cntnt_agit_rate : '攪拌数: {rot_value}{rot_unit}',
                      tag_stc_rec_agit_duration : '攪拌時間:__________{time_unit}'}

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
class Reslurry(uo.UnitOperation, uo_tag=defs.tag_uo_reslurry):
    def __init__(self,
                 caller: type[trdef.UniversalTrait] =None,
                 flowsheet:fsht.Flowsheet=None,
                 operation_seq: int=None,
                 num_subitems: int = None,
                 edit_comment:str=None):
        super().__init__(caller=caller, flowsheet=flowsheet, operation_seq=operation_seq, num_subitems=num_subitems, edit_comment=edit_comment)
        self.buffer_tank:list[str] = []
        self.arr_inputs:list[Input] = []
        self.val_time_agit:float = None
        self.unit_time_agit:str = None
        self.rpm_agit:float = None


    
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
            #<uo-specific process>
            pass



    def get_detail_header(self) -> list[str]:
        """UO-specific items only."""
        return list_hedr

    def get_detail_option_menu(self) -> Optional[dict[str, list[str]]]:
        return dict_opt
    
    @staticmethod
    def get_json_schema(caller: trdef.UniversalTrait=None)->Objason:
        common_schema = Reslurry.json_common()
        input_entry = Input.get_json_schema(caller=caller)
        arr_input = Array(key=arry_inputs_json,
                          content=input_entry,
                          description='A list of material input entries for the reslurry operation.',
                          required=True)
        


    def load_from_json_dict(self, json_dict: dict[str, any]):
        super().load_from_json_dict(json_dict)
        pass

    def output_unit_operation(self):
        self.flowsheet.header_organizer(op_nr=self.operation_seq, title=lang_dict_uo_titles[self.uo_tag])
        if not (self.pre_comment == None or self.pre_comment == ''):
            self.flowsheet.put_body_comments(self.pre_comment)
            self.flowsheet.linefeed()        

        #<Operation-specific processes here>

        if not (self.post_comment == None or self.post_comment == ''):
            self.flowsheet.put_body_comments(self.post_comment)
            self.flowsheet.linefeed()
    
    @classmethod
    def generate_test_df(cls,
                       precomment:str=None,
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
    
    @classmethod
    def add_to_test_df(cls,
                       df: pd.DataFrame=None,
                       PARAMETER=DEFALUT_VALUE)->None:
        width:int = len(df.columns)
        new_row:list[any] = [None]*width
        row:int = len(df)
        df.loc[row]=new_row
        df.at[row, HEADER_ITEM]=PARAMETER
        ...
