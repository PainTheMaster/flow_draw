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
key_class_name:str = 'Sample_class'
"""Header item for the class name"""
key_stem_sample_name:str = "Sample_name_stem"
"""Header item for sample names"""
key_suffix_sample_name:str = "Sample_name_suffix"
"""Key to the suffix of sample name"""
key_test_purpose:str = "Test_purpose"
"""Header item for sampling category; IPC, Monitoring, or Both"""
key_analysis_attribute:str = "Analysis_attribute"
"""Header item for sampling category: analysis attribute"""
key_analyte:str = 'Analyte'
"""Header item for analyte of the analysis"""
key_criteria_val_1:str = "Criteria_value_1"
"""Header item for IPC criteria 1"""
key_comparator_1:str = 'Criteria_comparator_1'
"""Header item for IPC criteria relations 1"""
key_criteria_val_2:str = "Criteria_value_2"
"""Header item for IPC criteria 2"""
key_comparator_2:str = 'Criteria_comparator_2'
"""Header item for IPC criteria relations 2"""
key_unit_meas:str = 'measurement_unit'
"""Header item for analysis: unit"""
key_obj_analysis:str = 'single_analysis_object'
"""Header item for analysis: analysis object"""
key_arr_analysis:str = 'array_of_analysis'
"""Header item for analysis: """
key_sample_comment:str = 'comment_for_sample'
"""Header item for sample comment"""
key_obj_sampe:str = 'sample_object'
"""header item for analysis: object for a sample"""

# hedr_ipc_rec_titles:str = "IPC_Rec_Title"
"""Header item for IPC record title for each analytical item"""
# hedr_ipc_rec_units:str = "IPC_Rec_Unit"
# """Header item for IPC record unit for each analytical item"""
# hedr_monit_item_high:str = "Monit_Item_High_Level"
# """Header item for sampling category; Monitoring items"""
# hedr_monit_rec_items:str = "Monit_Rec_Title"
# """Header item for sampling category; monitoring record title for each analytical item"""
# hedr_monit_rec_units:str = "Monit_Rec_Unit"
# """Header item for sampling category; monitoring record unit for each analytical item"""
# hedr_sample_comment:str = "Sample_Comment"
"""Header item for sampling category; sample comment"""

list_hedr:list[str]=[key_class_name, 
                     key_stem_sample_name,
                     key_suffix_sample_name,
                     key_test_purpose,
                     key_analysis_attribute,
                     key_analyte,
                     key_criteria_val_1,
                     key_comparator_1,
                     key_criteria_val_2,
                     key_comparator_2,
                     key_unit_meas,
                     key_obj_analysis,
                     key_arr_analysis,
                     key_sample_comment,
                     key_obj_sampe
                    ]
"""header items for the detail input form"""

key_json_arr_monit_items = 'json_array_monit_items'
"""Key to a JSON entity: An array of monitoring items"""
# key_json_tuple_monit ='json_monitoring_pair'
# """Key to a JSON entity: A pair (tuple) of monitoring item name and unit."""
key_json_pair_monit ='json_monit_pair'
"""Key to a JSON entity: A pair (object) of monitoring item name and unit."""

key_json_monit_item_name ='json_monit_item'
"""Key to a JSON entity: A pair (object) of monitoring item name and unit."""

key_json_monit_unit ='json_monit_unit'
"""Key to a JSON entity: A pair (object) of monitoring item name and unit."""

key_json_obj_monit = 'json_proc_monit'
"""Key to a JSON entity: A set of process monitoring for a sample."""
key_json_arr_monit = 'json_arr_monit'
"""key to a JSON entity: An array of monitoring items."""
key_json_obj_ipc = 'json_obj_ipc'
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

const_class_sample = 'Sample_class'
"""constant for the class name: sample_class"""

opt_analysis_cat_ipc:str="Analysis_IPC"
"""Option for the header item sampling_categoy: IPC"""
opt_analysis_cat_monit_tgt = "Analysis_monitoring_with_target"
"""Option for the header item samplingcategory"""
opt_analysis_cat_fio:str="Analysis_monitoring_informative"
"""Option for the header item sampling_categoy: Monitoring"""
list_opt_analysis_purpose:list[str]=[opt_analysis_cat_ipc,
                                     opt_analysis_cat_monit_tgt,
                                     opt_analysis_cat_fio]
"""List of options for sampling_cat"""

################## Attribute ################## 
opt_attrbt_conversion = 'conversion'
"""An option for analysis attribute: reaction conversion"""
opt_attrbt_rmnng_reactant = 'remaining_reactant'
"""An option for analysis attribute: remaining reactant."""
opt_attrbt_imp_level = 'impurity_level'
"""An option for analysis attribute: impurity level"""
opt_attrbt_ee = 'ee'
"""An option for analysis attribute: enantiomeric excess"""
opt_attrbt_de = 'de'
"""An option for analysis attribute: diastereomeric excess"""
opt_attrbt_water_cntnt = 'water_content'
"""An option for analysis attribute: moisture level"""
opt_attrbt_pH = 'pH'
"""An option for analysis attribute: pH"""
opt_attrbt_extract_loss = 'loss_to_wash_phase'
"""An option for analysis attribute: product loss in liq-liq wash"""
opt_attrbt_resid_excess = 'residual_reagent_level'
"""An option for analysis attribute: residual excess reagent, building block, catalyst in purging"""
opt_attrbt_solv_fraction = 'solvent_fraction'
"""An option for analysis attribute: solvent fraction in a process liquid or filtrate"""
opt_attrbt_tm_conc_pl = "target_material_concentration_in_process_liquid"
"""An option for analysis attribute: concentration of target material in process liquid"""
opt_attrbt_tm_conc_ml = "target_material_concentration_in_mother_liquor"
"""An option for analysis attribute: concentration of target material in mother liquor"""
opt_attrbt_cryst_form = "crystal_form"
"""An option for analysis attribute: crystal polymorphism"""
opt_attrbt_filt_liq_indicator = "cryst_wash_filtrate_indicator"
"""An option for analysis attribute: wet cake wash filtrate indicator, e.g., conductivity, salt conc., color, etc."""
opt_attrbt_filt_assay_tm = "target_material_assay"
"""An option for analysis attribute: assay of the target material in wet cake or dry product"""
opt_attrbt_lod = "loss_on_drying"
"""An option for analysis attribute: LOD"""
opt_attrbt_resid_solv = "residual_solvent_level"
"""An option for analysis attribute: individual residual solvent level"""
opt_attrbt_particle_size = "particle_size"
"""An option for analysis attribute: particle size."""
opt_attrbt_other = 'attribute_other'
"""An option for analysis attribute: other"""

