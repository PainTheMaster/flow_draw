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
from flow_draw.data_io.json_io import Primitive, Objason, Array 
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

hedr_equip = "Filtering Equipment"
"""Header item for filtering equipment"""
hedr_Tj_setpoint = "Tj set point"
"""Header item for Tj of the filtering device"""
hedr_press_min = "Filt P_min"
"""Header item for minimum filtration pressure"""
hedr_press_max = "Filt P_max"
"""Header item for maximum filtration pressure"""
hedr_unit_press = "Pressure Unit"
"""Header item for pressure """
hedr_integ_test = "Need_integrity_test"
"""Header item for integrity test"""
list_hedr = [hedr_equip,
             hedr_Tj_setpoint,
             hedr_press_min,
             hedr_press_max,
             hedr_unit_press,
             hedr_integ_test]


#########################################################
# UO-specific options, list, header_item: list dictionry thereof (for data input and internalsignaling)
#########################################################

opt_hedr_press_kPa = defs.opt_press_kPa
"""option for the deader item for hedr_unit_press: kPa"""
opt_hedr_press_MPa = defs.opt_press_MPa
"""option for the deader item for hedr_unit_press: MPa"""
list_opt_unit_press = [opt_hedr_press_kPa, opt_hedr_press_MPa]
"""list of options for the heder item hedr_unit_press"""

opt_integ_test_yes = defs.opt_yes
"""option for the header item for hedr_integ_test; Yes"""
opt_integ_test_no = defs.opt_no
"""option for the header item for hedr_integ_test; No"""
list_opt_integ_test = defs.list_yesno
"""List of options for the hdeader item hedr_integ_test"""

dict_filt_drpdwn = {hedr_unit_press : list_opt_unit_press,
                    hedr_integ_test : list_opt_integ_test}
"""drop-down list items for header items"""


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

tag_part_flow_method_integ_test = "method integ test"
"""tag for a flowsheet component: method column, integrity test"""
part_flow_method_integ_test_jp="漏れ確認"
"""a flowsheet component: method column, integrity test"""
tag_part_flow_chk_Tj_setpoint = "check-box Tj set point"
"""tag for a flowsheet component: check-box for the Tj set point"""
part_flow_chk_Tj_setpoint_jp="□ 設定値確認"
"""a flowsheet component: check-box for the Tj set point"""
tag_part_flow_chk_integ_test = "tag chk box integ test"
"""tag for a flowsheet component: check-box for filer integrity test"""
part_flow_chk_integ_test_jp = "□ 漏れ確認"
"""a flowsheet component: check-box for filer integrity test"""

tag_part_flow_content_integ_test_2 = "instr stc filt integ test 2nd prt"
"""tag for a flowsheet component: content column, integrity test part 2; in the case of leak"""
part_flow_content_integ_test_2_jp="漏れがあった場合は設備洗浄し、ろ布を交換後再確認する。"
"""a flowsheet component: content column, integrity test part 2; in the case of leak"""

tag_part_flow_method_instr_start = "instr filt start"
"""tag for a flowsheet component: method column, instruction to start filtration"""
part_flow_method_instr_start_jp="開始"
"""a flowsheet component: method column, instruction to start filtration"""

tag_part_flow_method_instr_end = "instr filt end"
"""tag for a flowsheet component: method column, instruction to end filtration"""
part_flow_method_instr_end_jp="終了"
"""a flowsheet component: method column, instruction to end filtration"""

tag_part_flow_press_arbitrary = "instruction arbit filt press"
"""tag for a flowsheet component: content column, instruction for an arbitrary filtration pressure"""
part_flow_press_arbitrary_jp="圧力:現場調整"
"""a flowsheet component: content column, instruction for an arbitrary filtration pressure"""

tag_part_flow_rec_cake_height = "rec cake height"
"""tag for a flowsheet component: record field for the filter cake height"""
part_flow_rec_cake_height_jp="ケーク高さ:____________cm"
"""a flowsheet component: record field for the filter cake height"""

