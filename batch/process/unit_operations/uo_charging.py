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
import flow_draw.data_io.flowsheet as fsht
from flow_draw.trait_def.trait_def import GetMats, GetInputs
from flow_draw.data_io.json_io import Objason, Primitive, Array


header_precomment = defs.hedr_cmn_io_dtil_precmnt #Don't include this in the specific header list!!!
header_postcomment = defs.hedr_cmn_io_dtil_postcmnt #Don't include this in the specific header list!!!


hedr_material_name = 'Material_Name'
hedr_metrics_value = 'Metrics_Value'
hedr_metrics_unit = 'Metrics_Unit'
hedr_error_pct = 'Permissible_Error(%)'
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
                     hedr_error_pct,
                     hedr_method,
                     hedr_time_control,
                     hedr_time_min,
                     hedr_time_max,
                     hedr_temp_control,
                     hedr_temp_min,
                     hedr_temp_max]

id_input_json = 'Material_Input_ID'
"""The key to a material input ID for JSON data exchange."""

hedr_basis_input = 'Calc_Basis_Material_Input_ID'
"""The key to the calculation basis material input ID for JSON data exchange."""

hedr_basis_array = 'Array_Calc_Basis'
"""The key to the array of calculation basis material input IDs for JSON data exchange."""

entry_input_json = 'charging_input_entry'
"""The key to a material input entry for JSON data exchange."""

arry_inputs_json = 'arr_charging_input_entry'
"""The key to a list of material input entries."""

obj_charging_json = 'charging_stage'
"""The key to the unit operation of charging."""

opt_special_id_basis_tgt = defs.id_special_tgt_uo_chgng
"""Special ID for the target compound used as the quantity calculation basis in the charging unit operation."""


cls_input_mat_sm = 'cls_sm'
"""Material class identifier for the starting material."""
cls_input_mat_tgt = 'cls_tgt'
"""Material class identifier for the target material."""
cls_input_mat_other = 'cls_other'
"""Material class identifier for other materials."""


method_liq = 'liquid_port'
method_shower = 'shower'
method_press = 'press_vessel'
method_mobile_tank = 'mobile_tank'
method_pow = 'powder_port'
method_placeholder = 'placeholder'
#List below
list_charging_method =[method_liq,
                       method_shower,
                       method_press,
                       method_mobile_tank,
                       method_pow,
                       method_placeholder]

timectrl_none = "No_time_control"
timectrl_min = "Time_control_with_minimum"
timectrl_max = "Time_control_with_maximum"
timectrl_min_max = 'Time_control_with_minimum_and_maximum'
timectrl_placeholder = 'placeholder'
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
temprctrl_placeholder = 'placeholder'
#list below
list_temp_control = [temprctrl_none,
                    temprctrl_min,
                    temprctrl_max,
                    temprctrl_min_max]

#list_metrics_unit = [defs.tag_metrics_equiv, defs.tag_metrics_vol]
opt_mtrcs_eq = "equiv"
opt_mtrcs_v_per_w = "v/w"
opt_mtrcs_wwpct = "w/w%"
opt_mtrcs_wt_gro_abs = 'wt_gross_abs_kg'
opt_mtrcs_vol_abs = 'vol_abs_kg'
#list below
list_metrics_unit = [opt_mtrcs_eq, opt_mtrcs_v_per_w, opt_mtrcs_wwpct, opt_mtrcs_wt_gro_abs, opt_mtrcs_vol_abs]

error_range_placeholder = 'placeholder'
error_default = 5.0
list_error_range = [None, 1.0, None, None, None, error_default, error_range_placeholder]

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

