import pandas as pd
import json
import flow_draw.definitions as defs
import warnings
from typing import Optional
from flow_draw.batch.process.unit_operations import unit_operation as uo
from flow_draw.data_io import process_io
from flow_draw.materials import materials as mats
# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
from flow_draw.data_io.flowsheet import Flowsheet
# import flow_draw.data_io.flowsheet as fsht
from flow_draw.trait_def.trait_def import GetMats, GetInputs
from flow_draw.data_io.json_io import Objason, Primitive, Array
from flow_draw.batch.process.unit_operations.material_input import *  # Input and its constants; kept importable as chgng.<name> for existing callers


header_precomment = defs.hedr_cmn_io_dtil_precmnt #Don't include this in the specific header list!!!
header_postcomment = defs.hedr_cmn_io_dtil_postcmnt #Don't include this in the specific header list!!!


#List below
list_header_items = [hedr_material_name,
                     hedr_metrics_value,
                     hedr_metrics_unit,
                     hedr_error_pct,
                     hedr_method,
                     hedr_time_control,
                     hedr_time_min,
                     hedr_time_max,
                     hedr_temp_control,
                     hedr_temp_min,
                     hedr_temp_max]

arry_inputs_json = 'arr_charging_input_entry'
"""The key to a list of material input entries."""

# obj_charging_json = 'charging_stage'
"""The key to the unit operation of charging."""


dict_dtil_drpdwn = {hedr_metrics_unit : list_metrics_unit,
                    hedr_method : list_charging_method,
                    hedr_time_control : list_time_control,
                    hedr_temp_control : list_temp_control}
"""The dict[str, list[str]] for drop-down lists for detail input"""


#Language dictionary for unit operation title. Although only 'charging is needed'
lang_dict_uo_titles = defs.dict_jp_part_uo_titles

#Tags for translation of common parts 
tag_flow_cmn_rec_time = defs.tag_flow_cmn_rec_time
tag_flow_cmn_rec_sign = defs.tag_flow_cmn_rec_sign
#language dictionary for common flowsheet items
lang_dict_cmn = defs.dict_jp_part_flow_cmn
"""
tag_flow_cmn_rec_time : part_flow_cmn_rec_time_jp,
tag_flow_cmn_rec_sign : part_flow_cmn_rec_sign_jp
"""

#Tags for translation of UO-specific parts
tag_part_instr_ini = "tag_chgng_instr_ini"
# part_instr_ini_jp = '仕込み開始'
"""Flowseet component for class Charging. An action item of commencement of charging/dosing"""
tag_part_instr_end = "tag_chgng_instr_end"
# part_instr_end_jp = '仕込み終了'
"""Flowseet component for class Charging. An action item of end of charging/dosing"""
tag_part_rec_qyt_input = "tag_chgng_rec_input"
# part_rec_input_jp = '仕込み量__________kg'
"""Flowseet component for class Charging. A recording element for dispensed amount"""
tag_part_rec_lot = "tag_chgng_rec_lot"
# part_rec_lot_jp = 'ロット番号__________'
"""Flowseet component for class Charging. A recording element for the lot number of a material"""

tag_part_rec_balance_id = "tag_chgng_rec_ID_balance"
"""Flowsheet component for class Charging. A recording element for the ID of the balance."""
#TODO: Please implement the printing logic of the balance ID record.

tag_part_rec_cntnr_id = 'tag_chgng_rec_ID_container'
"""Flowsheet component for class Charging. A recording element for the ID of liquid containers."""
tag_part_rec_hose = "tag_chgng_rec_ID_hose"
# part_rec_hose_jp ='フレキID__________'
"""Flowseet component for class Charging. A recording element for the ID of flexible hose for solvents"""
tag_part_rec_temprini = "tag_chgng_rec_temprini"
# part_rec_temprini_jp = '開始時内温_______℃'
"""Flowseet component for class Charging. A recording element for initial temperature of a certain action"""
tag_part_rec_temprmax = "tag_chgng_rec_temprmax"
# part_temprmax_jp = '仕込み時最高内温_______℃'
"""Flowseet component for class Charging. A recording element for the maximum temperature"""
tag_part_rec_temprmin = "tag_chgng_rec_temprmin"
# part_temprmin_jp = '仕込み時最低内温_______℃'
"""Flowseet component for class Charging. A recording element for the minimum"""
tag_part_rec_temprend = "tag_chgng_rec_temprend"
# part_temprend_jp = '終了時内温_______℃'
"""Flowseet component for class Charging. A recording element for the terminal temperature"""
tag_part_rec_cmpltd = "tag_chgng_rec_cmpltd"
# part_cmpltd_jp ='□ 仕込み実施'
"""Flowseet component for class Charging. A check box for complete charging/dosing"""