list_opt_attrbt = [opt_attrbt_conversion,
                   opt_attrbt_rmnng_reactant,
                   opt_attrbt_imp_level,
                   opt_attrbt_ee,
                   opt_attrbt_de,
                   opt_attrbt_water_cntnt,
                   opt_attrbt_pH,
                   opt_attrbt_extract_loss,
                   opt_attrbt_resid_excess,
                   opt_attrbt_solv_fraction,
                   opt_attrbt_tm_conc_pl,
                   opt_attrbt_tm_conc_ml,
                   opt_attrbt_cryst_form,
                   opt_attrbt_filt_liq_indicator,
                   opt_attrbt_filt_assay_tm,
                   opt_attrbt_lod,
                   opt_attrbt_resid_solv,
                   opt_attrbt_particle_size,
                   opt_attrbt_other
                   ]

################## Comparators ################## 
opt_comparator_equal = 'equal_to'
"""An option for criteria relation: equal to"""
opt_comparator_match = 'matches'
"""An option for criteria relation: matches"""
opt_comparator_lt = 'less_than'
"""An option for criteria relation: less than"""
opt_comparator_nmt = 'not_more_than'
"""An option for criteria relation: not more than"""
opt_comparator_nlt = 'not_less_than'
"""An option for criteria relation: not_less_than"""
opt_comparator_gt = 'greater_than'
"""An option for criteria relation: greater than"""
list_opt_comparator = [opt_comparator_equal,
                       opt_comparator_match,
                       opt_comparator_lt,
                       opt_comparator_nmt,
                       opt_comparator_nlt,
                       opt_comparator_gt]

# dict_dropdown: dict[str, str] = {hedr_sampling_cat : list_opt_analysis_purpose}
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

tag_part_flow_mthod_instr_sampling:str = "method_col_sampling"
"""Tag for a flowsheet component: sampling"""
# part_flow_mthod_instr_sampling_jp:str = "サンプリング"
"""A flowsheet component: sampling"""

tag_part_flow_rec_ok_nok:str = "ok nok"
"""Tag for a flowsheet component: IPC criterion OK or NOK"""
# part_flow_rec_criterion_ok_nok_jp:str = "□ 適 □ 不適"
"""A flowsheet component: IPC criterion OK or NOK"""

tag_part_flow_rec_sampleID:str = "sample ID"
"""Tag for a flowsheet component: record field for sample ID"""
# part_flow_rec_sampleID_jp:str = "サンプルID____________"
"""A flowsheet component: record field for sample ID"""
tag_stc_attrb_conversion:str = "sentence_conversion"
'''A flowsheet compoent: the template for "conversion", includes a placeholder {analyte}'''
tag_stc_attrb_rmnng_reactant:str = "sentence_remaining_reactant"
"""A flowsheet compoent: the template for remaining reactant, includes a placeholder {analyte}"""
tag_stc_attrb_imp_level:str = "sentence_impurity_level"
"""A flowsheet compoent: the template for a impurity level, includes a palcehoder {analyte}"""
tag_stc_attrb_ee:str = "sentence_ee"
"""A flowsheet compoent: the template for ee of a sample, includes a palcehoder {analyte}"""
tag_stc_attrb_de:str = "sentence_de"
"""A flowsheet compoent: the template for de of a sample, includes a palcehoder {analyte}"""
tag_stc_attrb_water_cntnt:str = "sentence_water_content"
"""A flowsheet compoent: the template for water content of a sample, may include a palcehoder {analyte}"""
tag_stc_attrb_pH:str = 'sentence_pH'
"""A flowsheet compoent: the template for pH of a sample. No analyte placeholder."""
tag_stc_attrb_extract_loss:str = "sentence_loss_to_wash_phase"
"""A flowsheet compoent: the template for product loss to wash phase, includes a placeholder {analyte}"""
tag_stc_attrb_resid_excess:str = "sentence_residual_reagent_level"
"""A flowsheet compoent: the template for residual excess reagent/catalyst level, includes a placeholder {analyte}"""
tag_stc_attrb_solv_fraction:str = "sentence_solvent_fraction"
"""A flowsheet compoent: the template for solvent fraction in a process liquid, includes a placeholder {analyte}"""
tag_stc_attrb_tm_conc_pl:str = "sentence_tm_conc_process_liquid"
"""A flowsheet compoent: the template for target material concentration in process liquid, includes a placeholder {analyte}"""
tag_stc_attrb_tm_conc_ml:str = "sentence_tm_conc_mother_liquor"
"""A flowsheet compoent: the template for target material concentration in mother liquor, includes a placeholder {analyte}"""
tag_stc_attrb_cryst_form:str = "sentence_crystal_form"
"""A flowsheet compoent: the template for crystal form, may include a placeholder {analyte}"""
tag_stc_attrb_filt_liq_indicator:str = "sentence_cryst_wash_filtrate_indicator"
"""A flowsheet compoent: the template for crystal wash filtrate indicator, may include a placeholder {analyte}"""
tag_stc_attrb_filt_assay_tm:str = "sentence_target_material_assay"
"""A flowsheet compoent: the template for assay of the target material, includes a placeholder {analyte}"""
tag_stc_attrb_lod:str = "sentence_loss_on_drying"
"""A flowsheet compoent: the template for loss on drying. No analyte placeholder."""
tag_stc_attrb_resid_solv:str = "sentence_residual_solvent_level"
"""A flowsheet compoent: the template for individual residual solvent level, includes a placeholder {analyte}"""
tag_stc_attrb_particle_size:str = "sentence_particle_size"
"""A flowsheet compoent: the template for particle size. No analyte placeholder."""
tag_stc_attrb_other:str = "sentence_attribute_other"
"""A flowsheet compoent: the template for other attributes, includes a placeholder {analyte}"""