tag_stc_flow_instr_equipment = "stc instr equip"
"""tag for an instruction sentence template: instruction to use a specific equipment; includes a placeholder {equipment}"""
stc_flow_instr_equipment_jp = "機器:{equipment}"
"""an instruction sentence template: instruction to use a specific equipment; includes a placeholder {equipment}"""

tag_stc_flow_instr_Tj_setpoint = "stc instr filt Tj"
"""tag for an instruction sentence template: instruction to set Tj; includes a placeholder {Tj}"""
stc_flow_instr_Tj_setpoint_jp = "外温設定:{Tj}℃"
"""an instruction sentence template: instruction to set Tj; includes a placeholder {Tj}"""

tag_stc_flow_content_instr_integ_test_1 = "stc instr filt integ test 1 prt"
"""tag for an instruction sentence template: 1st part of filter integrity test. includes a tag {equip}"""
stc_flow_content_instr_integ_test_1_jp = "スラリーを{equip}に少量送液し目視にて結晶の漏れがないことを確認する。"
"""an instruction sentence template: 1st part of filter integrity test. includes a tag {equip}"""

tag_stc_flow_press_range = "instruct stc template press range"
"""tag for an instruction sentence template: pressure range; includes placeholder {P_min}, {P_max}, and {P_unit}"""
stc_flow_press_range_jp = "圧力:{P_min}~{P_max} {P_unit}"
"""an instruction sentence template: pressure range; includes placeholder {P_min}, {P_max}, and {P_unit}"""

tag_stc_flow_press_single = "instruct stc template press range"
"""tag for an instruction sentence template: single point pressure; includes placeholder {P} and {P_unit}"""
stc_flow_press_single_jp = "圧力目安:{P} {P_unit}"
"""an instruction sentence template: single point pressure; includes placeholder {P} and {P_unit}"""

tag_stc_flow_press_min = "instruct stc template min press"
"""tag for an instruction sentence template: minimum pressure; includes placeholder {P_min} and {P_unit}"""
stc_flow_press_min_jp = "圧力:{P_min} {P_unit}以下"
"""An instruction sentence template: minimum pressure includes; tags {P_min} and {P_unit}"""

tag_stc_flow_press_max = "instruct stc template max press"
"""tag for an instruction sentence template: maximum pressure; includes placeholder {P_max} and {P_unit}"""
stc_flow_press_max_jp = "圧力:{P_max} {P_unit}以上"
"""An instruction sentence template: maximum pressure includes; tags {P_max} and {P_unit}"""

tag_stc_flow_rec_pres = "rec filt press"
"""tag for a sentence template: record field for filtration pressure; includes placeholders {P_unit}"""
stc_flow_rec_press_jp = "圧力:__________{P_unit}"
"""a sentence template: record field for filtration pressure; includes placeholders {P_unit}"""

dict_flowsheet_comp_jp = {tag_part_flow_method_integ_test : part_flow_method_integ_test_jp,
                          tag_part_flow_chk_Tj_setpoint : part_flow_chk_Tj_setpoint_jp,
                          tag_part_flow_chk_integ_test : part_flow_chk_integ_test_jp,
                          tag_part_flow_content_integ_test_2 : part_flow_content_integ_test_2_jp,
                          tag_part_flow_method_instr_start : part_flow_method_instr_start_jp,
                          tag_part_flow_method_instr_end : part_flow_method_instr_end_jp,
                          tag_part_flow_press_arbitrary : part_flow_press_arbitrary_jp,
                          tag_part_flow_rec_cake_height : part_flow_rec_cake_height_jp,
                          tag_stc_flow_instr_equipment : stc_flow_instr_equipment_jp,
                          tag_stc_flow_instr_Tj_setpoint : stc_flow_instr_Tj_setpoint_jp,
                          tag_stc_flow_content_instr_integ_test_1 : stc_flow_content_instr_integ_test_1_jp,
                          tag_stc_flow_press_range : stc_flow_press_range_jp,
                          tag_stc_flow_press_single : stc_flow_press_single_jp,
                          tag_stc_flow_press_min : stc_flow_press_min_jp,
                          tag_stc_flow_press_max : stc_flow_press_max_jp,
                          tag_stc_flow_rec_pres : stc_flow_rec_press_jp}

