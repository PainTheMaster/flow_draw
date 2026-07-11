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
from flow_draw.data_io.json_io import Objason, Primitive, Array, Tuple




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
hedr_monit_items:str = "Monit_Item"
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
                     hedr_monit_items,
                     hedr_monit_rec_items,
                     hedr_monit_rec_units,
                     hedr_sample_comment]
"""header items for the detail input form"""

key_json_arr_monit_items = 'json_array_monit_items'
"""Key to a JSON entity: An array of monitoring items"""
key_json_tuple_monit ='json_monitoring_pair'
"""Key to a JSON entity: A pair (tuple) of monitoring item name and unit."""
key_json_obj_monit = 'json_process_monitoring'
"""Key to a JSON entity: A set of process monitoring for a sample."""
key_json_arr_monit = 'json_arr_monitoring'
"""key to a JSON entity: An array of monitoring items."""
key_json_tuple_ipc = 'json_ipc_tuple'
"""Kye to a JSON entry: A tuple of ipc item, unit, and criterion."""
key_json_arr_ipc_items = 'json_array_ipc_items'
"""Key to a JSON entry: an array of tuple of IPC items"""
key_json_single_sample = "json_single_sample"
"""Key to a JSON entry: an object for a single sample"""
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

dict_dropdown: dict[str, str] = {hedr_sampling_cat : list_opt_sampling_cat}
"""header items vs dropdown items dictionary"""

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

tag_part_flow_mthod_instr_sampling:str = "method col sampling"
"""Tag for a flowsheet component: sampling"""
part_flow_mthod_instr_sampling_jp:str = "サンプリング"
"""A flowsheet component: sampling"""

tag_part_flow_rec_criterion_ok_nok:str = "ok nok"
"""Tag for a flowsheet component: IPC criterion OK or NOK"""
part_flow_rec_criterion_ok_nok_jp:str = "□ 適 □ 不適"
"""A flowsheet component: IPC criterion OK or NOK"""

tag_part_flow_rec_sampleID:str = "sample ID"
"""Tag for a flowsheet component: record field for sample ID"""
part_flow_rec_sampleID_jp:str = "サンプルID____________"
"""A flowsheet component: record field for sample ID"""



tag_stc_flow_content_sample_name = "content sample name"
"""Tag for a sentence template: sample name field for content column; includes placeholders {sample_name}"""
stc_flow_content_sample_name_jp = "サンプル名:{sample_name}"
"""a sentence template: sample name template for content column; includes placeholders {sample_name}"""

tag_stc_flow_ipc_criterion = "stc ipc criterion"
"""Tag for a sentence template: ipc criteron template for content column; includes placeholders {ipc_criterion}"""
stc_flow_ipc_criterion_jp = "IPC:{ipc_criterion}"
"""a sentence template: ipc criteron template for content column; includes placeholders {ipc_criterion}"""

tag_stc_flow_rec_ipc_result = "rec ipc result"
"""Tag for a sentence template: record field for ipc result; includes placeholders {ipc_item} and {ipc_rec_unit}"""
stc_flow_rec_ipc_result_jp = "{ipc_item}:__________{ipc_rec_unit}"
"""a sentence template: record field for ipc result; includes placeholders {ipc_item} and {ipc_rec_unit}"""

tag_stc_flow_monit_item = "content monitoring item"
"""Tag for a sentence template: sentence template for monitoring item in the content column; includes placeholders {monit_item}"""
stc_flow_monit_item_jp = "モニタリング:{monit_item}"
"""a sentence template: sentence template for monitoring item in the content column; includes placeholders {monit_item}"""

tag_stc_flow_rec_monit_result = "rec monitoring result"
"""Tag for a sentence template: record field for monitoring result; includes placeholders {monit_item} and {monit_rec_unit}"""
stc_flow_rec_monit_result_jp = "{monit_item}:__________{monit_rec_unit}"
"""a sentence template: record field for monitoring result; includes placeholders {monit_item} and {monit_rec_unit}"""

dict_parts_stcs_jp = {tag_part_flow_mthod_instr_sampling : part_flow_mthod_instr_sampling_jp,
                      tag_part_flow_rec_criterion_ok_nok : part_flow_rec_criterion_ok_nok_jp,
                      tag_part_flow_rec_sampleID : part_flow_rec_sampleID_jp,
                      tag_stc_flow_content_sample_name : stc_flow_content_sample_name_jp,
                      tag_stc_flow_ipc_criterion : stc_flow_ipc_criterion_jp,
                      tag_stc_flow_rec_ipc_result : stc_flow_rec_ipc_result_jp,
                      tag_stc_flow_monit_item : stc_flow_monit_item_jp,
                      tag_stc_flow_rec_monit_result : stc_flow_rec_monit_result_jp}