tag_part_mthd_liq = method_liq
# part_mthd_liq_jp = "液体投入口"
"""Flowsheet component for class Charging. Charging through liquid charging port. An ption for Liquid charging."""
tag_part_mthd_shower = method_shower
# part_mthd_shower_jp = "常設シャワー"
"""Flowsheet component for class Charging. Charging through the fixed shower. An ption for Liquid charging."""
tag_part_mthd_prssvesl = method_press
# part_mthd_prssvesl_jp = "圧送容器"
"""Flowsheet component for class Charging. Charging from a pressure vessel. An ption for Liquid charging."""
tag_part_mthd_mobile_tank = method_mobile_tank
# part_mthd_mobile_tank_jp = "液体コンテナ"
"""Flowsheet component for class Charging. Charging from a mobile tank. An option for large volume liquid charging."""
tag_part_mthd_pwdr = method_pow
# part_mthd_pwdr_jp = "粉体投入口"
"""Flowsheet component for class Charging. Charging through the power port. An ption for powder charging."""
tag_part_mthd_plchldr = method_placeholder
# part_mthd_plchldr_jp = "<Placeholder: charging method>"
"""Flowsheet component for class Charging. A place holder. An ption for Liquid charging."""
tag_part_instr_timectrl_plchldr = 'input_time_control_placeholder'
"""Flowsheet component for class Charging. A placeholdr for time control. """
tag_part_instr_temprctrl_plchldr = 'input_temperature_control_placeholder'
"""Flowsheet component for class Charging. A placeholdr for temperature control. """



dict_jp_parts={tag_part_instr_ini : '仕込み開始',
                tag_part_instr_end : '仕込み終了',
                tag_part_rec_qyt_input : '仕込み量__________kg',
                tag_part_rec_lot : 'ロット番号__________',
                tag_part_rec_balance_id : '秤量器ID__________', #TODO: Please implement the printing logic of the balance ID record.
                tag_part_rec_cntnr_id : '容器ID__________',
                tag_part_rec_hose : 'フレキID__________',
                tag_part_rec_temprini : '開始時内温_______℃',
                tag_part_rec_temprmax : '仕込み時最高内温_______℃',
                tag_part_rec_temprmin : '仕込み時最低内温_______℃',
                tag_part_rec_temprend : '終了時内温_______℃',
                tag_part_rec_cmpltd :'□ 仕込み実施',
                tag_part_mthd_liq : "液体投入口",
                tag_part_mthd_shower : "常設シャワー",
                tag_part_mthd_prssvesl : "圧送容器",
                tag_part_mthd_mobile_tank : "液体コンテナ",
                tag_part_mthd_pwdr : "粉体投入口",
                tag_part_mthd_plchldr : "<Placeholder: charging method>",
                tag_part_instr_timectrl_plchldr : "<Placeholder: time control>",
                tag_part_instr_temprctrl_plchldr : '<Placeholder: temperature control>'
                }

#Language dictionary for the unit operation
lang_dict_chgng_specif = dict_jp_parts


tag_stc_qty = "tag_stc_qty"
"""Keyword to retrieve a dosing instruction sentence for dosed quantity"""
tag_stc_time_min = timectrl_min
"""Keyword to retrieve a dosing instruction sentence with minimum time limit from multilingual dictionaries"""
tag_stc_time_max = timectrl_max
"""Keyword to retrieve a dosing instruction sentence with maximum time limit from multilingual dictionaries"""
tag_stc_time_min_max = timectrl_min_max
"""Keyword to retrieve a dosing instruction sentence with time limit range from multilingual dictionaries"""
tag_stc_temp_min = temprctrl_min
"""Keyword to retrieve a dosing instruction sentence with minimum temperature limit from multilingual dictionaries"""
tag_stc_temp_max = temprctrl_max
"""Keyword to retrieve a dosing instruction sentence with maximum temperature limit from multilingual dictionaries"""
tag_stc_temp_min_max = temprctrl_min_max
"""Keyword to retrieve a dosing instruction sentence with temperature limit range from multilingual dictionaries"""


dict_jp_stcs={tag_stc_qty : '{qty}±{err} kg',
              tag_stc_time_min : '*滴下時間{min}分以上',
              tag_stc_time_max : '*滴下時間{max}分以内',
              tag_stc_time_min_max : '*滴下時間{min}～{max}分以内',
              tag_stc_temp_min : "仕込み中内温{min}℃以上",
              tag_stc_temp_max : "仕込み中内温{max}℃以下",
              tag_stc_temp_min_max : "仕込み中内温{min}～{max}℃"}