dict_flowsheet_comp = dict_flowsheet_comp_jp

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
class Filtration(uo.UnitOperation, uo_tag=defs.tag_uo_filt):
    def __init__(self,
                 caller: type[trdef.UniversalTrait] =None,
                 flowsheet:fsht.Flowsheet=None,
                 operation_seq: int=None,
                 num_subitems: int = None,
                 edit_comment:str=None):
        super().__init__(caller=caller, flowsheet=flowsheet, operation_seq=operation_seq, num_subitems=num_subitems, edit_comment=edit_comment)
        self.equipment:str = None
        self.Tj_setpoint:float = None
        self.press_min:float = None
        self.press_max:float = None
        self.unit_press:str = None
        self.integ_test:bool = False
    
    def get_json_schema(caller:trdef.UniversalTrait = None):
        cmn_schema = Filtration.json_common()
        filt_device = Primitive(prim_type='string',
                                key = hedr_equip,
                                description = 'Please designate the filterin device for the operation. This property is required and not nullable. '
                                'If a right name is no found in the given set of information, please put "<Placeholder>" here.')
        temp_jacket = Primitive(prim_type = 'number',
                                key = hedr_Tj_setpoint,
                                description = 'Please designate the Tj set point for the filtration device. This property is optional and nullable.',
                                nullable=True)
        press_min = Primitive(prim_type = 'number',
                              key = hedr_press_min,
                              description = 'Please designate the minimum pressure for the filtration operation. This property is optional and nullable. '
                              'Please follow the information on the given flowsheet',
                              nullable=True)
        press_max = Primitive(prim_type = 'number',
                              key = hedr_press_max,
                              description = 'Please designate the maximum pressure for the filtration operation. This property is optional and nullable.'
                              'Please follow the information on the given flowsheet',
                              nullable=True)
        press_unit = Primitive(prim_type='string',
                               key=hedr_unit_press,
                               enum= list_opt_unit_press,
                               description=f'Pressure unit to designate the pressure for the filtration operation. '
                               f'This property is mandatory if either of "{hedr_press_min}" or "{hedr_press_max}" has a non-null value.',
                               nullable=True)
        integ_test = Primitive(prim_type='boolean',
                               key=hedr_integ_test,
                               description='Please designate whether the integrity test is required for the filtration operation.')
        obj_filtration = Objason(key=Filtration.uo_tag,
                                 props=cmn_schema + [filt_device, temp_jacket, press_min, press_max, press_unit, integ_test],
                                 description='This object describes the filtration operation in the process flowsheet.')
        return obj_filtration
        
    def load_from_json_dict(self, json_dict):
        super().load_from_json_dict(json_dict)
        self.equipment = json_dict.get(hedr_equip, None)
        self.Tj_setpoint = json_dict.get(hedr_Tj_setpoint, None)
        self.press_min = json_dict.get(hedr_press_min, None)
        self.press_max = json_dict.get(hedr_press_max, None)
        self.unit_press = json_dict.get(hedr_unit_press, None)
        self.integ_test = json_dict.get(hedr_integ_test, None)
        print(f'self.integ_test: {self.integ_test} (type: {type(self.integ_test)})')


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
        if not pd.isna(first_row[hedr_equip]):
            self.equipment = first_row[hedr_equip]
        else:
            raise ValueError(f"{self.__class__.__name__} Op. Seq. {self.operation_seq}: No filtration equipment specified in the process detail form.")
        if not pd.isna(first_row[hedr_Tj_setpoint]):
            self.Tj_setpoint = first_row[hedr_Tj_setpoint]
        if not pd.isna(first_row[hedr_press_min]):
            self.press_min = first_row[hedr_press_min]
        if not pd.isna(first_row[hedr_press_max]):
            self.press_max = first_row[hedr_press_max]
        if not pd.isna(first_row[hedr_unit_press]):
            self.unit_press = first_row[hedr_unit_press]
        elif self.press_min is not None or self.press_max is not None:
            raise ValueError(f"{self.__class__.__name__} Op. Seq. {self.operation_seq}: No filtration pressure unit is provided although P_min and/or P_max are specified.")
        if first_row[hedr_integ_test]==opt_yes:
            self.integ_test = True

    def get_detail_header(self) -> list[str]:
        return list_hedr

    def get_detail_option_menu(self) -> Optional[dict[str, list[str]]]:
        return dict_filt_drpdwn
    



    def output_unit_operation(self):
        self.flowsheet.header_organizer(op_nr=self.operation_seq, title=lang_dict_uo_titles[self.uo_tag])
        if not (self.pre_comment == None or self.pre_comment == ''):
            self.flowsheet.put_body_comments(self.pre_comment)
            self.flowsheet.linefeed()        

        self.flowsheet.put_line(content=dict_flowsheet_comp[tag_stc_flow_instr_equipment].format(equipment = self.equipment))
        if self.Tj_setpoint is not None:
            self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                    content=dict_flowsheet_comp[tag_stc_flow_instr_Tj_setpoint].format(Tj=self.Tj_setpoint),
                                    record=dict_flowsheet_comp[tag_part_flow_chk_Tj_setpoint],
                                    operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
        self.flowsheet.linefeed()

        if self.integ_test:
            self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                    method=dict_flowsheet_comp[tag_part_flow_method_integ_test],
                                    content=dict_flowsheet_comp[tag_stc_flow_content_instr_integ_test_1].format(equip=self.equipment),
                                    record=dict_flowsheet_comp[tag_part_flow_chk_integ_test],
                                    operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
            self.flowsheet.put_line(content=dict_flowsheet_comp[tag_part_flow_content_integ_test_2])
            self.flowsheet.linefeed()

        stc_pres:str = None
        if self.press_min is not None and self.press_max is not None:
            if self.press_min != self.press_max:
                stc_pres = dict_flowsheet_comp[tag_stc_flow_press_range].format(P_min=self.press_min, P_max=self.press_max, P_unit=self.unit_press)
            else:
                stc_pres = dict_flowsheet_comp[tag_stc_flow_press_single].format(P=self.press_min , P_unit=self.unit_press)
        elif self.press_min is not None:
            stc_pres = dict_flowsheet_comp[tag_stc_flow_press_min].format(P_min=self.press_min, P_unit=self.unit_press)
        elif self.press_max is not None:
            stc_pres = dict_flowsheet_comp[tag_stc_flow_press_max].format(P_max=self.press_max, P_unit=self.unit_press)
        else:
            stc_pres = dict_flowsheet_comp[tag_part_flow_press_arbitrary]
        
        temp_press_unit:str = None
        if self.unit_press is not None:
            temp_press_unit = self.unit_press
        else:
            temp_press_unit = opt_hedr_press_MPa

        self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                method=dict_flowsheet_comp[tag_part_flow_method_instr_start],
                                content=stc_pres,
                                record=dict_flowsheet_comp[tag_stc_flow_rec_pres].format(P_unit=temp_press_unit),
                                operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
        self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                method=dict_flowsheet_comp[tag_part_flow_method_instr_end],
                                record=dict_flowsheet_comp[tag_part_flow_rec_cake_height],
                                operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                witness=lang_dict_cmn[tag_flow_cmn_rec_sign])        

        if not (self.post_comment == None or self.post_comment == ''):
            self.flowsheet.put_body_comments(self.post_comment)
            self.flowsheet.linefeed()
    
    @classmethod
    def generate_test_df(cls,
                       equipment:str = None,
                       Tj:float = None,
                       P_min:float = None,
                       P_max:float = None,
                       P_unit:str = None,
                       integ_test:str = None)->pd.DataFrame:
        hedr:list[str] = defs.list_hedr_cmn_io_dtil + list_hedr
        content: list[any] = [None]*len(hedr)
        s:pd.Series = pd.Series(data=content, index=hedr)
        df = s.to_frame().T
        df.at[df.index[0], hedr_equip]=equipment
        df.at[df.index[0], hedr_Tj_setpoint]=Tj
        df.at[df.index[0], hedr_press_min]=P_min
        df.at[df.index[0], hedr_press_max]=P_max
        df.at[df.index[0], hedr_unit_press]=P_unit
        df.at[df.index[0], hedr_integ_test]=integ_test

        return df
    