"""JP language dictionary for flowsheet parts and sentence templates"""

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
class Sampling(uo.UnitOperation, uo_tag=defs.tag_uo_sampling):
    def __init__(self,
                 caller: type[trdef.UniversalTrait] =None,
                 flowsheet:fsht.Flowsheet=None,
                 operation_seq: int=None,
                 num_subitems: int = None,
                 edit_comment:str=None):
        super().__init__(caller=caller, flowsheet=flowsheet, operation_seq=operation_seq, num_subitems=num_subitems, edit_comment=edit_comment)
        self.list_samples:list[SingleSample] = []
    
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
        for sample_seq, subitem in df.iterrows():
            temp_sample = SingleSample(flowsheet=self.flowsheet)
            temp_sample.load_from_series(caller=self, sample_seq=sample_seq, ser=subitem)
            self.list_samples.append(temp_sample)


    def get_seq(self)-> int:
        return self.operation_seq
    
    def get_detail_header(self) -> list[str]:
        return list_hedr

    def get_detail_option_menu(self) -> Optional[dict[str, list[str]]]:
        return dict_dropdown
    
    def output_unit_operation(self):
        self.flowsheet.header_organizer(op_nr=self.operation_seq, title=lang_dict_uo_titles[self.uo_tag])
        if not (self.pre_comment == None or self.pre_comment == ''):
            self.flowsheet.put_body_comments(self.pre_comment)
            self.flowsheet.linefeed()        

        for sample in self.list_samples:
            sample.output_single_sample()
            self.flowsheet.linefeed()

        if not (self.post_comment == None or self.post_comment == ''):
            self.flowsheet.put_body_comments(self.post_comment)
            self.flowsheet.linefeed()
    
    def get_json_schema(caller:trdef.UniversalTrait = None) -> Objason:
        common = Sampling.json_common()
        sample_name:Primitive = Primitive(prim_type='string',
                                          key=hedr_sample_name,
                                          description='The name of a sample.')
        sample_cat:Primitive=Primitive(prim_type='string',
                                       key=hedr_sampling_cat,
                                       description=f'Category of the sample.'\
                                        f'"{opt_sampling_cat_ipc}" stands for in-process control with a must-satisfied criterion before moving to the next step. '\
                                        f'"{opt_sampling_cat_monit}" is sampling for technical information. Normally, not with a criterion. '\
                                        f'"{opt_sampling_cat_both}" is for both in-process control and monitoring. One or more analytical items are for decision making, whereas the other are just for info.',
                                       enum=list_opt_sampling_cat
                                       )
        
        #以下、モニタリング
        monit_item_name = Primitive(prim_type='string',
                                    key=hedr_monit_items,
                                    description=f'A monitoring item. This items is applicable to sampling categories of "{opt_sampling_cat_monit}" and "{opt_sampling_cat_both}". '\
                                        'This is more a high-level identifier, such as purity, residual solvent, etc. '\
                                        'instead of concrete names such as this impurity, that impurity, or this solvent... '\
                                        'if a right name cannot be read from the source, please put <placeholder>.')
        monit_ietm = Primitive(prim_type='string',
                                   key=hedr_monit_rec_items,
                                   description=f'A lower-layer recording item belonging to a super-category "{hedr_monit_items}"'\
                                   'a concrete analytical items such as residual solvent, impurity, assay, pH, etc.')
        monit_unit = Primitive(prim_type='string',
                                   key=hedr_monit_rec_units,
                                   description=f'Unit for a monitoring item. Null is accepted.',
                                   accept_null=True,
                                   required=True)
        tuple_monit = Tuple(key=key_json_tuple_monit,
                            content=[monit_ietm, monit_unit],
                            description='A pair of monitoring item and unit for it.')
        arr_monit_items = Array(key=key_json_arr_monit_items,
                                content=tuple_monit,
                                description=f'An array of tuple of monitoring item and unit for it. This is linked to "{hedr_monit_items}".',
                                required=False)
        obj_monit = Objason(key=key_json_obj_monit,
                            props=[monit_item_name, arr_monit_items],
                            description='A set of process monitoring information linked to a sample.')
        arr_monit = Array(key=key_json_arr_monit,
                          content = obj_monit,
                          description="An array of various kinds of monitoring items.",
                          required=False)
        
        #IPC below
        ipc_item = Primitive(prim_type='string',
                             key=hedr_ipc_rec_titles,
                             description='IPC items, such as a residual solvent, a specific impurity, conversion, etc.')
        ipc_unit = Primitive(prim_type='string',
                             key=hedr_ipc_rec_units,
                             description='reporting unit for the IPC item, such as %, ppm, etc.')
        ipc_criterion = Primitive(prim_type='string',
                                 key=hedr_ipc_criteria,
                                 description='IPC criterion, e.g., "conversion>99.95%"')
        tuple_ipc = Tuple(key=key_json_tuple_ipc,
                          content=[ipc_item, ipc_unit, ipc_criterion],
                          description='A set (tuple) of IPC item, unit for the item, and IPC criterion for it.')
        arr_ipc = Array(key=key_json_arr_ipc_items,
                        content=tuple_ipc,
                        description='A series (array) of a set of IPC items, unit for it, and criterion for one sample.',
                        required=False)
        
        single_sample = Objason(key=key_json_single_sample,
                                props=[sample_name, sample_cat, arr_monit, arr_ipc],
                                description="Descriptor of a sample. A collection of the sample name, sampling category (monitoring and/or IPC), necessary monitoring items, IPC items, and the criteria for the IPC.")
        
        arr_samples = Array(key=key_json_arr_samples,
                            content=single_sample,
                            description="An array of samples belonging to one sampling block and the necessary monitoring and/or IPC requirements associateid with them.",
                            required=True)

        json_sampling = Objason(#key=key_json_sampling_stage,
                                key=Sampling.uo_tag,
                                props=common+[arr_samples],
                                description='An object for a single sampling stage.')

        return json_sampling 
        

        
        
        
        

        
        
        
        
        




    @classmethod
    def generate_test_df(cls,
                         sample_name:str = None,
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
        df.at[df.index[0], hedr_monit_items] = monit_items
        df.at[df.index[0], hedr_monit_rec_items] = monit_rec_items
        df.at[df.index[0], hedr_monit_rec_units] = monit_rec_units
        df.at[df.index[0], hedr_sample_comment] = sample_comment

        return df
    
    @classmethod
    def add_to_test_df(cls,
                       df: pd.DataFrame=None,
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
        df.at[row, hedr_monit_items] = monit_items
        df.at[row, hedr_monit_rec_items] = monit_rec_items
        df.at[row, hedr_monit_rec_units] = monit_rec_units
        df.at[row, hedr_sample_comment] = sample_comment

class SingleSample:
    def __init__(self, flowsheet:fsht.Flowsheet=None):
        self.flowsheet:fsht.Flowsheet = flowsheet
        self.sample_seq:int = None
        self.name:str = None
        self.category:str = None
        """IPC, monitoring, both"""
        self.content_ipc_criteria:list[str] = []
        self.content_monit_items:list[str] = []
        self.rec_ipc_item_name:list[str] = []
        self.rec_ipc_unit:list[str] = []
        self.rec_monit_item_name:list[str] = []
        self.rec_monit_unit:list[str] = []
        self.sample_comment:str = None
    
    def load_from_series(self, caller:Sampling, sample_seq:int, ser:pd.Series):
        self.sample_seq = sample_seq
        if not pd.isna(ser[hedr_sample_name]):
            self.name = ser[hedr_sample_name]
        else:
            raise ValueError(f"{caller.__class__.__name__} Op. Seq. {caller.get_seq}: No name provided for the {self.sample_seq+1}th sample in the detail input.")
        
        if not pd.isna(ser[hedr_sampling_cat]):
            self.category = ser[hedr_sampling_cat]
        else:
            raise ValueError(f"{caller.__class__.__name__} Op. Seq. {caller.get_seq}: No sampling category chosen for the {self.sample_seq+1}th sample in the detail input.")
        
        if self.category == opt_sampling_cat_ipc or self.category == opt_sampling_cat_both:
            if not pd.isna(ser[hedr_ipc_criteria]):
                str_criteria:str = ser[hedr_ipc_criteria]
                if not pd.isna(str_criteria):
                    self.content_ipc_criteria = str_criteria.split("\n")
            else:
                raise ValueError(f"{caller.__class__.__name__} Op. Seq. {caller.get_seq}: No IPC criteria provided for the {self.sample_seq+1}th sample in the detail input \
                                although {opt_sampling_cat_ipc}/{opt_sampling_cat_both} is selected in the colum {hedr_sampling_cat}.")
            if not pd.isna(ser[hedr_ipc_rec_titles]):
                str_ipc_rec_titles:str = ser[hedr_ipc_rec_titles]
                str_ipc_rec_units:str = ser[hedr_ipc_rec_units]
                self.rec_ipc_item_name = str_ipc_rec_titles.split("\n")
                if not pd.isna(str_ipc_rec_units):
                    self.rec_ipc_unit = str_ipc_rec_units.split("\n")
                if len(self.rec_ipc_item_name) != len(self.rec_ipc_unit):
                    raise ValueError(f"{caller.__class__.__name__} Op. Seq. {caller.get_seq}: Mismatched numbers of IPC items and their units for the {self.sample_seq+1}th sample in the detail input.")
                if len(self.rec_ipc_item_name) != len(self.content_ipc_criteria):
                    raise ValueError(f"{caller.__class__.__name__} Op. Seq. {caller.get_seq}: Mismatched numbers of IPC criteria and their units for the {self.sample_seq+1}th sample in the detail input.")
            else:
                raise ValueError(f"{caller.__class__.__name__} Op. Seq. {caller.get_seq}: No IPC record name provided for the {self.sample_seq+1}th sample in the detail input \
                                although {opt_sampling_cat_ipc}/{opt_sampling_cat_both} is selected in the colum {hedr_sampling_cat}.")
        
        if self.category == opt_sampling_cat_monit or self.category == opt_sampling_cat_both:
            if not pd.isna(ser[hedr_monit_items]):
                str_monit_item:str = ser[hedr_monit_items]
                self.content_monit_items = str_monit_item.split("\n")
            if not pd.isna(ser[hedr_monit_rec_items]):
                str_monit_rec_items:str =  ser[hedr_monit_rec_items]
                str_monit_rec_units:str = ser[hedr_monit_rec_units]
                self.rec_monit_item_name = str_monit_rec_items.split("\n")
                if not pd.isna(str_monit_rec_units):
                    self.rec_monit_unit = str_monit_rec_units.split("\n")
                if len(self.rec_monit_item_name) != len(self.rec_monit_unit):
                    raise ValueError(f"{caller.__class__.__name__} Op. Seq. {caller.get_seq}: Mismatched numbers of monitoring items and their units for the {self.sample_seq+1}th sample in the detail input.")
        if not pd.isna(ser[hedr_sample_comment]):
            self.sample_comment = ser[hedr_sample_comment]

    def output_single_sample(self):
        self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                method=dict_parts_stcs[tag_part_flow_mthod_instr_sampling],
                                content=dict_parts_stcs[tag_stc_flow_content_sample_name].format(sample_name=self.name),
                                record=dict_parts_stcs[tag_part_flow_rec_sampleID],
                                operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
        if self.category == opt_sampling_cat_ipc or self.category == opt_sampling_cat_both:
            self.__output_IPC()
        if self.category == opt_sampling_cat_monit or self.category == opt_sampling_cat_both:
            self.__output_monit()
        


    def __output_IPC(self):
        for idx in range(len(self.content_ipc_criteria)):
            temp_ipc_criteria:str = dict_parts_stcs[tag_stc_flow_ipc_criterion].format(ipc_criterion=self.content_ipc_criteria[idx])
            temp_ipc_rec:str = dict_parts_stcs[tag_stc_flow_rec_ipc_result].format(ipc_item=self.rec_ipc_item_name[idx], ipc_rec_unit=self.rec_ipc_unit[idx])
            self.flowsheet.put_line(content=temp_ipc_criteria,
                                    record=temp_ipc_rec)
            self.flowsheet.put_line(record=dict_parts_stcs[tag_part_flow_rec_criterion_ok_nok])

    def __output_monit(self):
        idx_long:int = None
        if len(self.content_monit_items) >= len(self.rec_monit_item_name):
            idx_long = len(self.content_monit_items)
        else:
            idx_long = len(self.rec_monit_item_name)
        
        for idx in range(idx_long):
            temp_content_monit_item: str = ""
            if idx <=len(self.content_monit_items)-1:
                temp_content_monit_item = dict_parts_stcs[tag_stc_flow_monit_item].format(monit_item=self.content_monit_items[idx])
            temp_rec_monit_item:str = ""
            if idx <= len(self.rec_monit_item_name)-1:
                temp_rec_monit_item = dict_parts_stcs[tag_stc_flow_rec_monit_result].format(monit_item=self.rec_monit_item_name[idx],
                                                                                            monit_rec_unit=self.rec_monit_unit[idx])
            self.flowsheet.put_line(content=temp_content_monit_item,
                                    record=temp_rec_monit_item)

            





        
