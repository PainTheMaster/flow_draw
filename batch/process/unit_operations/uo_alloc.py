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

hedr_cell = "operation_cell"
"""
Tag for an element operation cell (room).
"""

hedr_op_resource = "operation_resource"
"""
Tag for an element operation resource such as reactor, filter dryer, mill, etc.
"""


#########################################################
# UO-specific options, list, header_item: list dictionry thereof (for data input and internalsignaling)
#########################################################






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
class Alloc(uo.UnitOperation, uo_tag=defs.tag_uo_alloc):
    def __init__(self,
                 caller: type[trdef.UniversalTrait] =None,
                 flowsheet:fsht.Flowsheet=None,
                 operation_seq: int=None,
                 num_subitems: int = None,
                 edit_comment:str=None):
        super().__init__(caller=caller, flowsheet=flowsheet, operation_seq=operation_seq, num_subitems=num_subitems, edit_comment=edit_comment)
        self.prod_cell:str = None
        self.op_resouce:str = None
    
    def load_params_from_df(self, df: pd.DataFrame):
        """
        Loads necessary parameters from a DataFrame object.
        The header items must be in line with the definition the class Charging.
        The header items can be passed from the get_detail_header() of each UnitOperation-drived class.
        This is the overriding mehtod in the class Charging..
        """

        #TODO: Implement me!
        
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
        pass

    def get_detail_option_menu(self) -> Optional[dict[str, list[str]]]:
        pass
    
    def get_json_schema(caller: trdef.UniversalTrait=None)->Objason:
        common_schema:list[Primitive] = Alloc.json_common()
        prim_prod_cell = Primitive(prim_type='string',
                              key=hedr_cell,
                              description='A property to specify a production cell (room) in a chemical plant. '
                              'If no information is provided in the document or from the user, please put "<placeholder: location>".')
        prim_op_resource = Primitive(prim_type='string',
                                key=hedr_op_resource,
                                description='A property to specify an operation resoruce, such as a reactor, filter dryer, jet mill, etc. I.e., equipment. '
                                'If no information is provided in the document or from the user, please put "<placeholder: equipment>"')
        alloc_obj = Objason(key=Alloc.uo_tag,
                            props=common_schema+[prim_prod_cell, prim_op_resource],
                            description='This class is for allocation of an operation resource for prodcution operation. '
                            'Normamally, an operation resource can be specified by a comination of a production cell (a room in a facility) and the name of a piece of equimpent. '
                            'At least an instace of this object is necessary at the top of the sequence of unit operations. '
                            'Other than the beginning of the sequence, this object shall typicall appear when the process solution is transferred to another reactor, '
                            'or when a new stage of the process, such as filtration, begins. '
                            'In a narrower meaning, this is not a unit operation on the shop floor. Thus, please do not try to assign a operation sequnce (number) to this object.')
        return alloc_obj

    def load_from_json_dict(self, json_dict: dict[str, any]):
        super().load_from_json_dict(json_dict)
        self.prod_cell = json_dict.get(hedr_cell, '<placeholder: location>')
        self.op_resouce = json_dict.get(hedr_op_resource, '<placeholder: equipment>')

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
                       prod_cell:str = None,
                       op_resouce:str = None)->pd.DataFrame:
        hedr:list[str] = defs.list_hedr_cmn_io_dtil + [hedr_cell, hedr_op_resource]
        content: list[any] = [None]*len(hedr)
        s:pd.Series = pd.Series(data=content, index=hedr)
        df = s.to_frame().T
        df.at[df.index[0], hedr_precomment] = precomment
        df.at[df.index[0], hedr_postcomment] = postcomment        
        df.at[df.index[0], hedr_cell] = prod_cell
        df.at[df.index[0], hedr_op_resource] = op_resouce
        return df
    
    @classmethod
    def add_to_test_df(cls,
                       df: pd.DataFrame=None,
                       prod_cell:str = None,
                       op_resouce:str = None)->None:
        width:int = len(df.columns)
        new_row:list[any] = [None]*width
        row:int = len(df)
        df.loc[row]=new_row
        df.at[row, hedr_cell] = prod_cell
        df.at[row, hedr_op_resource] = op_resouce
        return df


