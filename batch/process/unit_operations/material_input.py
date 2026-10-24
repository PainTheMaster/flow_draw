"""
Material input (one charge/dose of a material) and the constants that describe it.
Split out of uo_charging.py so that unit operations other than Charging can reuse Input.
"""
from typing import Any, Callable, Optional
import pandas as pd
import warnings
import flow_draw.definitions as defs
from flow_draw.materials import materials as mats
from flow_draw.data_io.flowsheet import Flowsheet
from flow_draw.trait_def.trait_def import GetMats, GetInputs, InputTrait
from flow_draw.data_io.json_io import Objason, Primitive, Array



##############################################
#           Material Input Headers           #
##############################################
hedr_material_name = 'Material_Name'
hedr_metrics_value = 'Metrics_Value'
hedr_metrics_unit = 'Metrics_Unit'
hedr_error_pct = 'Permissible_Error(%)'
hedr_method = 'Charging_Method'
hedr_vessel = "Vessel"
"""JSON key for a single vessel constituting the vessel train."""
hedr_train_vessel = 'Vessel_Train'
"""JSON key/header for vessel train. This is not on the out-most level."""
hedr_time_control = 'Time_Control'
"""header for time control method"""
hedr_time_min = 'Minimum_Time(min)'
"""header for min time"""
hedr_time_max = 'Maximum_Time(min)'
"""header for max time"""
hedr_temp_control = 'Temp_Control'
"""header for temp control"""
hedr_temp_min = 'Minimum_Temp(deg-C)'
"""header for min temp"""
hedr_temp_max = 'Maximum_Temp(deg-C)'
"""header for max temp"""
id_input_json = 'Material_Input_ID'
"""The key to a material input ID for JSON data exchange."""
hedr_basis_input = 'Calc_Basis_Material_Input_ID'
"""The key to the calculation basis material input ID for JSON data exchange."""
hedr_basis_array_json = 'Array_Calc_Basis'
"""The key to the array of calculation basis material input IDs for JSON data exchange."""
entry_input_json = 'charging_input_entry'
"""The key to a material input entry for JSON data exchange."""

#------------list of header items--------------#
list_hedr = [hedr_material_name,
             hedr_metrics_value,
             hedr_metrics_unit,
             hedr_error_pct,
             hedr_method,
            #  hedr_vessel,
             hedr_train_vessel,
             hedr_time_control,
             hedr_time_min,
             hedr_time_max,
             hedr_temp_control,
             hedr_temp_min,
             hedr_temp_max,
             id_input_json,
             hedr_basis_array_json,
             ]

############################################
#                Options                   #
############################################

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
                    temprctrl_min_max,
                    temprctrl_placeholder]

#list_metrics_unit = [defs.tag_metrics_equiv, defs.tag_metrics_vol]
opt_mtrcs_eq = "equiv"
opt_mtrcs_v_per_w = "v/w"
opt_mtrcs_wwpct = "w/w%"
opt_mtrcs_wt_gro_abs = 'wt_gross_abs_kg'
opt_mtrcs_vol_abs = 'vol_abs_kg'
#list below
list_metrics_unit = [opt_mtrcs_eq, opt_mtrcs_v_per_w, opt_mtrcs_wwpct, opt_mtrcs_wt_gro_abs, opt_mtrcs_vol_abs]

error_range_placeholder = 'placeholder'
error_pct_default = 5.0
list_error_range = [None, 1.0, None, None, None, error_pct_default, error_range_placeholder]


#------------header vs options dictionary-------------#
dict_dropdown = {
    hedr_method: list_charging_method,
    hedr_time_control: list_time_control,
    hedr_temp_control: list_temp_control,
    hedr_metrics_unit: list_metrics_unit,
    hedr_error_pct: list_error_range
}




##########################################
#  Tags for translation of common parts  #
##########################################
tag_flow_cmn_rec_time = defs.tag_flow_cmn_rec_time
tag_flow_cmn_rec_sign = defs.tag_flow_cmn_rec_sign
#language dictionary for common flowsheet items
lang_dict_cmn = defs.dict_jp_part_flow_cmn




#########################################
#     Language translation for parts    #
#########################################

#Tags for translation of UO-specific parts
tag_part_instr_ini = "tag_matin_instr_ini"
# part_instr_ini_jp = '仕込み開始'
"""Flowseet component for class Charging. An action item of commencement of charging/dosing"""
tag_part_instr_end = "tag_matin_instr_end"
# part_instr_end_jp = '仕込み終了'
"""Flowseet component for class Charging. An action item of end of charging/dosing"""
tag_part_rec_qyt_input = "tag_matin_rec_input"
# part_rec_input_jp = '仕込み量__________kg'
"""Flowseet component for class Charging. A recording element for dispensed amount"""
tag_part_rec_lot = "tag_matin_rec_lot"
# part_rec_lot_jp = 'ロット番号__________'
"""Flowseet component for class Charging. A recording element for the lot number of a material"""

tag_part_rec_balance_id = "tag_matin_rec_ID_balance"
"""Flowsheet component for class Charging. A recording element for the ID of the balance."""

