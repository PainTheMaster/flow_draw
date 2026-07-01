import pandas as pd
import json
import flow_draw.definitions as defs
from typing import Optional
from flow_draw.batch.process.unit_operations import unit_operation as uo
from flow_draw.data_io import process_io
from flow_draw.materials import materials as mats
from flow_draw.data_io.flowsheet import Flowsheet as fsht
from flow_draw.trait_def.trait_def import GetMats
from flow_draw.data_io.json_io import Objason, Primitive, Array


header_precomment = defs.hedr_cmn_io_dtil_precmnt #Don't include this in the specific header list!!!
header_postcomment = defs.hedr_cmn_io_dtil_postcmnt #Don't include this in the specific header list!!!

hedr_material_name = 'Material_Name'
hedr_metrics_value = 'Metrics_Value'
hedr_metrics_unit = 'Metrics_Unit'
hedr_error = 'Permissible_Error(%)'
hedr_method = 'Charging_Method'
hedr_time_control = 'Time_Control'
hedr_time_min = 'Minimum_Time(min)'
hedr_time_max = 'Maximum_Time(min)'
hedr_temp_control = 'Temp_Control'
hedr_temp_min = 'Minimum_Temp(deg-C)'
hedr_temp_max = 'Maximum_Temp(deg-C)'
#List below
list_header_items = [hedr_material_name,
                     hedr_metrics_value,
                     hedr_metrics_unit,
                     hedr_error,
                     hedr_method,
                     hedr_time_control,
                     hedr_time_min,
                     hedr_time_max,
                     hedr_temp_control,
                     hedr_temp_min,
                     hedr_temp_max]

entry_input_json = 'charging_input_entry'
"""The key to a material input entry for JSON data exchange."""

arry_inputs_json = 'arr_charging_input_entry'
"""The key to a list of material input entries."""

obj_charging_json = 'charging_stage'
"""The key to the unit operation of charging."""

method_liq = 'liquid_port'
method_shower = 'shower'
method_press = 'press_vessel'
method_pow = 'powder_port'
method_placeholder = 'placeholder'
#List below
list_charging_method =[method_liq,
                       method_shower,
                       method_press,
                       method_pow,
                       method_placeholder]

timectrl_none = "No_time_control"
timectrl_min = "Time_control_with_minimum"
timectrl_max = "Time_control_with_maximum"
timectrl_min_max = 'Time_control_with_minimum_and_maximum'
timectrl_placeholder = 'Placeholder'
#List below
list_time_control = [timectrl_none,
                    timectrl_min,
                    timectrl_max,
                    timectrl_min_max,
                    timectrl_placeholder]

temprctrl_none = "No_temp_control"
temprctrl_min = "Temp_control_with_minimum"
temprctrl_max = "Temp_control_with_maximum"
temprctrl_min_max = 'Temp_control_with_minimum_and_maximum'
temprctrl_placeholder = 'Placeholder'
#list below
list_temp_control = [temprctrl_none,
                    temprctrl_min,
                    temprctrl_max,
                    temprctrl_min_max]

#list_metrics_unit = [defs.tag_metrics_equiv, defs.tag_metrics_vol]
opt_mtrcs_eq = "equiv"
opt_mtrcs_vol = "v/w"
#list below
list_metrics_unit = [opt_mtrcs_eq, opt_mtrcs_vol]