#TODO: Add container ID!

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
tag_part_mthd_mobile_tank = method_mobile_tank
part_mthd_mobile_tank_jp = "液体コンテナ"
"""Flowsheet component for class Charging. Charging from a mobile tank. An option for large volume liquid charging."""
tag_part_mthd_pwdr = method_pow
part_mthd_pwdr_jp = "粉体投入口"
"""Flowsheet component for class Charging. Charging through the power port. An ption for powder charging."""
tag_part_mthd_plchldr = method_placeholder
part_mthd_plchldr_jp = "<Placeholder: charging method>"
"""Flowsheet component for class Charging. A place holder. An ption for Liquid charging."""


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
                tag_part_mthd_mobile_tank : part_mthd_mobile_tank_jp,
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
        # self.mats_data: mats.Materials = GetMats(self.caller).get_mats() #なんかやだからキャストする。
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


    def get_json_schema(caller: GetMats=None)-> Objason:
        mats_data: mats.Materials = caller.get_mats() 
        list_mats=mats_data.get_list_mats()
        #common=Charging.json_common(arg_name_uo=defs.tag_uo_charging)
        common=Charging.json_common()
        id_input = Primitive(prim_type='integer',
                             key=id_input_json,
                             description='A unique serial number (positive or zero) for the material input. '
                             'This value must be unique for each material input and this rule applies throughout the process. '
                             'Regardless of the input sequence, please assign 0 for (the first input of) the starting material (the key building block of the process). '
                             'This value is used to identify an instance of material input to calculate the quantity of other material inputs when this instance is used as the basis.',
                             nullable=False,
                             required=True)
        name_mats = Primitive(prim_type="string",
                              key=hedr_material_name,
                              enum=list_mats,
                              description='The name of the raw material, solvent, etc., charged.')
        qty_mats = Primitive(prim_type="number",
                             key=hedr_metrics_value,
                             description=f'Relative quantity of the raw material, solvent, and other materials. This object is for the value only.'
                             f'The unit is selected in another entry. '
                             'As a special case, if this instance is one of the split charges of the starting material (the key building block), please put the fraction of the total quantity. '
                             f'For example, if the starting material is split into three charges, each charge should have a relative quantity of 0.333 {opt_mtrcs_eq}. '
                             f'Otherwise (single charge), please put 1.0 {opt_mtrcs_eq} for the relative quantity of the starting material.')
        unit_mats = Primitive(prim_type="string",
                              key=hedr_metrics_unit,
                              description=f'Unit to specify the relative quantity of the raw material, solvent, and other materials. This is for the unit only. '
                              f'"{opt_mtrcs_eq}": molar equivalent vs the selected calculation basis material input. '
                              f'"{opt_mtrcs_v_per_w}": volume (L) of liquid vs weight (kg) of the selected calculation basis material input. '
                              f'"{opt_mtrcs_wwpct}": weight/weight percent vs the designated calculation basis material input. '
                              f'"{opt_mtrcs_wt_gro_abs}": The gross weight (kg) of a material is directly specified by an absolute value. This is an exceptional case. '
                              f'"{opt_mtrcs_vol_abs}": The volume (litre) of a non-solid material is directly specified by an absolute value. This is an exceptional case. '
                              'In the JSON, it normally is assumed that evne the starting material is quantified by a relative metrics (equiv or weight percent) in relation to a basis value defined elsewhere. '
                              'Please choose the absolute approac only when it is essential or instructed by the user. '
                              f'This item has to be consistent with the other entry "{hedr_metrics_value}"',
                              enum=list_metrics_unit)
        basis_input_single = Primitive(prim_type='integer',
                                key=hedr_basis_input,
                                description='The material input used as the basis for calculating the quantity of other material inputs.'
                                f'If the target material is designated as the calculation basis, please put {mats_data.get_name_sm()}.',
                                nullable=False,
                                required=True)
        arr_basis_inputs = Array(key=hedr_basis_array,
                           content = basis_input_single,
                           description='Array of material input IDs used as the basis for calculating the quantity of other material inputs. '
                           'In most cases, only one material input ID (the key building block) is used as the basis. '
                           'However, multiple input IDs are allowed. For a rare example, when the key raw material is split and charged in multiple steps. '
                           f'If the target material is designated as the calculation basis, please put {opt_special_id_basis_tgt}. '
                           'If this input depends on nothing, e.g., the starting material, please leave this null.',
                           nullable=True,
                           required = True)
        permiss_error = Primitive(prim_type="number",
                                  key=hedr_error_pct,
                                  description="Permissible error of the material quantity indicated in percent (%). If not specified in the data source, "
                                    "please use the default value of 1 percent for the key raw material, and 5 percent for other materials.")
        charging_method = Primitive(prim_type='string',
                                    key=hedr_method,
                                    enum=list_charging_method,
                                    description=f"Method to charge/dose a material. "
                                        f'"{method_liq}" is charging solvent or liquid reagent through a pipe. This method is less frequently chosen. '
                                        f'"{method_shower}" is charging solvents by using a showering device in the reaction vessel to clean adhered solid material on the wall. '
                                        f'"{method_press}" is preferred for solvents and liquid reagents less than 10 liters. The liquid material is put in a container under some pressure. '
                                        f'The liquid is transferred to the reaction vessel at a controlled rate. '
                                        f'"{method_mobile_tank}" is choses when a large volume of liquid, e.g. two-digit liters of solvent, needs to be measured and charged. '
                                        f'"{method_pow}" is for solid material. A solid material is charged through an opening on the top of the reactor. '
                                        'As a special case, slurry of crystal seed is charged by this method.'
                                        f'If you can\'t choose the right option, please select "{method_placeholder}"')
        time_ctrl = Primitive(prim_type='string',
                              key=hedr_time_control,
                              enum=list_time_control,
                              description=f'Constraint on time to dose/charge the material. '
                                f'"{timectrl_none}" means time control is no needed. '
                                f'"{timectrl_min}" should be selected when lower limit must be complied. '
                                f'"{timectrl_max}" should be selected when upper limit must be complied. '
                                f'"{timectrl_min_max}" should be selected when the event has to happen in a specific range of time. '
                                f'"Please select {timectrl_placeholder}" if the right option cannot be chosen from the given information.')
        
        time_min = Primitive(prim_type="number",
                             key=hedr_time_min,
                             description=f'Lower limit of charging/dosing time in minutes unit. Necessary if "{hedr_time_control}" is "{timectrl_min}" or "{timectrl_min_max}"; nullable otherwise',
                             nullable=True)
        
        time_max = Primitive(prim_type="number",
                             key=hedr_time_max,
                             description=f'Upper limit of charging/dosing time in minutes unit. Necessary if "{hedr_time_control}" is "{timectrl_max}" or "{timectrl_min_max}"',
                             nullable=True)
        
        temp_ctrl = Primitive(prim_type='string',
                              key=hedr_temp_control,
                              enum=list_temp_control,
                              description=f'Constraint on temperature during dosing/charging of the material. '
                              f'"{temprctrl_none}" means no temperature control is needed. '
                              f'"{temprctrl_min}" is selected when the lower limit is set for the dosing/charging. '
                              f'"{temprctrl_max}" is selected when the upper limit is set for the dosing/charging. '
                              f'"{temprctrl_min_max}" is for a case where the charging/dosing have to take place in a certain specific temperature range. ',
                              required=True)
        
        temp_min = Primitive(prim_type='number',
                             key=hedr_temp_min,
                             description= f'An optional lower limit for internal temperature during dosing/charging.'
                             f'This is necessary if "{hedr_temp_control}" is "{temprctrl_min}" or "{temprctrl_min_max}". Nullable, otherwise.',
                             nullable=True,
                             required=True)
        temp_max = Primitive(prim_type='number',
                             key=hedr_temp_max,
                             description=f'An optional upper limit for internal temperature during dosing/charging.'
                             f'This is necessary if "{hedr_temp_control}" is "{temprctrl_max}" or "{temprctrl_min_max}". Nullable, otherwise.',
                             nullable=True,
                             required=True)
        
        input_entry = Objason(key=entry_input_json,
                              props=[id_input, name_mats, qty_mats, unit_mats, arr_basis_inputs, permiss_error, charging_method, time_ctrl, time_min, time_max, temp_ctrl, temp_min, temp_max],
                              description='Combination of material, quantity, permissible quantity error, charging method, time constraints, temperature range to define each charging/dosing operation.'
                             )

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
            # line_mat = self.flowsheet.put_material(time=lang_dict_cmn[tag_flow_cmn_rec_time],
            #                                         method=lang_dict_chgng_specif[temp_inpt.method],
            #                                         record=lang_dict_chgng_specif[tag_part_rec_lot],
            #                                         operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
            #                                         witness=lang_dict_cmn[tag_flow_cmn_rec_sign],
            #                                         mat_input=temp_inpt)

            #line-1: Material name and relative quantity
            line_mat = inpt.put_material(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                              method=lang_dict_chgng_specif[inpt.method],
                                              record=lang_dict_chgng_specif[tag_part_rec_lot],
                                              operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                              witness=lang_dict_cmn[tag_flow_cmn_rec_sign],)

            #line-2: QTY instruction and record
            inpt.instruct_qty_range(record=lang_dict_chgng_specif[tag_part_rec_input],
                                   line_mat=line_mat)

            #For liquid only, flex ID 
            if (inpt.method == method_liq or
                # temp_inpt.method == method_press or
                inpt.method == method_shower or
                inpt.method == method_mobile_tank):
                self.flowsheet.put_line(record=lang_dict_chgng_specif[tag_part_rec_hose],
                                         operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                         witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
            
            #for both liq and solid; temp and time control.
            if not (inpt.time_control == timectrl_none or inpt.time_control is None):
                self.__put_time_control(input=inpt)

            if not (inpt.temp_control == temprctrl_none or inpt.temp_control is None):
                self.__put_temp_control(input=inpt)              
     
            self.__put_end_of_dosing()
            self.flowsheet.linefeed()

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
    def __init__(self, mats_data: mats.Materials = None, proc: GetInputs = None, flowsheet:Flowsheet=None):
        #Material constants
        self.mats_data: mats.Materials = mats_data
        self.proc: GetInputs = proc
        self.flowsheet = flowsheet

        self.mw:float = None
        """Molecular weight of the material."""
        self.density:float = None
        """Density of the material."""
        self.conc_assay:float = None
        """Assay or concentration of the material."""


        #Charging/dosing variables
        self.id_input:int = None
        """Identifier for the charging operation instance."""
        self.material_name:str = None
        """User input. Material name. Has to be consistent with the materials table"""
        self.material_class:str = None
        """Class identifier for the material. Can be one of 'cls_sm', 'cls_tgt', or 'cls_other'."""
        self.metrics_unit:str = None
        """Holds one of the options in list_metrics_unit. Metrics unit suc as eq or v/w"""
        self.metrics_val:float = None
        """User input float. Factor to the main material as in x eq or y v/w"""
        self.list_id_basis_input:list[int] = None
        """Array of basis input IDs for the material."""
        self.error_pct:float = None
        """User input float. Permissible error percentage. 5.0% for most of materials."""
        self.qty_kg_gross:float = None
        """User input float. Quantity of this raw material."""
        self.error_kg_gross:float = None
        """Calculated float from qty_kg and error_pct"""
        self.mol:float = None
        """Calculated float. Moles of the material."""
        self.qty_kg_net:float = None
        """Calculated float. Net quantity of this raw material."""
        self.vol_litre:float = None
        """Calculated float. Volume of the material in litres."""
        self.qty_calc_compltd:bool = False
        """Indicates whether the quantity has been calculated."""
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
        self.line_fs:int = None
        """Flowsheet line of the qty. """
    
  

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
        self.error_pct = ser[hedr_error_pct]
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
            warnings.warn(message=f"{__class__.__name}: mats_data is None",
                          category=RuntimeWarning)
        else:
            self.__calc_qty()
            self.mw = self.mats_data.get_mw(self.material_name)
            self.density = self.mats_data.get_density(self.material_name)
            self.conc_assay = self.mats_data.get_conc_assay(self.material_name)

    def load_from_json_dict(self, json_dict: dict[str, any]):
        self.id_input =json_dict[id_input_json]
        self.material_name = json_dict[hedr_material_name]
        self.metrics_unit = json_dict[hedr_metrics_unit]
        self.metrics_val = json_dict[hedr_metrics_value]
        self.list_id_basis_input = json_dict[hedr_basis_array]
        self.error_pct = json_dict[hedr_error_pct]
        self.method = json_dict[hedr_method]
        self.time_control = json_dict[hedr_time_control]
        if (self.time_control == timectrl_min or self.time_control == timectrl_min_max): #and hedr_time_min in json_dict:
            self.time_min = json_dict[hedr_time_min]
        if (self.time_control == timectrl_max or self.time_control == timectrl_min_max): #and hedr_time_max in json_dict:
            self.time_max = json_dict[hedr_time_max]
        self.temp_control = json_dict[hedr_temp_control]
        if (self.temp_control == temprctrl_min or self.temp_control == temprctrl_min_max): #and hedr_temp_min in json_dict:
            self.temp_min = json_dict[hedr_temp_min]
        if (self.temp_control == temprctrl_max or self.temp_control == temprctrl_min_max): #and hedr_temp_max in json_dict:
            self.temp_max = json_dict[hedr_temp_max]
        if self.mats_data is None:
            raise RuntimeError(f"{__class__.__name__}: mats_data is None")
        else:
            # self.calc_qty()
            self.mw = self.mats_data.get_mw(self.material_name)
            self.density = self.mats_data.get_density(self.material_name)
            self.conc_assay = self.mats_data.get_conc_assay(self.material_name)
            if self.material_name == self.mats_data.get_name_sm():
                self.material_class = cls_input_mat_sm
            elif self.material_name == self.mats_data.get_name_tgt():
                self.material_class = cls_input_mat_tgt
            else:
                self.material_class = cls_input_mat_other
    

    def test_data_creation1(self):
        self.material_name = 'H2O'
        self.metrics_unit = opt_mtrcs_v_per_w
        self.metrics_val = 1.0
        self.error_pct = 5.0
        self.method = method_liq
        self.time_control = timectrl_min
        self.time_min = '1h'
        self.time_max = None
        self.temp_control = temprctrl_min_max
        self.temp_min = 15
        self.temp_max = 25
        self.calc_qty()

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
        self.calc_qty()


    def mark_as_tgt(self):
        self.id_input = opt_special_id_basis_tgt
        self.material_name = self.mats_data.get_name_tgt()
        self.material_class = cls_input_mat_tgt
        self.mw = self.mats_data.get_mw(material_name=self.material_name)
        if self.mats_data.get_density(material_name=self.material_name) is not None:
            self.density = self.mats_data.get_density(material_name=self.material_name)
        self.error_pct = None

    def calc_qty(self)->bool:
        if self.qty_calc_compltd:
            return True
        
        if self.mats_data is None:
            raise RuntimeError(f"{self.__class__.__name__}.calc_qty() (input of \"{self.material_name}\"): No material data for provided in the material input worksheet.")

        if self.list_id_basis_input is None or len(self.list_id_basis_input) == 0:
            if self.material_class != cls_input_mat_sm and self.material_class != cls_input_mat_tgt:
                raise RuntimeError(f"{self.__class__.__name__}.calc_qty() (input of \"{self.material_name}\"): No quantity calculation basis specified.")
        
        def __is_pos_num(something=None)->bool:
            if something is not None and isinstance(something, (float, int)) and something > 0:
                return True
            else:
                return False

        def __calc_vol():
            dens_sm = self.mats_data.get_density(material_name=self.material_name)
            if not __is_pos_num(dens_sm):
                dens_sm = 1.0
                warnings.warn(f'{self.__class__.__name__}.calc_qty() (input of \"{self.material_name}\"): No density information provided for this material.'
                              '1.0 is assumed to estimate the volume.')
            self.vol_litre = self.qty_kg_gross / dens_sm

          

        if self.material_class == cls_input_mat_sm:
            def __set_metrcs_wt_abs_kg():
                self.metrics_val = self.qty_kg_gross
                self.metrics_unit = opt_mtrcs_wt_gro_abs  
        
            total_mol_sm = self.mats_data.get_mol_sm()
            total_kg_net_sm = self.mats_data.get_kg_net_sm()
            total_kg_gross_sm = self.mats_data.get_gross_kg_sm()
            if self.metrics_unit == opt_mtrcs_eq:
                self.mol = total_mol_sm * self.metrics_val
                self.qty_kg_net = total_kg_net_sm * self.metrics_val
                self.qty_kg_gross = total_kg_gross_sm * self.metrics_val
                self.error_kg_gross = self.qty_kg_gross * (self.error_pct/100.0)
                __calc_vol()
                __set_metrcs_wt_abs_kg()
            elif self.metrics_unit == opt_mtrcs_wwpct:
                self.mol = total_mol_sm * (self.metrics_val/100.0)
                self.qty_kg_net = total_kg_net_sm * (self.metrics_val/100.0)
                self.qty_kg_gross = total_kg_gross_sm * (self.metrics_val/100.0)
                self.error_kg_gross = self.qty_kg_gross * (self.error_pct/100.0)
                __calc_vol()
                __set_metrcs_wt_abs_kg()
            elif self.metrics_unit == opt_mtrcs_wt_gro_abs:
                self.qty_kg_gross = self.metrics_val
                self.error_kg_gross = self.qty_kg_gross * (self.error_pct/100.0)
                if __is_pos_num(self.assay_conc):
                    self.qty_kg_net = self.qty_kg_gross * (self.assay_conc/100.0)
                if __is_pos_num(self.mw):
                    self.mol = self.qty_kg_net * 1000 / self.mw
                __calc_vol()
            elif self.metrics_unit == opt_mtrcs_vol_abs:
                self.vol_litre = self.metrics_val
                if __is_pos_num(self.density):
                    self.qty_kg_gross = self.vol_litre * self.density
                if __is_pos_num(self.assay_conc) and __is_pos_num(self.qty_kg_gross):
                    self.qty_kg_net = self.qty_kg_gross * (self.assay_conc / 100.0)
                if __is_pos_num(self.mw) and __is_pos_num(self.qty_kg_net):
                    self.mol = self.qty_kg_net * 1000 / self.mw
            else:
                raise ValueError(f'{__class__.__name__}.calc_qty(): Invalid metrics_unit "{self.metrics_unit}" for the starting material "{self.material_name}". '
                                 'The quantity must be specified either in equivalents or weight percent.')

            self.qty_calc_compltd = True
            return True

        #Hereunder, the process data is required for further calculations.
        if self.proc is None:
            raise RuntimeError(f"{__class__.__name__}.calc_qty() (input of \"{self.material_name}\"): No process data provided.")

        if self.material_class == cls_input_mat_tgt:
            self.list_id_basis_input = self.proc.get_id_input_sm()
            self.metrics_val = self.proc.get_tgt_stoichiometry()
            self.metrics_unit = opt_mtrcs_eq
            self.mol = self.mats_data.get_mol_sm() * self.proc.get_tgt_stoichiometry() * (self.proc.get_assumed_yield_pct() / 100.0)
            mw_this = self.mats_data.get_mw(material_name = self.material_name)
            if not __is_pos_num(mw_this):
                raise RuntimeError(f"{__class__.__name__}.calc_qty() (input of \"{self.material_name}\"): Invalid molecular weight for this material.")
            self.mw = mw_this
            self.qty_kg_net = self.mw * self.mol / 1000
            self.qty_kg_gross = self.qty_kg_net

            self.qty_calc_compltd = True
            return True

        if self.metrics_unit == opt_mtrcs_eq:
            mol_basis = 0.0
            for dep_id in self.list_id_basis_input:
                input_depended = self.proc.get_input(dep_id)
                if input_depended is None:
                    raise RuntimeError(f"{__class__.__name__}.calc_qty() (input of \"{self.material_name}\"): Dependent input with ID \"{dep_id}\" not found.")
                if input_depended.mol is None:
                    return False
                else:
                    mol_basis += input_depended.mol
            self.mol = mol_basis * self.metrics_val
            mw_this = self.mats_data.get_mw(material_name = self.material_name)
            if mw_this is None or not isinstance(mw_this, (float, int)) or mw_this <= 0:
                raise RuntimeError(f"{__class__.__name__}.calc_qty() (input of \"{self.material_name}\"): Invalid molecular weight for this material.")
            conc_assay_this = self.mats_data.get_conc_assay(material_name = self.material_name)
            if conc_assay_this is None or not isinstance(conc_assay_this, (float, int)) or conc_assay_this <= 0:
                raise RuntimeError(f"{__class__.__name__}.calc_qty() (input of \"{self.material_name}\"): Invalid assay for this material.")
            self.qty_kg_net = self.mol * mw_this/1000
            self.qty_kg_gross = self.qty_kg_net / (conc_assay_this/100.0)
            self.error_kg_gross = self.qty_kg_gross * (self.error_pct/100.0)

            dens_this = self.mats_data.get_density(material_name=self.material_name)
            if dens_this is None or not isinstance(dens_this, (float, int)) or dens_this <= 0:
                dens_this = 1.0
                warnings.warn(f'{__class__.__name__}.calc_qty() (input of \"{self.material_name}\"): No density information provided tor this material.'
                              '1.0 is assumed to estimate the volume.',
                              RuntimeWarning)
            self.vol_litre = self.qty_kg_gross / dens_this
            self.qty_calc_compltd = True
            return True
        
        elif self.metrics_unit == opt_mtrcs_v_per_w:
            net_wt_basis = 0.0
            for dep_id in self.list_id_basis_input:
                input_depended = self.proc.get_input(dep_id)
                if input_depended is None:
                    raise RuntimeError(f"{__class__.__name__}.calc_qty() (input of \"{self.material_name}\"): Dependent input with ID \"{dep_id}\" not found.")
                if input_depended.qty_kg_net is None:
                    return False
                else:
                    net_wt_basis += input_depended.qty_kg_net
            self.vol_litre = net_wt_basis * self.metrics_val
            dens_this = self.mats_data.get_density(material_name=self.material_name)
            if dens_this is None or not isinstance(dens_this, (float, int)) or dens_this <= 0:
                dens_this = 1.0
                warnings.warn(f'{__class__.__name__}.calc_qty() (input of \"{self.material_name}\"): No density information provided tor this material.'
                              '1.0 is assumed to estimate the volume.',
                              RuntimeWarning)
            self.qty_kg_gross = self.vol_litre * dens_this
            self.error_kg_gross = self.qty_kg_gross * (self.error_pct/100.0)
            self.qty_calc_compltd = True
            conc_assay_this = self.mats_data.get_conc_assay(material_name = self.material_name)
            if conc_assay_this is None or not isinstance(conc_assay_this, (float, int)) or conc_assay_this <= 0:
                self.qty_calc_compltd = True
                return True
            self.qty_kg_net = self.qty_kg_gross * (conc_assay_this/100.0)
            mw_this = self.mats_data.get_mw(material_name = self.material_name)
            if mw_this is None or not isinstance(mw_this, (float, int)) or mw_this <= 0:
                self.qty_calc_compltd = True
                return True
            self.mol = self.qty_kg_net*1000 / mw_this
            self.qty_calc_compltd = True
            return True

        elif self.metrics_unit == opt_mtrcs_wwpct:
            net_wt_basis = 0.0
            for dep_id in self.list_id_basis_input:
                input_depended = self.proc.get_input(dep_id)
                if input_depended is None:
                    raise RuntimeError(f"{__class__.__name__}.calc_qty() (input of \"{self.material_name}\"): Dependent input with ID \"{dep_id}\" not found.")
                if input_depended.qty_kg_net is None:
                    return False
                else:
                    net_wt_basis += input_depended.qty_kg_net
            self.qty_kg_net = net_wt_basis * self.metrics_val / 100
            assay_this = self.mats_data.get_conc_assay(material_name = self.material_name)
            if assay_this is None or not isinstance(assay_this, (float, int)) or assay_this <= 0:
                assay_this = 100.0
                warnings.warn(f'{__class__.__name__}.calc_qty() (input of \"{self.material_name}\"): No valid assay information provided for this material. 100.0 is assumed.',
                              RuntimeWarning)
            self.qty_kg_gross = self.qty_kg_net / (assay_this/100)
            self.error_kg_gross = self.qty_kg_gross * (self.error_pct/100.0)
            dens_this = self.mats_data.get_density(material_name=self.material_name)
            if dens_this is None or not isinstance(dens_this, (float, int)) or dens_this <= 0:
                dens_this = 1.0
                warnings.warn(f'{__class__.__name__}.calc_qty() (input of \"{self.material_name}\"): No density information provided for this material. 1.0 is assumed to estimate the volume.',
                              RuntimeWarning)
            self.vol_litre = self.qty_kg_gross / dens_this
            mw_this = self.mats_data.get_mw(material_name=self.material_name)
            if mw_this is None or not isinstance(mw_this, (float, int)) or mw_this <= 0:
                self.qty_calc_compltd = True
                return True
            self.mol = self.qty_kg_net*1000 / mw_this
            self.qty_calc_compltd = True
            return True

        else:
            raise RuntimeError(f"{__class__.__name__}.calc_qty() (input of \"{self.material_name}\"): Unsupported metrics unit \"{self.metrics_unit}\".")


    def get_basis_name(self)->str|None:
        if not self.list_id_basis_input:
            return None
        
        first_id_basis = self.list_id_basis_input[0]
        input_depended = self.proc.get_input(first_id_basis)
        if input_depended is None:
            raise RuntimeError(f"{__class__.__name__}.get_basis_name() (input of \"{self.material_name}\"): Dependent input with ID \"{first_id_basis}\" not found.")
        return input_depended.material_name

    def put_material(self,
                     time=None,
                     method=None,
                     record=None,
                     operator=None,
                     witness=None):

        line = self.flowsheet.get_current_line()
        self.line_fs = line

        excel_formula_mat:str=""
        if self.material_class == cls_input_mat_sm:
            excel_formula_mat = f'={fsht.alph_col_mat}{line}'
        elif self.material_class == cls_input_mat_tgt:
            excel_formula_mat=''
        elif self.metrics_unit == opt_mtrcs_eq:
            excel_formula_mat = f'={fsht.alph_col_mat}{line}&" ("&{fsht.alph_col_equiv}{line}&"equiv vs "&{fsht.alph_col_name_basis}{line}&")"'
        elif self.metrics_unit == opt_mtrcs_v_per_w:
            excel_formula_mat = f'={fsht.alph_col_mat}{line}&" ("&{fsht.alph_col_v_per_w}{line}&"v/w vs "&{fsht.alph_col_name_basis}{line}&")"'               
        elif self.metrics_unit == opt_mtrcs_wwpct:
            excel_formula_mat = f'={fsht.alph_col_mat}{line}&" ("&{fsht.alph_col_wwpct}{line}&"w/w% vs "&{fsht.alph_col_name_basis}{line}&")"'

        if self.metrics_unit == opt_mtrcs_wt_gro_abs:
            self.flowsheet.put_material_new(time=time,
                                            method=method,
                                            record=record,
                                            operator=operator,
                                            witness=witness,
                                            name_mat=self.material_name,
                                            mw=self.mw,
                                            dens=self.density,
                                            conc_assay=self.conc_assay,
                                            wt_abs_kg_gro=self.metrics_val,
                                            error_rel=self.error_pct)
        elif self.metrics_unit == opt_mtrcs_vol_abs:
            self.flowsheet.put_material_new(time=time,
                                            method=method,
                                            record=record,
                                            operator=operator,
                                            witness=witness,
                                            name_mat=self.material_name,
                                            mw=self.mw,
                                            dens=self.density,
                                            conc_assay=self.conc_assay,
                                            vol_abs_litre=self.metrics_val,
                                            error_rel=self.error_pct)
        elif self.metrics_unit == opt_mtrcs_eq:
            self.flowsheet.put_material_new(time=time,
                                            method=method,
                                            record=record,
                                            operator=operator,
                                            witness=witness,
                                            name_mat=self.material_name,
                                            mw=self.mw,
                                            dens=self.density,
                                            conc_assay=self.conc_assay,
                                            equiv=self.metrics_val,
                                            error_rel=self.error_pct)
        elif self.metrics_unit == opt_mtrcs_v_per_w:
            self.flowsheet.put_material_new(time=time,
                                            method=method,
                                            record=record,
                                            operator=operator,
                                            witness=witness,
                                            name_mat=self.material_name,
                                            mw=self.mw,
                                            dens=self.density,
                                            conc_assay=self.conc_assay,
                                            v_per_w=self.metrics_val,
                                            error_rel=self.error_pct)
        elif self.metrics_unit == opt_mtrcs_wwpct:
            self.flowsheet.put_material_new(time=time,
                                            method=method,
                                            record=record,
                                            operator=operator,
                                            witness=witness,
                                            name_mat=self.material_name,
                                            mw=self.mw,
                                            dens=self.density,
                                            conc_assay=self.conc_assay,
                                            wwpct=self.metrics_val,
                                            error_rel=self.error_pct)
        else:
            raise ValueError(f'{self.__class__.__name__}.put_material(): Unsupported metrics unit ({self.metrics_unit}) for material ({self.material_name}).')

        return line

    def instruct_qty_range(self,
                  time: str =None,
                  method: str=None,
                  record: str=None,
                  operator: str=None,
                  witness: str=None,
                 line_mat:int=None)->int:
        if line_mat is None:
            raise ValueError(f'{self.__class__.__name__}.put_range(): Material line (line_mat) must be provided.')
        
        excel_formular_qty = f'=TEXT({fsht.alph_col_kg_gro}{line_mat},"0.00")&" ± "&TEXT({fsht.alph_col_err_abs}{line_mat},"0.00")&" kg"'
        line_qty = self.flowsheet.put_line(time=time, method=method, content=excel_formular_qty, record=record, operator=operator, witness=witness)

        return line_qty


    def link_inputs(self):
        if self.proc is None:
            raise ValueError(f'{self.__class__.__name__}.put_qty_material(): Material input (inputs:GetInputs) must be provided.')
        if self.line_fs is None:
            raise RuntimeError(f'{self.__class__.__name__}.put_qty_material(): '
                    f'Input "{self.material_name}" (ID {self.id_input}) has an empty fs_line_mat.')


        #>>>>>>>>>>>>>>>>>>>> func in func from here >>>>>>>>>>>>>>>>>>>>

        def __prep_ref(alph_col:str=None, list_rows:list[int]=None)->str:
            if alph_col is None:
                raise ValueError(f'{self.__class__.__name__}.put_qty_material().__prep_ref(): An argument "alph_col" is None. Alphabet column identifier is needed.')
            if not list_rows:
                raise ValueError(f'{self.__class__.__name__}.put_qty_material().__prep_ref(): An argument "list_rows" is None or len(list_rows)==0. A list of depended row is needed.')
            
            if len(list_rows) == 1:
                return f'={alph_col}{list_rows[0]}'
            else:
                list_cell:list[str] = []
                for row in list_rows:
                    list_cell.append(f'{alph_col}{row}')

                str_all_ref = ','.join(list_cell)
                xls_formula = f'=SUM({str_all_ref})'
                return xls_formula        

        def __basis_ids_to_lines(list_ids:list[int]=None)->list[int]:
            if not list_ids:
                raise RuntimeError(f'{self.__class__.__name__}.put_qty().__basis_ids_to_lines(): '
                                   '"list_ids" is None or empty.')
            list_lines:list[int]=[]
            for single_id in list_ids:
                basis = self.proc.get_input(id_input=single_id)
                list_lines.append(basis.line_fs)
            return list_lines

        #<<<<<<<<<<<<<<<<<<<< func in func to here <<<<<<<<<<<<<<<<<<<<<<<

        if self.metrics_unit in (opt_mtrcs_wt_gro_abs, opt_mtrcs_vol_abs):
            self.flowsheet.put_links(line_fs_this=self.line_fs,
                                     name_basis='(absolute)')
        else:
            if not self.list_id_basis_input:
                raise RuntimeError(f'{self.__class__.__name__}.put_qty_materials():'
                                   f'No basis specified for "{self.material_name}" (input ID: {self.id_input}). '
                                   f'Although it metrics_unit is {self.metrics_unit}, which requires at least one basis input.')

            first_id_input = self.list_id_basis_input[0]
            name_basis = self.proc.get_input(id_input=first_id_input).material_name

            list_lines_basis = __basis_ids_to_lines(list_ids=self.list_id_basis_input)

            if self.metrics_unit == opt_mtrcs_eq:
                # __put_values(name_basis=name_basis,
                #             list_rows_basis_mol=__basis_ids_to_lines(list_basis),
                #             equiv=mat_input.metrics_val)
                # return line_fs_this
                self.flowsheet.put_links(line_fs_this=self.line_fs,
                                         name_basis=name_basis,
                                         ref_mol_basis=__prep_ref(alph_col=fsht.alph_col_mol, list_rows=list_lines_basis))
            elif self.metrics_unit == opt_mtrcs_v_per_w:
                # __put_values(name_basis=name_basis,
                #             list_rows_basis_kg_net=__basis_ids_to_lines(list_basis),
                #             v_per_w=mat_input.metrics_val)
                # return line_fs_this
                self.flowsheet.put_links(line_fs_this=self.line_fs,
                                         name_basis=name_basis,
                                         ref_kg_net_basis=__prep_ref(alph_col=fsht.alph_col_kg_net, list_rows=list_lines_basis))
            elif self.metrics_unit == opt_mtrcs_wwpct:
                # __put_values(name_basis=name_basis,
                #             list_rows_basis_kg_net=__basis_ids_to_lines(list_basis),
                #             wwpct=mat_input.metrics_val)
                # return line_fs_this
                self.flowsheet.put_links(line_fs_this=self.line_fs,
                                         name_basis=name_basis,
                                         ref_kg_net_basis=__prep_ref(alph_col=fsht.alph_col_kg_net, list_rows=list_lines_basis))
            else:
                raise RuntimeError(f'{self.__class__.__name__}: Invalid metrics unit "{self.metrics_unit}" for the input ID {self.id_input} of "{self.material_name}".')



            
            



    