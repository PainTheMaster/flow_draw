#########################################################
# imports
#########################################################
import pandas as pd
import warnings
import flow_draw.definitions as defs
# import flow_draw.data_io.flowsheet as fsht
from typing import Optional, Any
from flow_draw.batch.process.unit_operations import unit_operation as uo
from flow_draw.data_io import process_io as procio
from flow_draw.materials import materials as mats
from flow_draw.trait_def import trait_def as trdef
#from flow_draw.trait_def.trait_def import GetMats
from flow_draw.data_io.json_io import Objason, Primitive, Array, Tuple
from flow_draw.batch.process.unit_operations.sample import Sample




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
hedr_sample_name:str = "Sample_Name"
"""Header item for sample names"""
hedr_sampling_cat:str = "Category"
"""Header item for sampling category; IPC, Monitoring, or Both"""
hedr_ipc_criteria:str = "IPC_Criteria"
"""Header item for IPC criteria"""
hedr_ipc_rec_titles:str = "IPC_Rec_Title"
"""Header item for IPC record title for each analytical item"""
hedr_ipc_rec_units:str = "IPC_Rec_Unit"
"""Header item for IPC record unit for each analytical item"""
hedr_monit_item_high:str = "Monit_Item_High_Level"
"""Header item for sampling category; Monitoring items"""
hedr_monit_rec_items:str = "Monit_Rec_Title"
"""Header item for sampling category; monitoring record title for each analytical item"""
hedr_monit_rec_units:str = "Monit_Rec_Unit"
"""Header item for sampling category; monitoring record unit for each analytical item"""
hedr_sample_comment:str = "Sample_Comment"
"""Header item for sampling category; sample comment"""

list_hedr:list[str]=[hedr_sample_name,
                     hedr_sampling_cat,
                     hedr_ipc_criteria,
                     hedr_ipc_rec_titles,
                     hedr_ipc_rec_units,
                     hedr_monit_item_high,
                     hedr_monit_rec_items,
                     hedr_monit_rec_units,
                     hedr_sample_comment]
"""header items for the detail input form"""

key_json_monit_item_name ='json_monit_item'
"""Key to a JSON entity: A pair (object) of monitoring item name and unit."""

key_json_monit_unit ='json_monit_unit'
"""Key to a JSON entity: A pair (object) of monitoring item name and unit."""

key_json_arr_samples = "json_array_samples"
"""key to a JSON entity: an array of objects for samples"""
key_json_sampling_stage = "sampling_stage"


#########################################################
# UO-specific options, list, header_item: list dictionry thereof (for data input and internalsignaling)
#########################################################

opt_sampling_cat_ipc:str="IPC"
"""Option for the header item sampling_categoy: IPC"""
opt_sampling_cat_monit:str="Monitoring"
"""Option for the header item sampling_categoy: Monitoring"""
opt_sampling_cat_both:str="Both"
"""Option for the header item sampling_categoy: Both"""
list_opt_sampling_cat:list[str]=[opt_sampling_cat_ipc,
                                 opt_sampling_cat_monit,
                                 opt_sampling_cat_both]
"""List of options for sampling_cat"""

dict_dropdown: dict[str, list[str]] = {hedr_sampling_cat : list_opt_sampling_cat}
"""header items vs dropdown items dictionary"""

#########################################################
# signal -> local language dictionary and tags for it
#########################################################
lang_dict_uo_titles = defs.dict_jp_part_uo_titles


        ##### Tags (keys) for translation of common parts ####