error_range_placeholder = 'place_holder'
list_error_range = [None, 1.0, None, None, None, 5.0, error_range_placeholder]

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
part_instr_ini_jp = '仕込み開始'
"""Flowseet component for class Charging. An action item of commencement of charging/dosing"""
tag_part_instr_end = "tag_chgng_instr_end"
part_instr_end_jp = '仕込み終了'
"""Flowseet component for class Charging. An action item of end of charging/dosing"""
tag_part_rec_input = "tag_chgng_rec_input"
part_rec_input_jp = '仕込み量__________kg'
"""Flowseet component for class Charging. A recording element for dispensed amount"""
tag_part_rec_lot = "tag_chgng_rec_lot"
part_rec_lot_jp = 'ロット番号__________'
"""Flowseet component for class Charging. A recording element for the lot number of a material"""
tag_part_rec_hose = "tag_chgng_rec_hose"
part_rec_hose_jp ='溶媒用フレキID__________'
"""Flowseet component for class Charging. A recording element for the ID of flexible tube for solvents"""
tag_part_rec_temprini = "tag_chgng_rec_temprini"
part_rec_temprini_jp = '開始時内温_______℃'
"""Flowseet component for class Charging. A recording element for initial temperature of a certain action"""
tag_part_rec_temprmax = "tag_chgng_rec_temprmax"
part_temprmax_jp = '仕込み時最高内温_______℃'
"""Flowseet component for class Charging. A recording element for the maximum temperature"""
tag_part_rec_temprmin = "tag_chgng_rec_temprmin"
part_temprmin_jp = '仕込み時最低内温_______℃'
"""Flowseet component for class Charging. A recording element for the minimum"""
tag_part_rec_temprend = "tag_chgng_rec_temprend"
part_temprend_jp = '終了時内温_______℃'
"""Flowseet component for class Charging. A recording element for the terminal temperature"""
tag_part_rec_cmpltd = "tag_chgng_rec_cmpltd"
part_cmpltd_jp ='□ 仕込み実施'
"""Flowseet component for class Charging. A check box for complete charging/dosing"""

tag_part_mthd_liq = method_liq
part_mthd_liq_jp = "液体投入口"
"""Flowsheet component for class Charging. Charging through liquid charging port. An ption for Liquid charging."""
tag_part_mthd_shower = method_shower
part_mthd_shower_jp = "常設シャワー"
"""Flowsheet component for class Charging. Charging through the fixed shower. An ption for Liquid charging."""
tag_part_mthd_prssvesl = method_press
part_mthd_prssvesl_jp = "圧送容器"
"""Flowsheet component for class Charging. Charging from a pressure vessel. An ption for Liquid charging."""
tag_part_mthd_pwdr = method_pow
part_mthd_pwdr_jp = "粉体投入口"
"""Flowsheet component for class Charging. Charging through the power port. An ption for powder charging."""
tag_part_mthd_plchldr = method_placeholder
part_mthd_plchldr_jp = "<Placeholder: charging method>"
"""Flowsheet component for class Charging. A place holder. An ption for Liquid charging."""


#TODO: Charging method!!!!

dict_jp_parts={tag_part_instr_ini : part_instr_ini_jp,
                tag_part_instr_end : part_instr_end_jp,
                tag_part_rec_input : part_rec_input_jp,
                tag_part_rec_lot : part_rec_lot_jp,
                tag_part_rec_hose : part_rec_hose_jp,
                tag_part_rec_temprini : part_rec_temprini_jp,
                tag_part_rec_temprmax : part_temprmax_jp,
                tag_part_rec_temprmin : part_temprmin_jp,
                tag_part_rec_temprend : part_temprend_jp,
                tag_part_rec_cmpltd : part_cmpltd_jp,
                tag_part_mthd_liq : part_mthd_liq_jp,
                tag_part_mthd_shower : part_mthd_shower_jp,
                tag_part_mthd_prssvesl : part_mthd_prssvesl_jp,
                tag_part_mthd_pwdr : part_mthd_pwdr_jp,
                tag_part_mthd_plchldr : part_mthd_plchldr_jp
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
              tag_stc_time_min : '*滴下時間{min}以上',
              tag_stc_time_max : '*滴下時間{max}以内',
              tag_stc_time_min_max : '*滴下時間{min}～{max}以内',
              tag_stc_temp_min : "仕込み中内温{min}℃以上",
              tag_stc_temp_max : "仕込み中内温{max}℃以下",
              tag_stc_temp_min_max : "仕込み中内温{min}～{max}℃"}

lang_dict_instr_stcs = dict_jp_stcs
"""A language dictionary for a instruction sentence with time or temperature limit. Use str.format(min and/or max) to pur an appropriate parameter"""