lang_dict_instr_stcs = dict_jp_stcs
"""A language dictionary for a instruction sentence with time or temperature limit. Use str.format(min and/or max) to pur an appropriate parameter"""


class Charging(uo.UnitOperation, uo_tag=defs.tag_uo_charging):
    """
    TODO: Make some comment here.
    """
    
    def __init__(self, caller: GetMats|GetInputs=None, flowsheet:"Flowsheet"=None, operation_seq:int=None, num_subitems: int =None, edit_comment:str=None):
        """
        Initialises the newly created instance of the class Charging.

        Parameters
        ---------------
        caller: flow_draw.trait_def.trait_def.GetMats
            The calling object. In the case of the class Charging, GetMats class is expected. From the given caller object, Charging expects materials.Materials passed by get_mats() method.
        """
        super().__init__(caller=caller, flowsheet=flowsheet, operation_seq=operation_seq, num_subitems=num_subitems, edit_comment=edit_comment)
        self.mats_data: mats.Materials = None
        if caller is not None:
            self.mats_data = (self.caller).get_mats()
        self.input_count = 0
        self.list_inputs: list[Input] = []

        #self.output_unit_operation()

    def get_detail_header(self) -> list[str]:
        return list_header_items
    
    def get_detail_option_menu(self) -> Optional[dict[str, list[str]]]:
        return dict_dtil_drpdwn

    def load_params_from_df(self, df: pd.DataFrame):
        """
        Loads necessary parameters from a DataFrame object.
        The header items must be in line with the definition the class Charging.
        The header items can be passed from the get_detail_header() of each UnitOperation-derived class.
        This is the overriding mehtod in the class Charging.
        """
        first_row = df.iloc[0]
        if not pd.isna(first_row[header_precomment]):
            self.pre_comment = first_row[header_precomment]
        if not pd.isna(first_row[header_postcomment]):
            self.post_comment = first_row[header_postcomment]
        for _, subitem in df.iterrows():
            #mats_data contains information for all the materials used in the process. At the moment, newly created Material instance has not been differentiated.
            new_input = Input(mats_data=self.mats_data)
            #each line of the df = each input material, now, the Material instance is unique in terms of the content.
            new_input.load_params_from_series(subitem)
            self.list_inputs.append(new_input)
            self.input_count += 1

    @staticmethod
    def get_json_schema(caller: GetMats=None)-> Objason:
        common=Charging.json_common()        
        input_entry = Input.get_json_schema(caller=caller)
        arr_input = Array(key=arry_inputs_json,
                          content=input_entry,
                          description='A list of material input entries. A single material or more is put in the reactor vessel in a charging/dosing stage.',
                          required=True)
        charging_dosing = Objason(key=Charging.uo_tag,
                                  props=common+[arr_input],
                                  description='This object corresponds to a unit operation of charging/dosing which appears as a single block on the flowsheet. '
                                    'One or more material(s) are dosed/charged into the reaction vessel.',
                                  required=False)
        return charging_dosing
        


    def load_from_json_dict(self, json_dict: dict[str, any]):
        super().load_from_json_dict(json_dict=json_dict)
        arr_input: list[dict[str, str|float]] = json_dict[arry_inputs_json]
        for single_input in arr_input:
            new_input = Input(mats_data=self.mats_data, proc=self.caller, flowsheet=self.flowsheet)
            new_input.load_from_json_dict(json_dict=single_input)
            self.list_inputs.append(new_input)
            self.input_count += 1

    def output_unit_operation(self):
        #TODO: Leave explanatory comments here.
        self.flowsheet.header_organizer(op_nr=self.operation_seq, title=lang_dict_uo_titles[self.uo_tag])
        if not (self.pre_comment == None or self.pre_comment == ''):
            self.flowsheet.put_body_comments(self.pre_comment)

        for inpt in self.list_inputs:
            inpt.print_input()
            # #line-1: Material name and relative quantity
            # line_mat = inpt.put_material(time=lang_dict_cmn[tag_flow_cmn_rec_time],
            #                                   method=lang_dict_chgng_specif[inpt.method],
            #                                   record=lang_dict_chgng_specif[tag_part_rec_lot],
            #                                   operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
            #                                   witness=lang_dict_cmn[tag_flow_cmn_rec_sign],)

            # #line-2: QTY instruction and record
            # inpt.instruct_qty_range(record=lang_dict_chgng_specif[tag_part_rec_qyt_input],
            #                        line_mat=line_mat)

            # #For liquid only, container ID, flex ID 
            # if inpt.method in (method_liq, method_shower, method_mobile_tank):
            #     self.flowsheet.put_line(record=lang_dict_chgng_specif[tag_part_rec_cntnr_id])
            #     self.flowsheet.put_line(record=lang_dict_chgng_specif[tag_part_rec_hose],
            #                              operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
            #                              witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
            # elif inpt.method == method_press:
            #     self.flowsheet.put_line(record=lang_dict_chgng_specif[tag_part_rec_cntnr_id],
            #                             operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
            #                             witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
            
            # #for both liq and solid; temp and time control.
            # if not (inpt.time_control == timectrl_none or inpt.time_control is None):
            #     self.__put_time_control(input=inpt)

            # if not (inpt.temp_control == temprctrl_none or inpt.temp_control is None):
            #     self.__put_temp_control(input=inpt)              
     
            # self.__put_end_of_dosing()
            # self.flowsheet.linefeed()

        if not (self.post_comment == None or self.post_comment == ''):
            self.flowsheet.put_body_comments(self.post_comment)
            self.flowsheet.linefeed()


    def __put_time_control(self, input: Input=None):
        sentence_instruction: str = ''
        if (input.time_control == timectrl_min):
            sentence_instruction = lang_dict_instr_stcs[tag_stc_time_min].format(min=input.time_min)

        elif (input.time_control == timectrl_max):
            sentence_instruction = lang_dict_instr_stcs[tag_stc_time_max].format(max=input.time_max)

        elif (input.time_control == timectrl_min_max):
            sentence_instruction = lang_dict_instr_stcs[tag_stc_time_min_max].format(min=input.time_min, max=input.time_max)

        elif input.time_control == timectrl_placeholder:
            sentence_instruction = lang_dict_chgng_specif[tag_part_instr_timectrl_plchldr]
        
        self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                method=lang_dict_chgng_specif[tag_part_instr_ini],
                                content=sentence_instruction,
                                operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                witness=lang_dict_cmn[tag_flow_cmn_rec_sign])


    def __put_temp_control(self, input: Input=None):
        if input.temp_control == temprctrl_min:
            sentence = lang_dict_instr_stcs[tag_stc_temp_min].format(min=input.temp_min)
            self.flowsheet.put_line(content=sentence, record=lang_dict_chgng_specif[tag_part_rec_temprini])
            self.flowsheet.put_line(record=lang_dict_chgng_specif[tag_part_rec_temprmin])
            self.flowsheet.put_line(record=lang_dict_chgng_specif[tag_part_rec_temprend])

        elif input.temp_control == temprctrl_max:
            sentence = lang_dict_instr_stcs[tag_stc_temp_max].format(max=input.temp_max)
            self.flowsheet.put_line(content=sentence, record=lang_dict_chgng_specif[tag_part_rec_temprini])
            self.flowsheet.put_line(record=lang_dict_chgng_specif[tag_part_rec_temprmax])
            self.flowsheet.put_line(record=lang_dict_chgng_specif[tag_part_rec_temprend])

        elif input.temp_control == temprctrl_min_max:
            sentence = lang_dict_instr_stcs[tag_stc_temp_min_max].format(min=input.temp_min, max=input.temp_max)
            self.flowsheet.put_line(content=sentence, record=lang_dict_chgng_specif[tag_part_rec_temprini])
            self.flowsheet.put_line(record=lang_dict_chgng_specif[tag_part_rec_temprmin])
            self.flowsheet.put_line(record=lang_dict_chgng_specif[tag_part_rec_temprmax])
            self.flowsheet.put_line(record=lang_dict_chgng_specif[tag_part_rec_temprend])

        elif input.temp_control == temprctrl_placeholder:
            sentence = lang_dict_chgng_specif[tag_part_instr_temprctrl_plchldr]
            self.flowsheet.put_line(content=sentence, record=lang_dict_chgng_specif[tag_part_rec_temprini])
            self.flowsheet.put_line(record=lang_dict_chgng_specif[tag_part_rec_temprmin])
            self.flowsheet.put_line(record=lang_dict_chgng_specif[tag_part_rec_temprmax])
            self.flowsheet.put_line(record=lang_dict_chgng_specif[tag_part_rec_temprend])

    def __put_end_of_dosing(self):
            self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                     method=lang_dict_chgng_specif[tag_part_instr_end],
                                     record=lang_dict_chgng_specif[tag_part_rec_cmpltd],
                                     operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