tag_part_rec_cntnr_id = 'tag_matin_rec_ID_container'
"""Flowsheet component for class Charging. A recording element for the ID of liquid containers."""
tag_part_rec_hose = "tag_matin_rec_ID_hose"
# part_rec_hose_jp ='フレキID__________'
"""Flowseet component for class Charging. A recording element for the ID of flexible hose for solvents"""
tag_part_rec_temprini = "tag_matin_rec_temprini"
# part_rec_temprini_jp = '開始時内温_______℃'
"""Flowseet component for class Charging. A recording element for initial temperature of a certain action"""
tag_part_rec_temprmax = "tag_matin_rec_temprmax"
# part_temprmax_jp = '仕込み時最高内温_______℃'
"""Flowseet component for class Charging. A recording element for the maximum temperature"""
tag_part_rec_temprmin = "tag_matin_rec_temprmin"
# part_temprmin_jp = '仕込み時最低内温_______℃'
"""Flowseet component for class Charging. A recording element for the minimum"""
tag_part_rec_temprend = "tag_matin_rec_temprend"
# part_temprend_jp = '終了時内温_______℃'
"""Flowseet component for class Charging. A recording element for the terminal temperature"""
tag_part_rec_cmpltd = "tag_matin_rec_cmpltd"
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
                tag_part_rec_balance_id : '秤量器ID__________',
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


######################################################
#     Language translation for sentence templates    #
######################################################

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