class Charging(uo.UnitOperation, uo_tag=defs.tag_uo_charging):
    """
    TODO: Make some comment here.
    """
    
    def __init__(self, caller: GetMats=None, flow_sheet:fsht.Flowsheet=None, operation_seq:int=None, num_subitems: int =None, edit_comment:str=None):
        """
        Initialises the newly created instance of the class Charging.

        Parameters
        ---------------
        caller: flow_draw.trait_def.trait_def.GetMats
            The calling object. In the case of the class Charging, GetMats class is expected. From the given caller object, Charging expects materials.Materials passed by get_mats() method.
        """
        super().__init__(caller=caller, flowsheet=flow_sheet, operation_seq=operation_seq, num_subitems=num_subitems, edit_comment=edit_comment)
        # self.mats_data: mats.Materials = GetMats(self.caller).get_mats() #なんかやだからキャストする。
        self.mats_data: mats.Materials = None
        if caller is not None:
            self.mats_data = (self.caller).get_mats()
        self.input_count = 0
        self.inputs: list[Input] = []

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
            self.inputs.append(new_input)
            self.input_count += 1


    def get_json_schema(caller: GetMats=None)-> Objason:
        mats_data: mats.Materials = caller.get_mats() 
        list_mats=mats_data.get_list_mats()
        #common=Charging.json_common(arg_name_uo=defs.tag_uo_charging)
        common=Charging.json_common()

        name_mats = Primitive(prim_type="string",
                              key=hedr_material_name,
                              enum=list_mats,
                              description='The name of the raw material, solvent, etc., charged.')
        qty_mats = Primitive(prim_type="number",
                             key=hedr_metrics_value,
                             description=f'Relative quantity of the raw material, solvent, and other materials in molar equivalent (eq) or volume/weight (v/w) vs the key raw material. '\
                                  f'The unit is selected in another entry. The key raw material is {mats_data.get_main_raw_material()}')
        unit_mats = Primitive(prim_type="string",
                              key=hedr_metrics_unit,
                              description=f'Unit to specify the relative quantity of the raw material, solvent, and other materials. Molar equivalent (eq) or volume/weight (v/w). '\
                                f'This item has to be consistent with the other entry "{hedr_metrics_value}"',
                              enum=list_metrics_unit)
        permiss_error = Primitive(prim_type="number",
                                  key=hedr_error,
                                  description="Permissible error of the material quantity indicated in percent (%). If not specified in the data source, "\
                                    "please use the default value of 1 percent for the key raw material, and 5 percent for other materials.")
        charging_method = Primitive(prim_type='string',
                                    key=hedr_method,
                                    enum=list_charging_method,
                                    description=f"Method to charge/dose a material."\
                                        f'"{method_liq}" is charging solvent or liquid reagent through a pipe. This method is less frequently chosen.'\
                                        f'"{method_shower}" is charging solvents by using a showering device in the reaction vessel to clean adhered solid material on the wall.'\
                                        f'"{method_press}" is preferred for solvents and liquid reagents. The liquid material is put in a container under a controlled pressure.'\
                                        f'The liquid is transferred to the reaction vessel at a controlled rate.'\
                                        f'"{method_pow}" is for solid material. A solid material is charged through an opening on the top of the reactor.'\
                                        f'If you can\'t choose the right option, please select "{method_placeholder}"',
                                        )
        time_ctrl = Primitive(prim_type='string',
                              key=hedr_time_control,
                              enum=list_time_control,
                              description=f'Constraint on time to dose/charge the material.'\
                                f'"{timectrl_none}" means time control is no needed.'\
                                f'"{timectrl_min}" should be selected when lower limit must be complied.'\
                                f'"{timectrl_max}" should be selected when upper limit must be complied.'\
                                f'"{timectrl_min_max}" should be selected when the event has to happen in a specific range of time.'\
                                f'"Please select {timectrl_placeholder}" if the right option cannot be chosen from the given information.')
        
        time_min = Primitive(prim_type="number",
                             key=hedr_time_min,
                             description=f'Lower limit of charging/dosing time. Necessary if "{hedr_time_control}" is "{timectrl_min}" or "{timectrl_min_max}"',
                             required=True)
        
        time_max = Primitive(prim_type="number",
                             key=hedr_time_max,
                             description=f'Upper limit of charging/dosing time. Necessary if "{hedr_time_control}" is "{timectrl_max}" or "{timectrl_min_max}"',
                             required=True)
        
        temp_ctrl = Primitive(prim_type='string',
                              key=hedr_temp_control,
                              enum=list_temp_control,
                              description=f'Constraint on temperature during dosing/charging of the material.'\
                              f'"{temprctrl_none}" means no temperature control is needed.'\
                              f'"{temprctrl_min}" is selected when the lower limit is set for the dosing/charging.'\
                              f'"{temprctrl_max}" is selected when the upper limit is set for the dosing/charging.'\
                              f'"{temprctrl_min_max}" is for a case where the charging/dosing have to take place in a certain specific temperature range.',
                              required=True
                              )
        
        temp_min = Primitive(prim_type='number',
                             key=hedr_temp_min,
                             description='An optional lower limit for inner temperature during dosing/charging. Please follow the instruction on the given data source.',
                             required=True
                             )
        temp_max = Primitive(prim_type='number',
                             key=hedr_temp_max,
                             description='An optional upper limit for inner temperature during dosing/charging. Please follow the instruction on the given data source.',
                             required=True
                             )
        
        input_entry = Objason(key=entry_input_json,
                              props=[name_mats, qty_mats, unit_mats, permiss_error, charging_method, time_ctrl, temp_ctrl],
                              description=f'Combination of material, quantity, permissible quantity error, charging method, time constraints, temperature range to define each charging/dosing operation.'
                             )
        input_entry.if_then_else(prop=time_ctrl.key,
                                 val_if=timectrl_min,
                                 props_then=[time_min])
        input_entry.if_then_else(prop=time_ctrl.key,
                                 val_if=timectrl_max,
                                 props_then=[time_max])
        input_entry.if_then_else(prop=time_ctrl.key,
                                 val_if=timectrl_min_max,
                                 props_then=[time_min, time_max])
        input_entry.if_then_else(prop=temp_ctrl.key,
                                 val_if=temprctrl_min,
                                 props_then=[temp_min])
        input_entry.if_then_else(prop=temp_ctrl.key,
                                 val_if=temprctrl_max,
                                 props_then=[temp_max])
        input_entry.if_then_else(prop=temp_ctrl.key,
                                 val_if=temprctrl_min_max,
                                 props_then=[temp_min, temp_max])
        
        arr_input = Array(key=arry_inputs_json,
                          content=input_entry,
                          description='A list of material input entries. A single material or more is put in the reactor vessel in a charging/dosing stage.',
                          required=True)
        charging_dosing = Objason(key=obj_charging_json,
                                  props=common+[arr_input],
                                  description='This object corresponds to a unit operation of charging/dosing which appears as a single block on the flowsheet. '\
                                    'One or more material(s) are dosed/charged into the reaction vessel.',
                                  required=False)
        return charging_dosing
        


    def load_from_json_dict(self, json_dict: dict[str, any]):
        self.operation_seq=json_dict[defs.hedr_cmn_io_dtil_seq]
        if defs.hedr_cmn_io_dtil_edt_cmnt in json_dict:
            self.edit_comment = json_dict[defs.hedr_cmn_io_dtil_edt_cmnt]
        if defs.hedr_cmn_io_dtil_precmnt in json_dict:
            self.pre_comment = json_dict[defs.hedr_cmn_io_dtil_precmnt]
        if defs.hedr_cmn_io_dtil_postcmnt in json_dict:
            self.post_comment = json_dict[defs.hedr_cmn_io_dtil_postcmnt]
        arr_input: list[dict[str, str|float]] = json_dict[arry_inputs_json]
        for single_input in arr_input:
            # name_mat:str = tmp_ipt[hedr_material_name]
            # #metrics value: float
            # qty_mats:float = tmp_ipt[hedr_metrics_value]
            # #metrics unit: str
            # unit_mats:str = tmp_ipt[hedr_metrics_unit]
            # #error: float percentage
            # permis_error:float = tmp_ipt[hedr_error]
            # #charging method: str
            # charging_method:str = tmp_ipt[hedr_method]
            # #time control method: str
            # tmie_ctrl:str = tmp_ipt[hedr_time_control]
            # #temp_min: float
            # tempr_min:float = tmp_ipt[hedr_temp_min]
            # #temp_max: float
            # tempr_max:float = tmp_ipt[hedr_temp_max]
            new_input = Input(mats_data=self.mats_data)
            new_input.load_from_json_dict(json_dict=single_input)
            self.inputs.append(new_input)
            self.input_count += 1






    def output_unit_operation(self):
        #TODO Leave explanatory comments here.
        self.flowsheet.header_organizer(op_nr=self.operation_seq, title=lang_dict_uo_titles[self.uo_tag])
        if not (self.pre_comment == None or self.pre_comment == ''):
            self.flowsheet.put_body_comments(self.pre_comment)

        for temp_inpt in self.inputs:
            self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                     method=lang_dict_chgng_specif[temp_inpt.method],
                                     content=temp_inpt.material_name,
                                     record=lang_dict_chgng_specif[tag_part_rec_lot],
                                     operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                     witness=lang_dict_cmn[tag_flow_cmn_rec_sign])

            #line-2: QTY instruction and record
            str_qty = lang_dict_instr_stcs[tag_stc_qty].format(qty=temp_inpt.qty_kg, err=temp_inpt.error_kg)
            self.flowsheet.put_line(content=str_qty, record=lang_dict_chgng_specif[tag_part_rec_input])

            #For liquid only, flex ID 
            if (temp_inpt.method == method_liq or
                temp_inpt.method == method_press or
                temp_inpt.method == method_shower):
                self.flowsheet.put_line(record=lang_dict_chgng_specif[tag_part_rec_hose],
                                         operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                         witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
            
            #for both liq and solid; temp and time control.
            if not (temp_inpt.time_control == timectrl_none or temp_inpt.time_control is None):
                self.__put_time_control(input=temp_inpt)

            if not (temp_inpt.temp_control == temprctrl_none or temp_inpt.temp_control is None):
                self.__put_temp_control(input=temp_inpt)              
     
            self.__put_end_of_dosing()
            self.flowsheet.linefeed()

        if not (self.post_comment == None or self.post_comment == ''):
            self.flowsheet.put_body_comments(self.post_comment)
            self.flowsheet.linefeed()
            
    def interact(self):
        print("Unit operation-"+str(self.operation_seq)+": Charging")
        print("Pre-comment?:")
        self.pre_comment = input()
        print("How many input materials?: ", end="")
        self.input_count=int(input())
        for i in range(self.input_count):
            this_material = Input(mats_data=self.mats_data)
            this_material.interact()
            self.inputs.append(this_material)
        print("Post-comment?:")
        self.post_comment = input()

    def test_data_creation(self):
        self.pre_comment = 'This is the line-1 of a dummy pre-comment\nThis is the line-2 of a dummy pre-comment'
        self.post_comment = 'This is the line-1 of a dummy post-comment;This is the line-2 of a dummy post-comment;The product is salty.'
        material1 = Input(mats_data=self.mats_data)
        material1.test_data_creation1()
        self.inputs.append(material1)
        material2 = Input(mats_data=self.mats_data)
        material2.test_data_creation2()
        self.inputs.append(material2)
        print("Test data created for salt water.")


    def __put_time_control(self, input: Input=None):
        sentence_instruction: str = ''
        if (input.time_control == timectrl_min):
            sentence_instruction = lang_dict_instr_stcs[tag_stc_time_min].format(min=input.time_min)

        elif (input.time_control == timectrl_max):
            sentence_instruction = lang_dict_instr_stcs[tag_stc_time_max].format(max=input.time_max)

        elif (input.time_control == timectrl_min_max):
            sentence_instruction = lang_dict_instr_stcs[tag_stc_time_min_max].format(min=input.time_min, max=input.time_max)
        
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

    def __put_end_of_dosing(self):
            self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                     method=lang_dict_chgng_specif[tag_part_instr_end],
                                     record=lang_dict_chgng_specif[tag_part_rec_cmpltd],
                                     operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    witness=lang_dict_cmn[tag_flow_cmn_rec_sign])