tag_part_comparator_equal = opt_comparator_equal
"""A flowsheet compoent the word for equal"""
tag_part_comparator_match = opt_comparator_match
"""A flowsheet compoent the word for match"""
tag_part_comparator_lt = 'less_than'
'''A flowsheet compoent the word for "<"'''
tag_part_comparator_nmt = 'not_more_than'
"""A flowsheet compoent the word for not ≦"""
tag_part_comparator_nlt = opt_comparator_nlt
"""A flowsheet compoent the word for not less than"""
tag_part_comparator_gt = opt_comparator_gt
"""A flowsheet compoent the word for greater than"""



tag_stc_flow_content_sample_name = "content sample name"
"""Tag for a sentence template: sample name field for content column; includes placeholders {sample_name}"""
# stc_flow_content_sample_name_jp = "サンプル名:{sample_name}"
"""a sentence template: sample name template for content column; includes placeholders {sample_name}"""

tag_stc_flow_ipc = "stc ipc criterion"
"""Tag for a sentence template: ipc criteron template for content column; includes placeholders {analysis_item}"""

tag_stc_flow_rec_ipc_result = "rec ipc result"
"""Tag for a sentence template: record field for ipc result; includes placeholders {analysis_item} and {meas_unit}"""

tag_stc_flow_monit_tgt = 'content_monit_with_tgt'
"""Tag fro a sentece template: sentence template for monitoring with a target includes a placeholder {analysis_item}"""
tag_stc_flow_fio = "content_monitoring_item"
"""Tag for a sentence template: sentence template for monitoring item in the content column; includes placeholders {analysis_item}"""
# stc_flow_monit_item_jp = "モニタリング:{monit_item}"
"""a sentence template: sentence template for monitoring item in the content column; includes placeholders {monit_item}"""

tag_stc_flow_rec_analysis_result = "rec monitoring result"
"""Tag for a sentence template: record field for monitoring result; includes placeholders {analysis_item} and {meas_unit}"""


