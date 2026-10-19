"""
Material input (one charge/dose of a material) and the constants that describe it.
Split out of uo_charging.py so that unit operations other than Charging can reuse Input.
"""
import pandas as pd
import warnings
import flow_draw.definitions as defs
from flow_draw.materials import materials as mats
from flow_draw.data_io.flowsheet import Flowsheet
from flow_draw.trait_def.trait_def import GetMats, GetInputs
from flow_draw.data_io.json_io import Objason, Primitive, Array


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

id_input_json = 'Material_Input_ID'
"""The key to a material input ID for JSON data exchange."""

hedr_basis_input = 'Calc_Basis_Material_Input_ID'
"""The key to the calculation basis material input ID for JSON data exchange."""

hedr_basis_array_json = 'Array_Calc_Basis'
"""The key to the array of calculation basis material input IDs for JSON data exchange."""

entry_input_json = 'charging_input_entry'
"""The key to a material input entry for JSON data exchange."""

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
            warnings.warn(message=f"{__class__.__name__}: mats_data is None",
                          category=RuntimeWarning)
        else:
            self.calc_qty()
            self.mw = self.mats_data.get_mw(self.material_name)
            self.density = self.mats_data.get_density(self.material_name)
            self.conc_assay = self.mats_data.get_conc_assay(self.material_name)

    @staticmethod
    def get_json_schema(caller: GetMats=None)-> Objason:
        mats_data: mats.Materials = caller.get_mats() 
        list_mats=mats_data.get_list_mats()
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
                                f'If the target material is designated as the calculation basis, please put {opt_special_id_basis_tgt}.',
                                nullable=False,
                                required=True)
        arr_basis_inputs = Array(key=hedr_basis_array_json,
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
                              props=[id_input, name_mats, qty_mats, unit_mats, arr_basis_inputs, permiss_error, charging_method, time_ctrl, time_min, time_max, temp_ctrl, temp_min, temp_max],
                              description='Combination of material, quantity, permissible quantity error, charging method, time constraints, temperature range to define each charging/dosing operation.'
                             )

        return input_entry

        
    def load_from_json_dict(self, json_dict: dict[str, any]):
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
        self.conc_assay = 100.0 #This doesn't make a chemical sence, but do no harm. Just to suppress an annoying message on Excel. 
        self.error_pct = None

    def calc_qty(self)->bool:
        if self.qty_calc_compltd:
            return True
        
        if self.mats_data is None:
            raise RuntimeError(f"{self.__class__.__name__}.calc_qty() (input of \"{self.material_name}\"): No material data for provided in the material input worksheet.")

        if self.list_id_basis_input is None or len(self.list_id_basis_input) == 0:
            # if self.material_class != cls_input_mat_sm and self.material_class != cls_input_mat_tgt:
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



            
            



    