class Input:
    """
    This class is for each material charged, each instance correspnds to each dosage in a charging operation.
    """
    def __init__(self, mats_data: mats.Materials = None):
        self.mats_data: mats.Materials = mats_data
        self.material_name:str = None
        """User input. Material name. Has to be consistent with the materials table"""
        self.metrics_unit:str = None
        """Holds one of the options in list_metrics_unit. Metrics unit suc as eq or v/w"""
        self.metrics_val:float = None
        """User input float. Factor to the main material as in x eq or y v/w"""
        self.error_pct:float = None
        """User input float. Permissible error percentage. 5.0% for most of materials."""
        self.qty_kg:float = None
        """User input float. Quantity of this raw material."""
        self.error_kg:float = None
        """Calculated float from qty_kg and error_pct"""
        self.method = ""
        """Holds one of the options in list_charging_method. Input method."""
        self.time_control:str = None
        """Holds one of the options in list list_time_control. Demand for temperature control"""
        self.time_min:str = None
        """User input string. Lower limit for the input time."""
        self.time_max:str = None
        """User input string. Upper limit for the input time."""
        self.temp_control:str = None
        """Holds one of the options in list list_temp_control. Demand for dosing time control"""
        self.temp_min:float = None
        """User input float. Lower temperature limit."""
        self.temp_max:float = None
        """User input float. Upper temperature limit."""
    
    def interact(self):
        print("Material name?: ", end='')
        self.material_name = input()
    
        print("Metrics unit?: ")
        for idx in range(len(list_metrics_unit)):
            print(str(idx)+": "+list_metrics_unit[idx])
        print("> ", end='')
        idx = int(input())
        self.metrics_unit = list_metrics_unit[idx]
        
        print("Metrics value?: ", end='')
        self.metrics_val = float(input())

        
        print('Permissible error?:')
        for idx in range(len(list_error_range)):
            if list_error_range[idx] is not None:
                print(str(idx)+": "+str(list_error_range[idx])+"%")
        print("> ", end='')
        choice_error_range = int(input())
        self.error_pct = list_error_range[choice_error_range]

        print('Specify a charging method?:')
        for idx in range(len(defs.list_yesno)):
            print(str(idx)+': '+defs.list_yesno[idx])
        print("> ", end='')
        specif_yesno = int(input())
        if defs.list_yesno[specif_yesno] == defs.opt_yes:
            for idx in range(len(list_charging_method)):
                print(str(idx)+': '+list_charging_method[idx])
            print("> ", end='')
            choice_chargingmethod = int(input())
            self.method = list_charging_method[choice_chargingmethod]
        
        print("Specicfy a time control method?: ")
        for idx in range(len(list_time_control)):
            print(str(idx)+': '+list_time_control[idx])
        print("> ", end='')
        choice_time_control = int(input())
        self.time_control = list_time_control[choice_time_control]
        if self.time_control == timectrl_min or self.time_control == timectrl_min_max:
            print("Charging time lower limit?: ", end='')
            self.time_min = input()
        if self.time_control == timectrl_max or self.time_control == timectrl_min_max:
            print("Charging time upper limit?: ", end='')
            self.time_max = input()
        
        print("Specicfy a temperature control method?: ")
        for idx in range(len(list_temp_control)):
            print(str(idx)+': '+list_temp_control[idx])
        print("> ", end='')
        choice_temp_control = int(input())
        self.temp_control = list_temp_control[choice_temp_control]
        if self.temp_control == temprctrl_min or self.temp_control == temprctrl_min_max:
            print("Charging temperature (℃) lower limit?: ", end='')
            self.temp_min = float(input())
        if self.temp_control == temprctrl_max or self.temp_control == temprctrl_min_max:
            print("Charging temperature (℃) upper limit?: ", end='')
            self.temp_max = float(input())
        
        self.__calc_qty()

    def load_params_from_series(self, ser: pd.Series):
        """
        Loads charing operation parameters from a pandas.Series object which is cut out from an pandas.DataFrame object.
        This method is intended to be used solely in Charging.load_params_from_df().

        Parameters
        --------------
        ser: pd.Series
            A series with a header. The series holds input data for each material charged/dosed in the unit operation.
            The header items shall be in line with those defined in the module.

        Returns
        --------------
        None
        """
        self.material_name = ser[hedr_material_name]
        self.metrics_unit = ser[hedr_metrics_unit]
        self.metrics_val = ser[hedr_metrics_value]
        self.error_pct = ser[hedr_error]
        self.method  = ser[hedr_method]
        self.time_control = ser[hedr_time_control]
        if self.time_control == timectrl_min or self.time_control == timectrl_min_max:
            self.time_min = ser[hedr_time_min]
        if self.time_control == timectrl_max or self.time_control == timectrl_min_max:
            self.time_max = ser[hedr_time_max]
        self.temp_control = ser[hedr_temp_control]
        if self.temp_control == temprctrl_min or self.temp_control == temprctrl_min_max:
            self.temp_min = ser[hedr_temp_min]
        if self.temp_control == temprctrl_max or self.temp_control == temprctrl_min_max:
            self.temp_max = ser[hedr_temp_max]
        if self.mats_data is None:
            raise RuntimeWarning(f"{__class__.__name}: mats_data is None")
        else:
            self.__calc_qty()

    def load_from_json_dict(self, json_dict: dict[str, any]):
        self.material_name = json_dict[hedr_material_name]
        self.metrics_unit = json_dict[hedr_metrics_unit]
        self.metrics_val = json_dict[hedr_metrics_value]
        self.method = json_dict[hedr_method]
        self.time_control = json_dict[hedr_time_control]
        if (self.time_control == timectrl_min or self.time_control == timectrl_min_max) and hedr_time_min in json_dict:
            self.time_min = json_dict[hedr_time_min]
        if (self.time_control == timectrl_max or self.time_control == timectrl_min_max) and hedr_time_max in json_dict:
            self.time_max = json_dict[hedr_time_max]
        self.temp_control = json_dict[hedr_temp_control]
        if (self.temp_control == temprctrl_min or self.temp_control == temprctrl_min_max) and hedr_temp_min in json_dict:
            self.temp_min = json_dict[hedr_temp_min]
        if (self.temp_control == temprctrl_max or self.temp_control == temprctrl_min_max) and hedr_temp_max in json_dict:
            self.temp_max = json_dict[hedr_temp_max]
        if self.mats_data is None:
            raise RuntimeWarning(f"{__class__.__name}: mats_data is None")
        else:
            self.__calc_qty()
    
    

    def test_data_creation1(self):
        self.material_name = 'H2O'
        self.metrics_unit = opt_mtrcs_vol
        self.metrics_val = 1.0
        self.error_pct = 5.0
        self.method = method_liq
        self.time_control = timectrl_min
        self.time_min = '1h'
        self.time_max = None
        self.temp_control = temprctrl_min_max
        self.temp_min = 15
        self.temp_max = 25
        self.__calc_qty()

    def test_data_creation2(self):
        self.material_name = 'NaCl'
        self.metrics_unit = opt_mtrcs_eq
        self.metrics_val = 2.0
        self.error_pct = 5.0
        self.method = method_pow
        self.time_control = timectrl_none
        self.time_min = None
        self.time_max = None
        self.temp_control = temprctrl_min_max
        self.temp_min = 15
        self.temp_max = 25
        self.__calc_qty()

    def __calc_qty(self):
        """
        Calculates the quantity of the material and permissible error in "kg" unit.
        For this function to work, instance/values of mats_data, metrics unit (equiv or v/w), metrics value (a factor to the main starting material) have to have been let to the instance variable.
        The calculated result is set to the self.qty_kg, self.error_kg, and returns nothing.

        Parameters
        -----------
        None

        Returns
        -----------
        None
        """
        if self.mats_data is None:
            raise RuntimeError(f"{__class__.__name__}.__calc_qty() (input of \"{self.material_name}\"): Material data for provided in the material input worksheet.")
        if self.metrics_unit == opt_mtrcs_eq:
            self.qty_kg = self.mats_data.to_kilogram(material_name = self.material_name, equiv=self.metrics_val)
            self.error_kg = self.qty_kg * (self.error_pct/100.0)
        elif self.metrics_unit == opt_mtrcs_vol:
            self.qty_kg = self.mats_data.to_kilogram(material_name = self.material_name, vol_per_weight=self.metrics_val)
            self.error_kg = self.qty_kg * (self.error_pct/100.0)
        else:
            raise ValueError(f'{__class__.__name__}.__calc_qty(): metrics_unit (eq or v/w) for \"{self.material_name}\" not defined in the detail input worksheet.')


    