class Input(InputTrait):
    """
    This class is for each material charged, each instance correspnds to each dosage in a charging operation.
    """
    def __init__(self, get_mats: GetMats = None, get_inputs: GetInputs = None, flowsheet:Flowsheet=None):
        #Material constants
        # self.mats_data: mats.Materials = get_mats
        self.mats_data: mats.Materials = get_mats.get_mats()
        self.proc: GetInputs = get_inputs
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
        self.vessel_train:list[str] = None
        """List corresponding to the vessel train."""
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
    
    
    @staticmethod
    def get_detai_header()->list[str]:
        return list_hedr

    @staticmethod
    def get_detail_option_menu() -> Optional[dict[str, list[str]]]:
        return dict_dropdown

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
        def __is_blank(something=None)->bool:
            return something is None or (not isinstance(something, (list, tuple)) and pd.isna(something))

        def __to_list(something=None)->list:
            if __is_blank(something):
                return []
            elif isinstance(something, (list, tuple)):
                return list(something)
            elif isinstance(something, str):
                #A cell on a worksheet holds a list as a comma-separated string.
                return [v.strip() for v in something.split(',') if v.strip() != '']
            else:
                return [something]

        def __to_int(something=None)->int|None:
            #Integers often come back from Excel as float, e.g. 0.0
            try:
                val = float(something)
            except (TypeError, ValueError):
                warnings.warn(f'{self.__class__.__name__}.load_params_from_series() (input of "{self.material_name}"): '
                              f'"{something}" is not a valid material input ID. It is ignored.', UserWarning)
                return None
            if not val.is_integer():
                warnings.warn(f'{self.__class__.__name__}.load_params_from_series() (input of "{self.material_name}"): '
                              f'"{something}" is not a valid material input ID. It is ignored.', UserWarning)
                return None
            return int(val)

        self.material_name = ser[hedr_material_name]
        if not __is_blank(ser.get(id_input_json)):
            self.id_input = __to_int(ser[id_input_json])
        self.list_id_basis_input = [i for i in map(__to_int, __to_list(ser.get(hedr_basis_array_json))) if i is not None]
        self.metrics_unit = ser[hedr_metrics_unit]
        self.metrics_val = ser[hedr_metrics_value]
        if not __is_blank(ser.get(hedr_error_pct)) and ser[hedr_error_pct]:
            self.error_pct = ser[hedr_error_pct]
        else:
            self.error_pct = error_pct_default
            warnings.warn(f'{self.__class__.__name__}.load_params_from_series(): The given error is empty or zero. {error_pct_default}% as the default value is put for now.', UserWarning)
        self.method  = ser[hedr_method]
        self.vessel_train = [str(v) for v in __to_list(ser.get(hedr_train_vessel))]
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
            warnings.warn(message=f"{__class__.__name__}: mats_data is None",
                          category=RuntimeWarning)
        else:
            #calc_qty() is called later by the process once all the inputs are loaded.
            self.mw = self.mats_data.get_mw(self.material_name)
            self.density = self.mats_data.get_density(self.material_name)
            self.conc_assay = self.mats_data.get_conc_assay(self.material_name)
            if self.material_name == self.mats_data.get_name_sm():
                self.material_class = cls_input_mat_sm
            else:
                self.material_class = cls_input_mat_other

    @staticmethod
    def get_json_schema(caller: GetMats=None)-> Objason:
        mats_data: mats.Materials = caller.get_mats() 
        list_mats=mats_data.get_list_mats()
        id_input = Primitive(prim_type='integer',
                             key=id_input_json,
                             description='A unique serial number (positive or zero) for the material input. '
                             'This value must be unique throughout the process (the whole JSON file for a process). '
                             'Regardless of the input sequence, please assign 0 for (the first input of) the starting material (the key building block of the process). '
                             'This value is used to identify an instance of material input to calculate the quantity of other material inputs when this instance is used as the basis.',
                             nullable=False,
                             required=True)
        name_mats = Primitive(prim_type="string",
                              key=hedr_material_name,
                              enum=list_mats,
                              description='The name of the raw material, solvent, etc., charged.')
        basis_input_single = Primitive(prim_type='integer',
                                        key=hedr_basis_input,
                                        description='The material input used as the basis for calculating the quantity of other material inputs. '
                                        f'If the target material is designated as the calculation basis, please put {opt_special_id_basis_tgt}. '
                                        'Please select the basis input in a source-faithful manner. Preserve not only the value itself, '
                                        'but also the basis or reference quantity against which the value is defined in the source. '
                                        'Do not recalculate, convert, normalize, derive or rebase values even when doing so would provide a mathematically equivalent presentation.',
                                        nullable=False,
                                        required=True)
        arr_basis_inputs = Array(key=hedr_basis_array_json,
                            content = basis_input_single,
                            description='Array of material input IDs used as the basis for calculating the quantity of other material inputs. '
                            'Please select the basis input in a source-faithful manner. Please do not rebase. '
                            'In most cases, only one material input ID (the key building block) is used as the basis. '
                            'However, multiple input IDs are allowed. For a rare example, when the key raw material is split and charged in multiple steps. '
                            f'If the target material is designated as the calculation basis, please put {opt_special_id_basis_tgt}. '
                            'If this input depends on nothing, e.g., the starting material, please leave this null.',
                            nullable=True,
                            required = True)
        qty_mats = Primitive(prim_type="number",
                             key=hedr_metrics_value,
                             description=f'Relative quantity of the raw material, solvent, and other materials. This object is for the value only.'
                             f'The unit is selected in another entry. '
                             'As a special case, if this instance is one of the split charges of the starting material (the key building block), please put the fraction of the total quantity. '
                             f'For example, if the starting material is split into three charges, each charge should have a relative quantity of 0.333 {opt_mtrcs_eq}. '
                             f'Otherwise (single charge), please put 1.0 {opt_mtrcs_eq} for the relative quantity of the starting material. '
                             'Keep the value exactly as written in the source, together with its basis. Do not convert it to another basis.')
        unit_mats = Primitive(prim_type="string",
                              key=hedr_metrics_unit,
                              description=f'Unit to specify the relative quantity of the raw material, solvent, and other materials. This property is for unit only. '
                              f'"{opt_mtrcs_eq}": molar equivalent vs the selected calculation basis material input. '
                              f'"{opt_mtrcs_v_per_w}": volume (L) of liquid vs weight (kg) of the selected calculation basis material input. '
                              f'"{opt_mtrcs_wwpct}": weight/weight percent vs the designated calculation basis material input. '
                              f'"{opt_mtrcs_wt_gro_abs}": The gross weight (kg) of a material is directly specified by an absolute value. This is an exceptional case. '
                              f'"{opt_mtrcs_vol_abs}": The volume (litre) of a non-solid material is directly specified by an absolute value. This is an exceptional case. '
                              'In the JSON, it is normally assumed that even the starting material is quantified by a relative metrics (equiv or weight percent) in relation to a basis value defined elsewhere. '
                              'Please choose the absolute approach only when it is essential or instructed by the user. '
                              f'This item has to be consistent with the other entry "{hedr_metrics_value}"',
                              enum=list_metrics_unit)
        
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
        
        vessel = Primitive(prim_type='string',
                           key=hedr_vessel,
                           description='Target vessel of the charging/dosing operation.')
        
        vessel_train =  Array(key=hedr_train_vessel,
                              content=vessel,
                             description='A train of vessels. In some cases, not only a single vessel/reactor comes into play, but a sequence of vessels is used. '
                             'For example, two or more solvents are pre-mixed in a mobile tank before being charged to the reaction vessel. '
                             'In another scenario, solvent is charged into a reactor, from which recrystallized slurry has been transferred to a filter dryer. '
                             'Then the rinse is transferred to the filter dryer as well to minimize material loss. ',
                             required=True,
                             nullable=True)
        
        time_ctrl = Primitive(prim_type='string',
                              key=hedr_time_control,
                              enum=list_time_control,
                              description=f'Constraint on time to dose/charge the material. '
                                f'"{timectrl_none}" means time control is no needed. '
                                f'"{timectrl_min}" should be selected when lower limit must be complied. '
                                f'"{timectrl_max}" should be selected when upper limit must be complied. '
                                f'"{timectrl_min_max}" should be selected when the event has to happen in a specific range of time. '
                                f'"Please select {timectrl_placeholder}" if the right option cannot be chosen based on the given information.')
        
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
                              f'"{temprctrl_min_max}" is for a case where the charging/dosing have to take place in a certain specific temperature range. '
                              f'Please select "{temprctrl_placeholder}" if the right option cannot be chosen based on the given infomation.',
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
                              props=[id_input, name_mats, arr_basis_inputs, qty_mats, unit_mats, permiss_error, charging_method, vessel_train, time_ctrl, time_min, time_max, temp_ctrl, temp_min, temp_max],
                              description='Combination of material, quantity, permissible quantity error, charging method, time constraints, temperature range to define each material input. '
                              'Material input appears in various unit operations such as charging/dosing, reslurry washing, cleaning in place, etc. ',
                              required=True
                              )

        return input_entry

        
    def load_from_json_dict(self, json_dict: dict[str, Any]):
        """
        Reads a dict object corresponding to the JSON Schema for Input class and sets each value to the object.
        """
        self.id_input =json_dict[id_input_json]
        self.material_name = json_dict[hedr_material_name]
        self.metrics_unit = json_dict[hedr_metrics_unit]
        self.metrics_val = json_dict[hedr_metrics_value]
        self.list_id_basis_input = json_dict[hedr_basis_array_json]
        if json_dict.get(hedr_error_pct):
            self.error_pct = json_dict[hedr_error_pct]
        else:
            self.error_pct = error_pct_default
            warnings.warn(f'{self.__class__.__name__}.load_from_json_dict(): The given error is empty or zero. {error_pct_default}% as the default value is put for now.', UserWarning)
        self.method = json_dict[hedr_method]
        self.vessel_train = json_dict.get(hedr_train_vessel, [])
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
            else:
                self.material_class = cls_input_mat_other

    def get_name_this(self):
        return self.material_name
    
    def get_vessel_train(self) -> list[str]:
        if self.vessel_train is None:
            self.vessel_train = []
        return self.vessel_train


    def print_input(self):
        def __put_time_control():
            sentence_instruction: str = ''
            if (self.time_control == timectrl_min):
                sentence_instruction = lang_dict_instr_stcs[tag_stc_time_min].format(min=self.time_min)
    
            elif (self.time_control == timectrl_max):
                sentence_instruction = lang_dict_instr_stcs[tag_stc_time_max].format(max=self.time_max)
    
            elif (self.time_control == timectrl_min_max):
                sentence_instruction = lang_dict_instr_stcs[tag_stc_time_min_max].format(min=self.time_min, max=self.time_max)
    
            elif self.time_control == timectrl_placeholder:
                sentence_instruction = lang_dict_chgng_specif[tag_part_instr_timectrl_plchldr]
            
            self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                    method=lang_dict_chgng_specif[tag_part_instr_ini],
                                    content=sentence_instruction,
                                    operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    witness=lang_dict_cmn[tag_flow_cmn_rec_sign])

        def __put_temp_control():
            if self.temp_control == temprctrl_min:
                sentence = lang_dict_instr_stcs[tag_stc_temp_min].format(min=self.temp_min)
                self.flowsheet.put_line(content=sentence, record=lang_dict_chgng_specif[tag_part_rec_temprini])
                self.flowsheet.put_line(record=lang_dict_chgng_specif[tag_part_rec_temprmin])
                self.flowsheet.put_line(record=lang_dict_chgng_specif[tag_part_rec_temprend])

            elif self.temp_control == temprctrl_max:
                sentence = lang_dict_instr_stcs[tag_stc_temp_max].format(max=self.temp_max)
                self.flowsheet.put_line(content=sentence, record=lang_dict_chgng_specif[tag_part_rec_temprini])
                self.flowsheet.put_line(record=lang_dict_chgng_specif[tag_part_rec_temprmax])
                self.flowsheet.put_line(record=lang_dict_chgng_specif[tag_part_rec_temprend])

            elif self.temp_control == temprctrl_min_max:
                sentence = lang_dict_instr_stcs[tag_stc_temp_min_max].format(min=self.temp_min, max=self.temp_max)
                self.flowsheet.put_line(content=sentence, record=lang_dict_chgng_specif[tag_part_rec_temprini])
                self.flowsheet.put_line(record=lang_dict_chgng_specif[tag_part_rec_temprmin])
                self.flowsheet.put_line(record=lang_dict_chgng_specif[tag_part_rec_temprmax])
                self.flowsheet.put_line(record=lang_dict_chgng_specif[tag_part_rec_temprend])

            elif self.temp_control == temprctrl_placeholder:
                sentence = lang_dict_chgng_specif[tag_part_instr_temprctrl_plchldr]
                self.flowsheet.put_line(content=sentence, record=lang_dict_chgng_specif[tag_part_rec_temprini])
                self.flowsheet.put_line(record=lang_dict_chgng_specif[tag_part_rec_temprmin])
                self.flowsheet.put_line(record=lang_dict_chgng_specif[tag_part_rec_temprmax])
                self.flowsheet.put_line(record=lang_dict_chgng_specif[tag_part_rec_temprend])

        def __put_end_of_dosing():
            self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                     method=lang_dict_chgng_specif[tag_part_instr_end],
                                     record=lang_dict_chgng_specif[tag_part_rec_cmpltd],
                                     operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    witness=lang_dict_cmn[tag_flow_cmn_rec_sign])

        def __get_fifo_train(list_vessels: list[str]|None)->Callable[[],str|None]:
            list_this = list_vessels
            if list_this is None:
                list_this = []
            len_this = len(list_this)
            idx = 0
            def fifo_train()->str|None:
                nonlocal idx
                if idx == len_this:
                    return None 
                elif idx == 0:
                    idx += 1
                    return list_this[idx-1]
                else:
                    idx += 1
                    return 'to '+list_this[idx-1]
            return fifo_train

        ##################################################################################################
        ##################################################################################################

        #line-1: Material name and relative quantity
        line_mat = self.put_material(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                     method=lang_dict_chgng_specif[self.method],
                                     record=lang_dict_chgng_specif[tag_part_rec_lot],
                                     operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                     witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
        
        fifo_train = __get_fifo_train(self.vessel_train)

        #line-2: QTY instruction and record
        self.instruct_qty_range(method=fifo_train(),
                                record=lang_dict_chgng_specif[tag_part_rec_qyt_input],
                                line_mat=line_mat)

        #line-3: Balance info
        self.flowsheet.put_line(method=fifo_train(),
                                record=lang_dict_chgng_specif[tag_part_rec_balance_id])

        #For liquid only, container ID, flex ID 
        if self.method in (method_liq, method_shower, method_mobile_tank):
            self.flowsheet.put_line(method=fifo_train(),
                                     record=lang_dict_chgng_specif[tag_part_rec_cntnr_id])
            self.flowsheet.put_line(method=fifo_train(),
                                    record=lang_dict_chgng_specif[tag_part_rec_hose],
                                    operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
        elif self.method == method_press:
            self.flowsheet.put_line(method=fifo_train(),
                                    record=lang_dict_chgng_specif[tag_part_rec_cntnr_id],
                                    operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                    witness=lang_dict_cmn[tag_flow_cmn_rec_sign])

        vessel_via = fifo_train()
        while vessel_via is not None:
            self.flowsheet.put_line(method=vessel_via)
            vessel_via = fifo_train()
        else:
            self.flowsheet.linefeed()
        
        #for both liq and solid; temp and time control.
        if not (self.time_control == timectrl_none or self.time_control is None):
            __put_time_control()


        if not (self.temp_control == temprctrl_none or self.temp_control is None):
            __put_temp_control()

        __put_end_of_dosing()
        self.flowsheet.linefeed()

    @staticmethod
    def generate_test_df(material_name:str=None,
                         metrics_val:float=None,
                         metrics_unit:str=None,
                         error_pct:float=error_pct_default,
                         method:str=None,
                         vessel_train:list[str]=None,
                         time_control:str=timectrl_none,
                         time_min:float=None,
                         time_max:float=None,
                         temp_control:str=temprctrl_none,
                         temp_min:float=None,
                         temp_max:float=None,
                         id_input:int=None,
                         list_id_basis_input:list[int]=None)->pd.DataFrame:
        hedr:list[str] = defs.list_hedr_cmn_io_dtil + list_hedr
        content: list[any] = [None]*len(hedr)
        s:pd.Series = pd.Series(data=content, index=hedr)
        df = s.to_frame().T
        df.at[df.index[0], hedr_material_name]=material_name
        df.at[df.index[0], hedr_metrics_value]=metrics_val
        df.at[df.index[0], hedr_metrics_unit]=metrics_unit
        df.at[df.index[0], hedr_error_pct]=error_pct
        df.at[df.index[0], hedr_method]=method
        # df.at[df.index[0], hedr_vessel]=vessel
        df.at[df.index[0], hedr_train_vessel]=vessel_train
        df.at[df.index[0], hedr_time_control]=time_control
        df.at[df.index[0], hedr_time_min]=time_min
        df.at[df.index[0], hedr_time_max]=time_max
        df.at[df.index[0], hedr_temp_control]=temp_control
        df.at[df.index[0], hedr_temp_min]=temp_min
        df.at[df.index[0], hedr_temp_max]=temp_max
        df.at[df.index[0], id_input_json]=id_input
        df.at[df.index[0], hedr_basis_array_json]=list_id_basis_input

        return df

    @staticmethod
    def add_to_test_df(df: pd.DataFrame=None,
                       material_name:str=None,
                       metrics_val:float=None,
                       metrics_unit:str=None,
                       error_pct:float=error_pct_default,
                       method:str=None,
                       vessel_train:list[str]=None,
                       time_control:str=timectrl_none,
                       time_min:float=None,
                       time_max:float=None,
                       temp_control:str=temprctrl_none,
                       temp_min:float=None,
                       temp_max:float=None,
                       id_input:int=None,
                       list_id_basis_input:list[int]=None)->None:
        width:int = len(df.columns)
        new_row:list[Any] = [None]*width
        row:int = len(df)
        df.loc[row]=new_row
        df.at[row, hedr_material_name]=material_name
        df.at[row, hedr_metrics_value]=metrics_val
        df.at[row, hedr_metrics_unit]=metrics_unit
        df.at[row, hedr_error_pct]=error_pct
        df.at[row, hedr_method]=method
        # df.at[row, hedr_vessel]=vessel
        df.at[row, hedr_train_vessel]=vessel_train
        df.at[row, hedr_time_control]=time_control
        df.at[row, hedr_time_min]=time_min
        df.at[row, hedr_time_max]=time_max
        df.at[row, hedr_temp_control]=temp_control
        df.at[row, hedr_temp_min]=temp_min
        df.at[row, hedr_temp_max]=temp_max
        df.at[row, id_input_json]=id_input
        df.at[row, hedr_basis_array_json]=list_id_basis_input


    def mark_as_tgt(self):
        self.id_input = opt_special_id_basis_tgt
        self.material_name = self.mats_data.get_name_tgt()
        self.material_class = cls_input_mat_tgt
        self.mw = self.mats_data.get_mw(material_name=self.material_name)
        if self.mats_data.get_density(material_name=self.material_name) is not None:
            self.density = self.mats_data.get_density(material_name=self.material_name)
        self.conc_assay = 100.0 #This doesn't make a chemical sence, but do no harm. Just to suppress an annoying message on Excel. 
        self.error_pct = None

    def calc_qty(self)->bool:
        if self.qty_calc_compltd:
            return True
        
        if self.mats_data is None:
            raise RuntimeError(f"{self.__class__.__name__}.calc_qty() (input of \"{self.material_name}\"): No material data for provided in the material input worksheet.")

        if self.list_id_basis_input is None or len(self.list_id_basis_input) == 0:
            if (self.material_class not in (cls_input_mat_sm, cls_input_mat_tgt)
                and self.metrics_unit not in (opt_mtrcs_wt_gro_abs, opt_mtrcs_vol_abs)):
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
                if __is_pos_num(self.conc_assay):
                    self.qty_kg_net = self.qty_kg_gross * (self.conc_assay/100.0)
                else:
                    self.qty_kg_net = self.qty_kg_gross
                    warnings.warn(f'{self.__class__.__name__}.calc_qty(): No valid assay provided for "{self.material_name}" (input ID {self.id_input}) '
                                  'where the quantity is directly specified by gross weight. '
                                  'Assay=100% is assumed to estimate the net weight from the gross one.',
                                  UserWarning)
                if __is_pos_num(self.mw):
                    self.mol = self.qty_kg_net * 1000 / self.mw
                else:
                    warnings.warn(f'{self.__class__.__name__}.calc_qty(): No valid molecule weight provided for "{self.material_name}" (input ID {self.id_input}) ', UserWarning)
                __calc_vol()


            elif self.metrics_unit == opt_mtrcs_vol_abs:
                self.vol_litre = self.metrics_val
                if __is_pos_num(self.density):
                    self.qty_kg_gross = self.vol_litre * self.density
                else:
                    self.qty_kg_gross = self.vol_litre * 1.0
                    warnings.warn(f'{self.__class__.__name__}.calc_qty(): No valid density provided for "{self.material_name}" (input ID {self.id_input}) '
                                  'where the quantity is directly specified by volume.'
                                  'd=1 kg/L is assumed to estimate the gross weight for internal purpose.',
                                  UserWarning)    
                if __is_pos_num(self.conc_assay):
                    self.qty_kg_net = self.qty_kg_gross * (self.conc_assay / 100.0)
                else:
                    self.qty_kg_net = self.qty_kg_gross
                    warnings.warn(f'{self.__class__.__name__}.calc_qty(): No valid assay provided for "{self.material_name}" (input ID {self.id_input}) '
                                'where the quantity is directly specified by volume.'
                                'assay=100% is assumed to estimate the net weight for internal purpose.',
                                UserWarning) 
                if __is_pos_num(self.mw):
                    self.mol = self.qty_kg_net * 1000 / self.mw
                else:
                    warnings.warn(f'{self.__class__.__name__}.calc_qty(): No valid molecule weight provided for "{self.material_name}" (input ID {self.id_input}) ', UserWarning)

                        
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
            # if mw_this is None or not isinstance(mw_this, (float, int)) or mw_this <= 0:
            if not __is_pos_num(mw_this):
                raise RuntimeError(f"{__class__.__name__}.calc_qty() (input of \"{self.material_name}\"): Invalid molecular weight for this material.")
            conc_assay_this = self.mats_data.get_conc_assay(material_name = self.material_name)
            # if conc_assay_this is None or not isinstance(conc_assay_this, (float, int)) or conc_assay_this <= 0:
            if not __is_pos_num(conc_assay_this):
                raise RuntimeError(f"{__class__.__name__}.calc_qty() (input of \"{self.material_name}\"): Invalid assay for this material.")
            self.qty_kg_net = self.mol * mw_this/1000
            self.qty_kg_gross = self.qty_kg_net / (conc_assay_this/100.0)
            self.error_kg_gross = self.qty_kg_gross * (self.error_pct/100.0)

            dens_this = self.mats_data.get_density(material_name=self.material_name)
            # if dens_this is None or not isinstance(dens_this, (float, int)) or dens_this <= 0:
            if not __is_pos_num(dens_this):
                dens_this = 1.0
                warnings.warn(f'{__class__.__name__}.calc_qty() (input of \"{self.material_name}\"): No density information provided tor this material.'
                              '1.0 is assumed to estimate the volume.',
                              RuntimeWarning)
            self.vol_litre = self.qty_kg_gross / dens_this
            self.qty_calc_compltd = True
            return True
        
        elif self.metrics_unit == opt_mtrcs_v_per_w:
            net_wt_basis = 0.0

            #First, we need the sum of net weight of the basis material.
            for dep_id in self.list_id_basis_input:
                input_depended = self.proc.get_input(dep_id)
                if input_depended is None:
                    raise RuntimeError(f"{__class__.__name__}.calc_qty() (input of \"{self.material_name}\"): Dependent input with ID \"{dep_id}\" not found.")
                if input_depended.qty_kg_net is None:
                    return False
                else:
                    net_wt_basis += input_depended.qty_kg_net
            
            # volume -> gross weight -> permissible error
            self.vol_litre = net_wt_basis * self.metrics_val
            dens_this = self.mats_data.get_density(material_name=self.material_name)
            # if dens_this is None or not isinstance(dens_this, (float, int)) or dens_this <= 0:
            if not __is_pos_num(dens_this):
                dens_this = 1.0
                warnings.warn(f'{__class__.__name__}.calc_qty() (input of \"{self.material_name}\"): No density information provided tor this material.'
                              '1.0 is assumed to estimate the volume.',
                              RuntimeWarning)
            self.qty_kg_gross = self.vol_litre * dens_this
            self.error_kg_gross = self.qty_kg_gross * (self.error_pct/100.0)
            self.qty_calc_compltd = True

            # Next, net weight
            conc_assay_this = self.mats_data.get_conc_assay(material_name = self.material_name)
            #if conc_assay_this is None or not isinstance(conc_assay_this, (float, int)) or conc_assay_this <= 0:
            if not __is_pos_num(conc_assay_this):
                conc_assay_this = 100.0
                warnings.warn(f'{self.__class__.__name__}.calc_qty() (input of "{self.material_name}"): No valid assay information provided for this material. '
                              '100.0 is assumed to estimate the net weight for internal purpose.',
                              RuntimeWarning)
                # self.qty_calc_compltd = True
                # return True
            self.qty_kg_net = self.qty_kg_gross * (conc_assay_this/100.0)

            # Mol
            mw_this = self.mats_data.get_mw(material_name = self.material_name)
            # if mw_this is None or not isinstance(mw_this, (float, int)) or mw_this <= 0:
            if not __is_pos_num(mw_this):
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
            # if assay_this is None or not isinstance(assay_this, (float, int)) or assay_this <= 0:
            if not __is_pos_num(assay_this):
                assay_this = 100.0
                warnings.warn(f'{__class__.__name__}.calc_qty() (input of \"{self.material_name}\"): No valid assay information provided for this material. 100.0 is assumed.',
                              RuntimeWarning)
            self.qty_kg_gross = self.qty_kg_net / (assay_this/100)
            self.error_kg_gross = self.qty_kg_gross * (self.error_pct/100.0)
            dens_this = self.mats_data.get_density(material_name=self.material_name)
            # if dens_this is None or not isinstance(dens_this, (float, int)) or dens_this <= 0:
            if not __is_pos_num(dens_this):
                dens_this = 1.0
                warnings.warn(f'{__class__.__name__}.calc_qty() (input of \"{self.material_name}\"): No density information provided for this material. 1.0 is assumed to estimate the volume.',
                              RuntimeWarning)
            self.vol_litre = self.qty_kg_gross / dens_this
            mw_this = self.mats_data.get_mw(material_name=self.material_name)
            # if mw_this is None or not isinstance(mw_this, (float, int)) or mw_this <= 0:
            if not __is_pos_num(mw_this):
                self.qty_calc_compltd = True
                return True
            self.mol = self.qty_kg_net*1000 / mw_this
            self.qty_calc_compltd = True
            return True

        elif self.metrics_unit == opt_mtrcs_wt_gro_abs:
            # The gross weight (kg) is directly given. No basis input is needed.
            if not __is_pos_num(self.metrics_val):
                raise ValueError(f'{self.__class__.__name__}.calc_qty() (input of "{self.material_name}"): '
                                 f'"{opt_mtrcs_wt_gro_abs}" requires a positive "{hedr_metrics_value}", but got {self.metrics_val}.')
            self.qty_kg_gross = self.metrics_val
            self.error_kg_gross = self.qty_kg_gross * (self.error_pct/100.0)

            # Net weight
            if __is_pos_num(self.conc_assay):
                self.qty_kg_net = self.qty_kg_gross * (self.conc_assay/100.0)
            else:
                self.qty_kg_net = self.qty_kg_gross
                warnings.warn(f'{self.__class__.__name__}.calc_qty(): No valid assay provided for "{self.material_name}" (input ID {self.id_input}) '
                              'where the quantity is directly specified by gross weight. '
                              'Assay=100% is assumed to estimate the net weight for internal purpose.',
                              UserWarning)

            # Mol (only when MW is available)
            if __is_pos_num(self.mw):
                self.mol = self.qty_kg_net * 1000 / self.mw

            __calc_vol()
            self.qty_calc_compltd = True
            return True

        elif self.metrics_unit == opt_mtrcs_vol_abs:
            # The volume (L) is directly given. No basis input is needed.
            if not __is_pos_num(self.metrics_val):
                raise ValueError(f'{self.__class__.__name__}.calc_qty() (input of "{self.material_name}"): '
                                 f'"{opt_mtrcs_vol_abs}" requires a positive "{hedr_metrics_value}", but got {self.metrics_val}.')
            self.vol_litre = self.metrics_val

            # Gross weight -> permissible error
            if __is_pos_num(self.density):
                self.qty_kg_gross = self.vol_litre * self.density
            else:
                self.qty_kg_gross = self.vol_litre * 1.0
                warnings.warn(f'{self.__class__.__name__}.calc_qty(): No valid density provided for "{self.material_name}" (input ID {self.id_input}) '
                              'where the quantity is directly specified by volume. '
                              'd=1 kg/L is assumed to estimate the gross weight for internal purpose.',
                              UserWarning)
            self.error_kg_gross = self.qty_kg_gross * (self.error_pct/100.0)

            # Net weight
            if __is_pos_num(self.conc_assay):
                self.qty_kg_net = self.qty_kg_gross * (self.conc_assay/100.0)
            else:
                self.qty_kg_net = self.qty_kg_gross
                warnings.warn(f'{self.__class__.__name__}.calc_qty(): No valid assay provided for "{self.material_name}" (input ID {self.id_input}) '
                              'where the quantity is directly specified by volume. '
                              'Assay=100% is assumed to estimate the net weight for internal purpose.',
                              UserWarning)

            # Mol (only when MW is available)
            if __is_pos_num(self.mw):
                self.mol = self.qty_kg_net * 1000 / self.mw

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

    def is_based_on_tgt(self)->bool:
        if not self.list_id_basis_input:
            return False
        return opt_special_id_basis_tgt in self.list_id_basis_input

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
            excel_formula_mat = f'={{{defs.plchld_flow_col_mat}}}{line}'
        elif self.material_class == cls_input_mat_tgt:
            excel_formula_mat=''
        elif self.metrics_unit == opt_mtrcs_eq:
            excel_formula_mat = f'={{{defs.plchld_flow_col_mat}}}{line}&" ("&{{{defs.plchld_flow_col_equiv}}}{line}&"equiv vs "&{{{defs.plchld_flow_col_name_basis}}}{line}&")"'
        elif self.metrics_unit == opt_mtrcs_v_per_w:
            excel_formula_mat = f'={{{defs.plchld_flow_col_mat}}}{line}&" ("&{{{defs.plchld_flow_col_v_per_w}}}{line}&"v/w vs "&{{{defs.plchld_flow_col_name_basis}}}{line}&")"'               
        elif self.metrics_unit == opt_mtrcs_wwpct:
            excel_formula_mat = f'={{{defs.plchld_flow_col_mat}}}{line}&" ("&{{{defs.plchld_flow_col_wwpct}}}{line}&"w/w% vs "&{{{defs.plchld_flow_col_name_basis}}}{line}&")"'

        if self.metrics_unit == opt_mtrcs_wt_gro_abs:
            self.flowsheet.put_material(time=time,
                                            method=method,
                                            content=excel_formula_mat,
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
            self.flowsheet.put_material(time=time,
                                            method=method,
                                            content=excel_formula_mat,
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
            self.flowsheet.put_material(time=time,
                                            method=method,
                                            content=excel_formula_mat,
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
            self.flowsheet.put_material(time=time,
                                            method=method,
                                            content=excel_formula_mat,
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
            self.flowsheet.put_material(time=time,
                                            method=method,
                                            content=excel_formula_mat,
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
        
        # excel_formular_qty = f'=TEXT({fsht.alph_col_kg_gro}{line_mat},"0.00")&" ± "&TEXT({fsht.alph_col_err_abs}{line_mat},"0.00")&" kg"'
        excel_formular_qty = f'=TEXT({{{defs.plchld_flow_col_kg_gro}}}{line_mat},"0.00")&" ± "&TEXT({{{defs.plchld_flow_col_err_abs}}}{line_mat},"0.00")&" kg"'
        line_qty = self.flowsheet.put_line(time=time, method=method, content=excel_formular_qty, record=record, operator=operator, witness=witness)

        return line_qty


    def link_inputs(self):
        if self.proc is None:
            raise ValueError(f'{self.__class__.__name__}.put_qty_material(): Material input (inputs:GetInputs) must be provided.')
        if self.line_fs is None:
            raise RuntimeError(f'{self.__class__.__name__}.put_qty_material(): '
                    f'Input "{self.material_name}" (ID {self.id_input}) has an empty fs_line_mat.')


        #>>>>>>>>>>>>>>>>>>>> func in func from here >>>>>>>>>>>>>>>>>>>>

        def __prep_ref(plchld_alph_col:str=None, list_rows:list[int]=None)->str:
            if plchld_alph_col is None:
                raise ValueError(f'{self.__class__.__name__}.put_qty_material().__prep_ref(): An argument "alph_col" is None. Alphabet column identifier is needed.')
            if not list_rows:
                raise ValueError(f'{self.__class__.__name__}.put_qty_material().__prep_ref(): An argument "list_rows" is None or len(list_rows)==0. A list of depended row is needed.')
            
            if len(list_rows) == 1:
                return f'={plchld_alph_col}{list_rows[0]}'
            else:
                list_cell:list[str] = []
                for row in list_rows:
                    list_cell.append(f'{plchld_alph_col}{row}')

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
                self.flowsheet.put_links(line_fs_this=self.line_fs,
                                         name_basis=name_basis,
                                         ref_mol_basis=__prep_ref(plchld_alph_col=f'{{{defs.plchld_flow_col_mol}}}', list_rows=list_lines_basis))
            elif self.metrics_unit == opt_mtrcs_v_per_w:
                self.flowsheet.put_links(line_fs_this=self.line_fs,
                                         name_basis=name_basis,
                                         ref_kg_net_basis=__prep_ref(plchld_alph_col=f'{{{defs.plchld_flow_col_kg_net}}}', list_rows=list_lines_basis))
            elif self.metrics_unit == opt_mtrcs_wwpct:

                self.flowsheet.put_links(line_fs_this=self.line_fs,
                                         name_basis=name_basis,
                                         ref_kg_net_basis=__prep_ref(plchld_alph_col=f'{{{defs.plchld_flow_col_kg_net}}}', list_rows=list_lines_basis))
            else:
                raise RuntimeError(f'{self.__class__.__name__}: Invalid metrics unit "{self.metrics_unit}" for the input ID {self.id_input} of "{self.material_name}".')



            
            



    