# tag_flow_cmn_rec_time:str = defs.tag_flow_cmn_rec_time
# """The key to the time-recording field for the flowsheet, a common item."""
# tag_flow_cmn_rec_sign:str = defs.tag_flow_cmn_rec_sign
# """The key to the ignature field for the flowsheet, a common item."""
tag_flow_cmn_time_unit_second = opt_time_unit_second
"""Tag for a common flowsheet component for an unit of time: second"""
tag_flow_cmn_time_unit_minute = opt_time_unit_minute
"""Tag for a common flowsheet component for an unit of time: minute"""
tag_flow_cmn_time_unit_hour = opt_time_unit_hour
"""Tag for a common flowsheet component for an unit of time: hour"""
# lang_dict_cmn:dict[str, str] = defs.dict_jp_part_flow_cmn
# """
# Language dictionary for common parts.
#     tag_flow_cmn_rec_time : part_flow_cmn_rec_time_jp,
#     tag_flow_cmn_rec_sign : part_flow_cmn_rec_sign_jp
#     tag_flow_cmn_time_unit_second : part_flow_cmn_time_unit_second,
#     tag_flow_cmn_time_unit_minute : part_flow_cmn_time_unit_minute,
#     tag_flow_cmn_time_unit_hour : part_flow_cmn_time_unit_hour
# """

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
class Sampling(uo.UnitOperation, uo_tag=defs.tag_uo_sampling):
    def __init__(self,
                 caller: trdef.UniversalTrait =None,
                 flowsheet:trdef.FlowsheetTrait=None,
                 operation_seq: int=None,
                 num_subitems: int = None,
                 edit_comment:str=None):
        super().__init__(caller=caller, flowsheet=flowsheet, operation_seq=operation_seq, num_subitems=num_subitems, edit_comment=edit_comment)
        self.list_samples:list[Sample] = []
    
    def load_params_from_df(self, df: pd.DataFrame):
        """
        Loads necessary parameters from a DataFrame object.
        The header items must be in line with the definition the class Charging.
        The header items can be passed from the get_detail_header() of each UnitOperation-drived class.
        This is the overriding mehtod in the class Charging..
        """

        # first_row = df.iloc[0]
        # if not pd.isna(first_row[hedr_precomment]):
        #     self.pre_comment = first_row[hedr_precomment]
        # if not pd.isna(first_row[hedr_postcomment]):
        #     self.post_comment = first_row[hedr_postcomment]
        # for sample_seq, subitem in df.iterrows():
        #     temp_sample = SingleSample(flowsheet=self.flowsheet)
        #     temp_sample.load_from_series(caller=self, sample_seq=sample_seq, ser=subitem)
        #     self.list_samples.append(temp_sample)
        pass


    def get_seq(self)-> int:
        return self.operation_seq
    
    def get_detail_header(self) -> list[str]:
        return list_hedr

    def get_detail_option_menu(self) -> Optional[dict[str, list[str]]]:
        return dict_dropdown
    
    def print_unit_operation(self):
        # self.flowsheet.header_organizer(op_nr=self.operation_seq, title=lang_dict_uo_titles[self.uo_tag])
        self.flowsheet.header_organizer(title=lang_dict_uo_titles[self.uo_tag])

        if self.pre_comment:
            self.flowsheet.put_body_comments(self.pre_comment)
            self.flowsheet.linefeed()        

        for sample in self.list_samples:
            # sample.output_single_sample()
            # self.flowsheet.linefeed()
            sample.print_sample()
            self.flowsheet.linefeed()

        if self.post_comment:
            self.flowsheet.put_body_comments(self.post_comment)
            self.flowsheet.linefeed()

    @staticmethod
    def get_json_schema(caller:trdef.UniversalTrait = None) -> Objason:
        common = Sampling.json_common()
       
        single_sample = Sample.get_json_schema(caller=caller)

        arr_samples = Array(key=key_json_arr_samples,
                            content=single_sample,
                            description="An array of samples belonging to one sampling block and the necessary monitoring and/or IPC requirements associated with them. ",
                            required=True,
                            nullable=True)

        json_sampling = Objason(key=Sampling.uo_tag,
                                props=common+[arr_samples],
                                description='An object for a single sampling stage.')

        return json_sampling 
        

    def load_from_json_dict(self, json_dict:dict[str, Any]):
        super().load_from_json_dict(json_dict)
        arr_sample:list[dict[str,Any]] = json_dict.get(key_json_arr_samples)
        self.list_samples.clear()
        if arr_sample is not None:
            for sample in arr_sample:
                single_sample = Sample(flowsheet=self.flowsheet, json_dict=sample)
                self.list_samples.append(single_sample)


    @staticmethod
    def generate_test_df(sample_name:str = None,
                         sampling_cat:str = None,
                         ipc_criteria:str = None,
                         ipc_rec_titles:str = None,
                         ipc_rec_units:str = None,
                         monit_items:str = None,
                         monit_rec_items:str = None,
                         monit_rec_units:str = None,
                         sample_comment:str = None
                         )->pd.DataFrame:
        hedr:list[str] = defs.list_hedr_cmn_io_dtil + list_hedr
        content: list[any] = [None]*len(hedr)
        s:pd.Series = pd.Series(data=content, index=hedr)
        df = s.to_frame().T
        df.at[df.index[0], hedr_sample_name] = sample_name
        df.at[df.index[0], hedr_sampling_cat] = sampling_cat
        df.at[df.index[0], hedr_ipc_criteria] = ipc_criteria
        df.at[df.index[0], hedr_ipc_rec_titles] = ipc_rec_titles
        df.at[df.index[0], hedr_ipc_rec_units] = ipc_rec_units
        df.at[df.index[0], hedr_monit_item_high] = monit_items
        df.at[df.index[0], hedr_monit_rec_items] = monit_rec_items
        df.at[df.index[0], hedr_monit_rec_units] = monit_rec_units
        df.at[df.index[0], hedr_sample_comment] = sample_comment

        return df
    
    @staticmethod
    def add_to_test_df(df: pd.DataFrame=None,
                       sample_name:str = None,
                       sampling_cat:str = None,
                       ipc_criteria:str = None,
                       ipc_rec_titles:str = None,
                       ipc_rec_units:str = None,
                       monit_items:str = None,
                       monit_rec_items:str = None,
                       monit_rec_units:str = None,
                       sample_comment:str = None
                       )->None:
        width:int = len(df.columns)
        new_row:list[any] = [None]*width
        row:int = len(df)
        df.loc[row]=new_row
        df.at[row, hedr_sample_name] = sample_name
        df.at[row, hedr_sampling_cat] = sampling_cat
        df.at[row, hedr_ipc_criteria] = ipc_criteria
        df.at[row, hedr_ipc_rec_titles] = ipc_rec_titles
        df.at[row, hedr_ipc_rec_units] = ipc_rec_units
        df.at[row, hedr_monit_item_high] = monit_items
        df.at[row, hedr_monit_rec_items] = monit_rec_items
        df.at[row, hedr_monit_rec_units] = monit_rec_units
        df.at[row, hedr_sample_comment] = sample_comment




        