dict_parts_stcs_jp = {tag_part_flow_mthod_instr_sampling : "サンプリング",
                      tag_part_flow_rec_ok_nok : "□ 適 □ 不適",
                      tag_part_flow_rec_sampleID : "サンプルID____________",
                      
                      tag_part_comparator_equal : '=',
                      tag_part_comparator_match : ': ',
                      tag_part_comparator_lt : '<',
                      tag_part_comparator_nmt : '≦',

                      tag_stc_attrb_conversion : "{analyte}転化率",
                      tag_stc_attrb_rmnng_reactant : "{analyte}残存率",
                      tag_stc_attrb_imp_level: "{analyte}量",
                      tag_stc_attrb_ee: "{analyte}ee",
                      tag_stc_attrb_de: '{analyte}de',
                      tag_stc_attrb_water_cntnt: "水分含量",
                      tag_stc_attrb_pH: "pH",
                      tag_stc_attrb_extract_loss: "洗浄相への{analyte}ロス",
                      tag_stc_attrb_resid_excess: "{analyte}残存量",
                      tag_stc_attrb_solv_fraction: "{analyte}含有率",
                      tag_stc_attrb_tm_conc_pl: "{analyte}濃度",
                      tag_stc_attrb_tm_conc_ml: "母液中{analyte}濃度",
                      tag_stc_attrb_cryst_form: "{analyte}結晶形",
                      tag_stc_attrb_filt_liq_indicator: "洗浄ろ液{analyte}指標",
                      tag_stc_attrb_filt_assay_tm: "{analyte}含量",
                      tag_stc_attrb_lod: "乾燥減量",
                      tag_stc_attrb_resid_solv: "残留{analyte}量",
                      tag_stc_attrb_particle_size: "粒度",
                      tag_stc_attrb_other: "{analyte}<placeholder>",


                      tag_stc_flow_content_sample_name : "サンプル名:{sample_name}",
                      tag_stc_flow_ipc : "IPC:{analysis_item}",
                    #   tag_stc_flow_rec_ipc_result : "{analysis_item}:__________{meas_unit}",
                      tag_stc_flow_monit_tgt : 'モニタリング(目標):{analysis_item}',
                      tag_stc_flow_fio : "モニタリング:{analysis_item}",
                      tag_stc_flow_rec_analysis_result : "{analysis_item}:__________{meas_unit}",
                      }
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
class Sample(trdef.SampleTrait):
    def __init__(self, flowsheet:trdef.FlowsheetTrait=None, json_dict:dict[str,Any]=None):
        self.flowsheet = flowsheet
        if not json_dict:
            raise RuntimeError(f'{self.__class__.__name__}: No json_dict provided.')
        self.stem_sample_name:str|None = None
        self.suffix_sample_name :str|None= None
        self.sample_comment:str|None = None
        self.list_ipc: list[dict[str,Any]] = []
        self.list_monit_tgt: list[dict[str,Any]] = []
        self.list_fio: list[dict[str,Any]] =[]
        self.__load_from_json_dict(json_dict)

    
    # def load_params_from_df(self, df: pd.DataFrame):
    #     """
    #     Loads necessary parameters from a DataFrame object.
    #     The header items must be in line with the definition the class Charging.
    #     The header items can be passed from the get_detail_header() of each UnitOperation-drived class.
    #     This is the overriding mehtod in the class Charging..
    #     """

    #     first_row = df.iloc[0]
    #     if not pd.isna(first_row[hedr_precomment]):
    #         self.pre_comment = first_row[hedr_precomment]
    #     if not pd.isna(first_row[hedr_postcomment]):
    #         self.post_comment = first_row[hedr_postcomment]
    #     for sample_seq, subitem in df.iterrows():
    #         temp_sample = SingleSample(flowsheet=self.flowsheet)
    #         temp_sample.load_from_series(caller=self, sample_seq=sample_seq, ser=subitem)
    #         self.list_samples.append(temp_sample)


    # def get_seq(self)-> int:
    #     return self.operation_seq
    
    # def get_detail_header(self) -> list[str]:
    #     return list_hedr

    # def get_detail_option_menu(self) -> Optional[dict[str, list[str]]]:
    #     return dict_dropdown
    
    # def print_unit_operation(self):
    #     # self.flowsheet.header_organizer(op_nr=self.operation_seq, title=lang_dict_uo_titles[self.uo_tag])
    #     self.flowsheet.header_organizer(title=lang_dict_uo_titles[self.uo_tag])

    #     if not (self.pre_comment == None or self.pre_comment == ''):
    #         self.flowsheet.put_body_comments(self.pre_comment)
    #         self.flowsheet.linefeed()        

    #     for sample in self.list_samples:
    #         sample.output_single_sample()
    #         self.flowsheet.linefeed()

    #     if not (self.post_comment == None or self.post_comment == ''):
    #         self.flowsheet.put_body_comments(self.post_comment)
    #         self.flowsheet.linefeed()

    def print_sample(self):
        def print_analytical_items(list_analysis:list[dict[str,Any]]=None):
            def comparator_to_str(item:str=None,
                                  analysis:dict[str, Any]=None)->str:
                val1 = analysis.get(key_criteria_val_1)
                comparator1 = analysis.get(key_comparator_1)
                val2 = analysis.get(key_criteria_val_2)
                comparator2 = analysis.get(key_comparator_2)                
                unit = analysis.get(key_unit_meas)

                if not unit:
                    unit=''
                str_this = ''
                if ((val1 is not None and comparator1) and not (val2 is not None and comparator2)
                    or (not(val1 is not None and comparator1) and (val2 is not None and comparator2))):
                    val = None
                    comp = None
                    if val1 is not None:
                        val = val1
                        comp = comparator1
                    else:
                        val = val2
                        comp = comparator2
                    if comp in [opt_comparator_equal, opt_comparator_match]:
                        str_this = item+dict_parts_stcs[comp]+str(val) + unit
                    elif comp == opt_comparator_lt:
                        str_this = item + dict_parts_stcs[tag_part_comparator_lt] + str(val) + unit
                    elif comp == opt_comparator_nmt:
                        str_this = item + dict_parts_stcs[tag_part_comparator_nmt] + str(val) + unit
                    elif comp == opt_comparator_nlt:
                        str_this = str(val) + unit + dict_parts_stcs[tag_part_comparator_nmt] + item
                    elif comp ==  opt_comparator_gt:
                        str_this = str(val) + unit + dict_parts_stcs[tag_part_comparator_lt] + item
                elif (val1 is not None and comparator1) and (val2 is not None and comparator2):
                    if comparator1 == opt_comparator_lt:
                        str_this = item + dict_parts_stcs[tag_part_comparator_lt] + str(val1) + unit
                    elif comparator1 == opt_comparator_nmt:
                        str_this = item + dict_parts_stcs[tag_part_comparator_nmt] + str(val1) + unit
                    elif comparator1 == opt_comparator_nlt:
                        str_this = str(val1) + unit + dict_parts_stcs[tag_part_comparator_nmt] + item
                    elif comparator1 ==  opt_comparator_gt:
                        str_this = str(val1) + unit + dict_parts_stcs[tag_part_comparator_lt] + item
                    if comparator2 == opt_comparator_lt:
                        str_this = str_this + dict_parts_stcs[tag_part_comparator_lt] + str(val2) + unit
                    elif comparator2 == opt_comparator_nmt:
                        str_this = str_this + dict_parts_stcs[tag_part_comparator_nmt] + str(val2) + unit
                    elif comparator2 == opt_comparator_nlt:
                        str_this = str(val2) + unit + dict_parts_stcs[tag_part_comparator_nmt] + str_this
                    elif comparator2 == opt_comparator_gt:
                        str_this = str(val2) + unit + dict_parts_stcs[tag_part_comparator_lt] + str_this
                
                return str_this

            def print_generic_analysis_item(template_attrbt:str=None, analysis:dict[str, Any]=None):
                #Template for method column: e.g., "IPC:{analysis_item}"
                #Analysis item: e.g., "compound-x転化率" or "99.0%≦compound-x転化率≦99.9%"
                #Finally, method colum component: e.g., "IPC:99.0%≦compound-x転化率≦99.9%"
                test_purpose = analysis.get(key_test_purpose)
                template_method_col:str=None
                method_col_component:str=None
                if test_purpose == opt_analysis_cat_ipc:
                    template_method_col = dict_parts_stcs[tag_stc_flow_ipc]
                    analysis_item_method = comparator_to_str(item=template_attrbt.replace('{analyte}', (analysis.get(key_analyte) or '')),
                                                              analysis=analysis)
                    method_col_component = template_method_col.replace('{analysis_item}', analysis_item_method)
                elif test_purpose == opt_analysis_cat_monit_tgt:
                    template_method_col = dict_parts_stcs[tag_stc_flow_monit_tgt]
                    analysis_item_method = comparator_to_str(item=template_attrbt.replace('{analyte}', (analysis.get(key_analyte) or '')),
                                                              analysis=analysis)
                    method_col_component = template_method_col.replace('{analysis_item}', analysis_item_method)
                elif test_purpose == opt_analysis_cat_fio:
                    template_method_col = dict_parts_stcs[tag_stc_flow_fio]
                    analysis_item_method = template_attrbt.replace('{analyte}', (analysis.get(key_analyte) or ''))
                    method_col_component = template_method_col.replace('{analysis_item}', analysis_item_method)

                #Record field e.g. "転化率____________%"
                unit = analysis.get(key_unit_meas)
                unit = unit if unit else ''
                analysis_item_rec = template_attrbt.replace('{analyte}','')
                record_conversion = dict_parts_stcs[tag_stc_flow_rec_analysis_result].format(analysis_item=analysis_item_rec, meas_unit=unit)

                self.flowsheet.put_line(content=method_col_component, record=record_conversion)
                if analysis.get(key_test_purpose) in [opt_analysis_cat_ipc, opt_analysis_cat_monit_tgt]:
                    self.flowsheet.put_line(record = dict_parts_stcs[tag_part_flow_rec_ok_nok])
            ############### functions inprint_analytical_items() till here #########################

            for analysis in list_analysis:
                if analysis.get(key_analysis_attribute) == opt_attrbt_conversion:
                    print_generic_analysis_item(template_attrbt=dict_parts_stcs[tag_stc_attrb_conversion], analysis=analysis)
                elif analysis.get(key_analysis_attribute) == opt_attrbt_rmnng_reactant:
                    print_generic_analysis_item(template_attrbt=dict_parts_stcs[tag_stc_attrb_rmnng_reactant], analysis=analysis)
                elif analysis.get(key_analysis_attribute) == opt_attrbt_imp_level:
                    print_generic_analysis_item(template_attrbt=dict_parts_stcs[tag_stc_attrb_imp_level], analysis=analysis)
                elif analysis.get(key_analysis_attribute) == opt_attrbt_ee:
                    print_generic_analysis_item(template_attrbt=dict_parts_stcs[tag_stc_attrb_ee], analysis=analysis)
                elif analysis.get(key_analysis_attribute) == opt_attrbt_de:
                    print_generic_analysis_item(template_attrbt=dict_parts_stcs[tag_stc_attrb_de], analysis=analysis)
                elif analysis.get(key_analysis_attribute) == opt_attrbt_water_cntnt:
                    print_generic_analysis_item(template_attrbt=dict_parts_stcs[tag_stc_attrb_water_cntnt], analysis=analysis)
                elif analysis.get(key_analysis_attribute) == opt_attrbt_pH:
                    print_generic_analysis_item(template_attrbt=dict_parts_stcs[tag_stc_attrb_pH], analysis=analysis)
                elif analysis.get(key_analysis_attribute) == opt_attrbt_extract_loss:
                    print_generic_analysis_item(template_attrbt=dict_parts_stcs[tag_stc_attrb_extract_loss], analysis=analysis)
                elif analysis.get(key_analysis_attribute) == opt_attrbt_resid_excess:
                    print_generic_analysis_item(template_attrbt=dict_parts_stcs[tag_stc_attrb_resid_excess], analysis=analysis)
                elif analysis.get(key_analysis_attribute) == opt_attrbt_solv_fraction:
                    print_generic_analysis_item(template_attrbt=dict_parts_stcs[tag_stc_attrb_solv_fraction], analysis=analysis)
                elif analysis.get(key_analysis_attribute) == opt_attrbt_tm_conc_pl:
                    print_generic_analysis_item(template_attrbt=dict_parts_stcs[tag_stc_attrb_tm_conc_pl], analysis=analysis)
                elif analysis.get(key_analysis_attribute) == opt_attrbt_tm_conc_ml:
                    print_generic_analysis_item(template_attrbt=dict_parts_stcs[tag_stc_attrb_tm_conc_ml], analysis=analysis)
                elif analysis.get(key_analysis_attribute) == opt_attrbt_cryst_form:
                    print_generic_analysis_item(template_attrbt=dict_parts_stcs[tag_stc_attrb_cryst_form], analysis=analysis)
                elif analysis.get(key_analysis_attribute) == opt_attrbt_filt_liq_indicator:
                    print_generic_analysis_item(template_attrbt=dict_parts_stcs[tag_stc_attrb_filt_liq_indicator], analysis=analysis)
                elif analysis.get(key_analysis_attribute) == opt_attrbt_filt_assay_tm:
                    print_generic_analysis_item(template_attrbt=dict_parts_stcs[tag_stc_attrb_filt_assay_tm], analysis=analysis)
                elif analysis.get(key_analysis_attribute) == opt_attrbt_lod:
                    print_generic_analysis_item(template_attrbt=dict_parts_stcs[tag_stc_attrb_lod], analysis=analysis)
                elif analysis.get(key_analysis_attribute) == opt_attrbt_resid_solv:
                    print_generic_analysis_item(template_attrbt=dict_parts_stcs[tag_stc_attrb_resid_solv], analysis=analysis)
                elif analysis.get(key_analysis_attribute) == opt_attrbt_particle_size:
                    print_generic_analysis_item(template_attrbt=dict_parts_stcs[tag_stc_attrb_particle_size], analysis=analysis)
                elif analysis.get(key_analysis_attribute) == opt_attrbt_other:
                    print_generic_analysis_item(template_attrbt=dict_parts_stcs[tag_stc_attrb_other], analysis=analysis)
                else:
                    warnings.warn(message=f'{self.__class__.__name__}.print_sample() Unknown attribute "{analysis.get(key_analysis_attribute)}".',
                                  category=RuntimeWarning)

        if self.sample_comment:
            self.flowsheet.put_body_comments(self.sample_comment)

        sample_name = self.stem_sample_name + (self.suffix_sample_name or '')
        self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                method=dict_parts_stcs[tag_part_flow_mthod_instr_sampling],
                                content=dict_parts_stcs[tag_stc_flow_content_sample_name].format(sample_name=sample_name),
                                record=dict_parts_stcs[tag_part_flow_rec_sampleID],
                                operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                witness=lang_dict_cmn[tag_flow_cmn_rec_sign])

        if self.list_ipc:
           print_analytical_items(list_analysis=self.list_ipc)
        if self.list_monit_tgt:
            print_analytical_items(list_analysis=self.list_monit_tgt)
        if self.list_fio:
            print_analytical_items(list_analysis=self.list_fio) 



    @staticmethod
    def get_json_schema(caller:trdef.UniversalTrait=None) -> Objason:
        class_sample = Primitive(prim_type='string',
                                 key=key_class_name,
                                 description=f'Constant. The name of the class "{const_class_sample}".',
                                 const=const_class_sample,
                                 required=True,
                                 nullable=False)
        stem_sample_name = Primitive(prim_type='string',
                                     key=key_stem_sample_name,
                                     description='Stem of the ample name.',
                                     nullable=False,
                                     required=True)
        suffix_sample_name = Primitive(prim_type='string',
                                       key=key_suffix_sample_name,
                                       description='Suffix of the sample name. Not necessarily required, but useful in some cases., '
                                       'For instance, samples are taken in a time series such as 1hr, 2hr... to trace the progress of the reaction. '
                                       'The same is true for drying. In such cases, time is a simple and comveninent suffix to identify a sample. '
                                       'In another case, "top", "middle", and "bottom" are used when multiple samples are taken from bulk.',
                                       nullable=True,
                                       required=False)
        comment = Primitive(prim_type='string',
                            key=key_sample_comment,
                            description='A commet(s) for the sample. Optional.',
                            required=False,
                            nullable=True)
        test_purpose = Primitive(prim_type='string',
                                 key=key_test_purpose,
                                 description='Purpose of the analysis. '
                                 f'"{opt_analysis_cat_ipc}": A decision about the operation is made based on the result of the analysis. '
                                 f'"{opt_analysis_cat_monit_tgt}": The analysis is done for the sake of process monitoring. Meanwhile a target value is set for that. '
                                 'Meeting the target value is deriable, but not a strict requirement. Not only the target value, but also various relevant conditions are took into consideration. '
                                 f'"{opt_analysis_cat_fio}" The analysis is done simply for the sake of process monitoring. No decision is made from the result.',
                                 enum=list_opt_analysis_purpose,
                                 nullable=False,
                                 required=True)
        test_attribute =  Primitive(prim_type='string',
                                    key=key_analysis_attribute,
                                    description='An attribute is a measurable or observable property of a material at a defined point in the process.\n'
                                    '- Always has a subject (the material/sample it belongs to). e.g., "residual THF in intermediate X" not just THF.\n'
                                    '- May refer to an analyte (THF, impurity-x), but some attributes have none (crystal form, particle size).\n'
                                    '- Is NOT:\n'
                                    '   - an analyte (THF itself is an analyte)\n'
                                    '   - a process parameter (temperature, addition rate are inputs)\n'
                                    '   - a test category (purity, residual solvents group attributes)\n'
                                    '   - a test method (HPLC, GC, NMR measure attributes)\n'
                                    f'"{opt_attrbt_conversion}": Conversion of the starting material. Normally associated with the starting material as the analyte. '
                                        f'"{opt_attrbt_rmnng_reactant}" can be used for the same purpose. Please select an attribute in a source-faithful manner.\n'
                                    f'"{opt_attrbt_rmnng_reactant}": Remaining reactant, e.g., starting material, intermediate, etc. Associated with the reactant as the analyte. '
                                        f'In the case the starting material is the reactant, "{opt_attrbt_conversion}" can be used for the same purpose. Please choose an attribute in a source-faithful manner.\n'
                                    f'"{opt_attrbt_imp_level}": Impurity level. Associated with a specified impurity as the analyte.\n'
                                    f'"{opt_attrbt_ee}": Enantiomeric excess. Normally associated with the target material as the analyte, but another compound can be an analyte.\n'
                                    f'"{opt_attrbt_de}": Diastereomeric excess. Normally associated with one of the diastereomers of the target compound, but another can be an analyte.\n'
                                    f'"{opt_attrbt_water_cntnt}": Water content in the sample. Water is always the analyte. Can be associated with the target material, process liquid, etc.\n'
                                    f'"{opt_attrbt_pH}": pH of the sample. Technically, analyte is hydroxonium ion. However, the analyte does not have to be specified, as pH can be regarded as physicochemical property of a solution.\n'
                                    f'"{opt_attrbt_extract_loss}": Loss of target compound during liquid-liquid washing or extraction, but not necessarily limited to them. '
                                        'In many cases, associated with the target material as an analyte. However, the starting material or intermediate can be the analyte if instructed by the process owner.\n'
                                    f'"{opt_attrbt_resid_excess}": Remaining level of excess reagent, building block, catalyst, etc., during quenching or purging. '
                                        'Normally the analytes are those excess compounds or the catalyst.\n'
                                    f'"{opt_attrbt_solv_fraction}": Fraction of a specific solvent in the process liquid. The specified solvent is the analyte.\n'
                                    f'"{opt_attrbt_tm_conc_pl}": Concentration of the target material in the process liquid. Sometimes, this value is required to determine the timing of seeding. '
                                        'Needless to say, the analyte is the target compound.\n'
                                    f'"{opt_attrbt_tm_conc_ml}": Concentration of the target material in the supernatant or filtrate in the recrystallization slurry. '
                                        'This can be needed to ensure the completion of recrystallization, or to monitor the product loss in the filtrate. '
                                        'Typical unit of measurment is mg/mL, but please follow the data source if specified.\n'
                                    f'"{opt_attrbt_cryst_form}": Crystal form. Various compounds can be the analyte, but in many cases, it is the target material. '
                                        'Sample can be crystals taken from the recrystallization slurry, wet cake of the filtration, the dry product, etc.\n'
                                    f'"{opt_attrbt_filt_liq_indicator}": An indicator of the crystal wash filtrate to monitor the progress of crystal washing. '
                                        'For example, conductivity, salt concentration, color, etc. Various compounds can be the analyte, or no analyte is specified if a physicochemical property is the indicator.\n'
                                    f'"{opt_attrbt_filt_assay_tm}": Assay of the target material in wet cake, dry product, etc. The target compound is the analyte.\n'
                                    f'"{opt_attrbt_lod}": Loss on drying of a sample. As this attribute is determined by the weight reduction of the material, no analyte is defined.\n'
                                    f'"{opt_attrbt_resid_solv}": Residual solvent level in the solid sample, i.e., wet cake or dry product, etc. '
                                        'Normally determined by means of gas chromatography. The analyte is the specified solvent. '
                                    f'For solvent composition of a process liquid, use "{opt_attrbt_solv_fraction}".\n'
                                    f'"{opt_attrbt_particle_size}": Particle size. Normally this is for the product powder, but not limited to it. '
                                        'Various particle size indicators, such as D10, D50, D90, etc.\n'
                                    f'"{opt_attrbt_other}": Attribute not mentioned earlier. Also in this case, the analyte can be designated if appropriate.\n',
                                    enum=list_opt_attrbt,
                                    nullable=False,
                                    required=True)
        analyte = Primitive(prim_type='string',
                            key=key_analyte,
                            description='Analyte of the analysis such as a specific solvent, e.g., THF, ethanol, water, etc., target compound, a specific impurity, and an unspecified impurity, etc. '
                            'Analyte is required in most of cases, but not always. For instance, if pH is the test attribute, it is regarded as a physicochemical property, and the analyte is not specified.',
                            nullable=True,
                            required=False)
        criteria_val_1 = Primitive(prim_type=['number','string'],
                              key=key_criteria_val_1,
                              description='Criteria value 1 for IPC or monitoring with a target. Either quantitative (interval scale or ratio scale; normally number type) '
                              'or qualitative (nominal scale; normally string type). '
                              'This is the primary criteria. For an IPC or monitoring with a target, this is a mandatory field. '
                              'If only one criteria is given, please put it in this property. '
                              f'Together with this property, please specify the "{key_comparator_1}" to specify the criteria.',
                              nullable=True,
                              required=False)
        criteria_comparator_1 = Primitive(prim_type='string',
                                          key=key_comparator_1,
                                          description=f'The comparator to specify the relationship between the actual analytical value and "{key_criteria_val_1}". Mandatory if the value is provided.\n'
                                          f'"{opt_comparator_equal}": The analytical result shall be equal to the specification value. This is for quantitative criteria.\n'
                                          f'"{opt_comparator_match}": The analytical result shall match the specification value. This is for qualitative criteria such as appearance, smell, taste, etc. \n'
                                          f'"{opt_comparator_lt}": The analytical result shall be less than the specification value.\n'
                                          f'"{opt_comparator_nmt}": The analytical result shall be not more than the specification value.\n'
                                          f'"{opt_comparator_nlt}": The analytical result shall be not less than the specification value.\n'
                                          f'"{opt_comparator_gt}": The analytical result shall be greater than the specification value.',
                                          enum=list_opt_comparator,
                                          required=False,
                                          nullable=True)
        criteria_val_2 = Primitive(prim_type=['number','string'],
                                   key=key_criteria_val_2,
                                   description='Criteria value 2 for IPC or monitoring with a target. Either quantitative (interval scale or ratio scale; normally number type) '
                                   'or qualitative (nominal scale; normally string type). '
                                   'For some IPC or monitoring with a target, this property is required. '
                                   'If a second parameter is specified please put it in this property, e.g., the upper limit of a range.'
                                   f'Together with this property, please specify the "{key_comparator_2}" between the result and the set value to specify the criteria.',
                                   nullable=True,
                                   required=False)
        criteria_comparator_2 = Primitive(prim_type='string',
                                          key=key_comparator_2,
                                          description=f'The comparator to specify the relationship between the actual analytical value and "{key_criteria_val_2}". Mandatory if the value is provided.\n'
                                          f'"{opt_comparator_equal}": The analytical result shall be equal to the specification value. This is for quantitative criteria.\n'
                                          f'"{opt_comparator_match}": The analytical result shall match the specification value. This is for qualitative criteria such as appearance, smell, taste, etc. \n'
                                          f'"{opt_comparator_lt}": The analytical result shall be less than the specification value.\n'
                                          f'"{opt_comparator_nmt}": The analytical result shall be not more than the specification value.\n'
                                          f'"{opt_comparator_nlt}": The analytical result shall be not less than the specification value.\n'
                                          f'"{opt_comparator_gt}": The analytical result shall be greater than the specification value.',
                                          enum=list_opt_comparator,
                                          required=False,
                                          nullable=True)
        unit = Primitive(prim_type='string',
                         key=key_unit_meas,
                         description='Unit of measurement for the analysis.',
                         nullable=True,
                         required=False)
        single_analysis = Objason(key=key_obj_analysis,
                                  props=[test_purpose, test_attribute, analyte, criteria_val_1, criteria_comparator_1, criteria_val_2, criteria_comparator_2, unit],
                                  description='Object for a single analysis.',
                                  required=True,
                                  nullable=False)
        arr_analysis = Array(key=key_arr_analysis,
                             content=single_analysis,
                             description='An array of single analysis belonging to a sample.',
                             required=False,
                             nullable=None)
        obj_sample = Objason(key=key_obj_sampe,
                             props=[class_sample, stem_sample_name, suffix_sample_name, comment, arr_analysis],
                             description='An object for a sample. Sample has (stem and optional suffix for) a name and an optional array of analysis.',
                             required=True,
                             nullable=False)
        
        return obj_sample
        

    def __load_from_json_dict(self, json_dict:dict[str, Any]):
        def sort_transf_analysis(orig:list[dict[str, Any]]=None, dest:list[dict[str, Any]]|None=None):
            if orig is None:
                return

            if dest is None:
                return
            
            for attr in list_opt_attrbt:
                matched = []
                for i in range(len(orig)-1, -1, -1):
                    analysis = orig[i]
                    if attr == analysis.get(key_analysis_attribute):
                        matched.append(orig.pop(i))
                dest.extend(reversed(matched))
            if orig:
                for element in orig:
                    warnings.warn(message=f'{self.__class__.__name__}.__load_from_json_dict(): unknown attribute "{element.get(key_analysis_attribute)}"',
                                  category=RuntimeWarning)
                        
        if json_dict.get(key_class_name) != const_class_sample:
            warnings.warn(message=f'{self.__class__.__name__}.__load_from_json_dict(): The json_dictionary doesn\'t include the constant for the object name "{const_class_sample}".',
                          category=RuntimeWarning)
        self.stem_sample_name = json_dict.get(key_stem_sample_name)
        if not self.stem_sample_name:
            self.stem_sample_name = '<placeholder:samplename>'
            warnings.warn(message=f'{self.__class__.__name__}.__load_from_json_dict(): No sample name stem is provided.',
                          category=RuntimeWarning)
        self.suffix_sample_name = json_dict.get(key_suffix_sample_name)
        self.sample_comment = json_dict.get(key_sample_comment)
        arr_analysis = json_dict.get(key_arr_analysis)
        if arr_analysis:
            buf_list_ipc:list[dict[str, Any]] = []
            buf_list_monit_tgt:list[dict[str, Any]] = []
            buf_list_fio:list[dict[str, Any]] = []
            for single_analysis in arr_analysis:
                purpose = single_analysis.get(key_test_purpose)
                if purpose == opt_analysis_cat_ipc:
                    buf_list_ipc.append(single_analysis)
                elif purpose == opt_analysis_cat_monit_tgt:
                    buf_list_monit_tgt.append(single_analysis)
                elif purpose == opt_analysis_cat_fio:
                    buf_list_fio.append(single_analysis)
            sort_transf_analysis(orig=buf_list_ipc, dest=self.list_ipc)
            sort_transf_analysis(orig=buf_list_monit_tgt, dest=self.list_monit_tgt)
            sort_transf_analysis(orig=buf_list_fio, dest=self.list_fio)


    # @staticmethod
    # def generate_test_df(sample_name:str = None,
    #                      sampling_cat:str = None,
    #                      ipc_criteria:str = None,
    #                      ipc_rec_titles:str = None,
    #                      ipc_rec_units:str = None,
    #                      monit_items:str = None,
    #                      monit_rec_items:str = None,
    #                      monit_rec_units:str = None,
    #                      sample_comment:str = None
    #                      )->pd.DataFrame:
    #     hedr:list[str] = defs.list_hedr_cmn_io_dtil + list_hedr
    #     content: list[any] = [None]*len(hedr)
    #     s:pd.Series = pd.Series(data=content, index=hedr)
    #     df = s.to_frame().T
    #     df.at[df.index[0], hedr_sample_name] = sample_name
    #     df.at[df.index[0], hedr_sampling_cat] = sampling_cat
    #     df.at[df.index[0], key_criteria_val_1] = ipc_criteria
    #     df.at[df.index[0], hedr_ipc_rec_titles] = ipc_rec_titles
    #     df.at[df.index[0], hedr_ipc_rec_units] = ipc_rec_units
    #     df.at[df.index[0], hedr_monit_item_high] = monit_items
    #     df.at[df.index[0], hedr_monit_rec_items] = monit_rec_items
    #     df.at[df.index[0], hedr_monit_rec_units] = monit_rec_units
    #     df.at[df.index[0], hedr_sample_comment] = sample_comment

    #     return df
    
    # @staticmethod
    # def add_to_test_df(df: pd.DataFrame=None,
    #                    sample_name:str = None,
    #                    sampling_cat:str = None,
    #                    ipc_criteria:str = None,
    #                    ipc_rec_titles:str = None,
    #                    ipc_rec_units:str = None,
    #                    monit_items:str = None,
    #                    monit_rec_items:str = None,
    #                    monit_rec_units:str = None,
    #                    sample_comment:str = None
    #                    )->None:
    #     width:int = len(df.columns)
    #     new_row:list[any] = [None]*width
    #     row:int = len(df)
    #     df.loc[row]=new_row
    #     df.at[row, hedr_sample_name] = sample_name
    #     df.at[row, hedr_sampling_cat] = sampling_cat
    #     df.at[row, key_criteria_val_1] = ipc_criteria
    #     df.at[row, hedr_ipc_rec_titles] = ipc_rec_titles
    #     df.at[row, hedr_ipc_rec_units] = ipc_rec_units
    #     df.at[row, hedr_monit_item_high] = monit_items
    #     df.at[row, hedr_monit_rec_items] = monit_rec_items
    #     df.at[row, hedr_monit_rec_units] = monit_rec_units
    #     df.at[row, hedr_sample_comment] = sample_comment


            





        
