import pandas as pd
import flow_draw.definitions as defs
from flow_draw.project.process.unit_operations import unit_operation as uo
from flow_draw.data_io import process_io
from flow_draw.materials import materials as mats
from flow_draw.data_io.flowsheet import Flowsheet as fsht
from flow_draw.trait_def.trait_def import GetMats
#from typing import List


header_precomment = process_io.header_detail_precomment #Don't include this in the specific header list!!!
header_postcomment = process_io.header_detail_postcomment #Don't include this in the specific header list!!!

header_material_name = 'Material Name'
header_metrics_value = 'Metrics Value'
header_metrics_unit = 'Metrics Unit'
header_error = 'Permissible Error (%)'
header_method = 'Charging Method'
header_time_control = 'Time Control'
header_time_min = 'Minimum Time (min)'
header_time_max = 'Maximum Time (min)'
header_temp_control = 'Temp Control'
header_temp_min = 'Minimum Temp (deg-C)'
header_temp_max = 'Maximum Temp (deg-C)'

list_header_items = [
    header_material_name,
    header_metrics_value,
    header_metrics_unit,
    header_error,
    header_method,
    header_time_control,
    header_time_min,
    header_time_max,
    header_temp_control,
    header_temp_min,
    header_temp_max
]


charging_method_liq = 'liquid_port'
charging_method_shower = 'shower'
charging_method_press = 'press_vessel'
charging_method_pow ='powder_port'
charging_method_placeholder = 'placeholder'
list_charging_method =[
    charging_method_liq,
    charging_method_shower,
    charging_method_press,
    charging_method_pow,
    charging_method_placeholder
]

time_control_none = "No time control"
time_control_min="Time control with minimum"
time_control_max="Time control with maximum"
time_control_min_max='Time control with minimum and maximum'
time_control_placeholder = 'Placeholder'
list_time_control =[
    time_control_none,
    time_control_min,
    time_control_max,
    time_control_min_max,
    time_control_placeholder
]

temp_control_none = "No temp control"
temp_control_min="Temp control with minimum"
temp_control_max="Temp control with maximum"
temp_control_min_max='Temp control with minimum and maximum'
temp_control_placeholder = 'Placeholder'
list_temp_control =[
    temp_control_none,
    temp_control_min,
    temp_control_max,
    temp_control_min_max,
    temp_control_placeholder
]

#list_metrics_unit = [defs.tag_metrics_equiv, defs.tag_metrics_vol]
list_metrics_unit = defs.list_metrics_unit

error_range_placeholder='place holder'
list_error_range = [None, 1.0, None, None, None, 5.0, error_range_placeholder]

menu_dict ={
    header_metrics_unit: list_metrics_unit,
    header_method: list_charging_method,
    header_time_control: list_time_control,
    header_temp_control: list_temp_control
}


class Charging(uo.UnitOperation, uo_name=defs.op_charging):
    """
    TODO: Make some comment here.
    """
    
    def __init__(self, caller: GetMats=None, flow_sheet:fsht.Flowsheet=None, operation_seq:int=None, num_subitems: int =None, edit_comment:str=None):
        """
        Initialises the newly created instance of the class Charging.

        Parameters
        ---------------
        caller: flow_draw.trait_def.trait_def.GetMats
            The calling object. In the case of the class Charging, GetMats class is expected. From the given caller object, Charging expects materials.Materials given by get_mats() method.
        """
        super().__init__(caller=caller, flow_sheet=flow_sheet, operation_seq=operation_seq, num_subitems=num_subitems, edit_comment=edit_comment)
        # self.mats_data: mats.Materials = GetMats(self.caller).get_mats() #なんかやだからキャストする。
        self.mats_data = GetMats(self.caller).get_mats()
        self.input_count = 0
        self.inputs: list[Input] = []

        self.output_unit_operation()

    def get_detail_header(self) -> list[str]:
        return list_header_items

    def load_params_from_df(self, df: pd.DataFrame):
        """
        Loads necessary parameters from a DataFrame object.
        The header items must be in line with the definition the class Charging.
        The header items can be passed from the get_detail_header() of each UnitOperation-drived class.
        This is the overriding mehtod in the class Charging..
        """
        #TODO: please check if my implementation is sufficient!!!!
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

    def output_unit_operation(self):
        self.flow_sheet.header_organizer(op_nr=self.operation_seq, title=self.unit_operation)
        if not (self.pre_comment == None or self.pre_comment == ''):
            self.flow_sheet.put_body_comments(self.pre_comment)

        for temp_inpt in self.inputs:
            self.flow_sheet.put_line(time=defs.part_time,
                                     method=temp_inpt.method,
                                     content=temp_inpt.material_name,
                                     record=defs.part_record_lot,
                                     operator=defs.part_signature,
                                     witness=defs.part_signature)

            #line-2: QTY instruction and record
            str_qty = f'{temp_inpt.qty_kg}±{temp_inpt.error_kg} kg'
            self.flow_sheet.put_line(content=str_qty, record=defs.part_record_input)

            #For liquid only, flex ID 
            if (temp_inpt.method == charging_method_liq or
                temp_inpt.method == charging_method_press or
                temp_inpt.method == charging_method_shower):
                self.flow_sheet.put_line(record=defs.part_record_flex,
                                         operator=defs.part_signature,
                                         witness=defs.part_signature)
            
            #for both liq and solid; temp and time control.
            if not (temp_inpt.time_control == time_control_none or temp_inpt.time_control is None):
                self.__put_time_control(input=temp_inpt)

            if not (temp_inpt.temp_control == temp_control_none or temp_inpt.temp_control is None):
                self.__put_temp_control(input=temp_inpt)              
     
            self.__put_end_of_dosing()
            self.flow_sheet.linefeed()

        if not (self.post_comment == None or self.post_comment == ''):
            self.flow_sheet.put_body_comments(self.post_comment)
            self.flow_sheet.linefeed()
            
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
        if (input.time_control == time_control_min):
            sentence_instruction = f'*滴下時間{input.time_min}以上'

        elif (input.time_control == time_control_max):
            sentence_instruction = f'*滴下時間{input.time_max}以内'

        elif (input.time_control == time_control_min_max):
            sentence_instruction = f'*滴下時間{input.time_min}～{input.time_max}以内'
        
        self.flow_sheet.put_line(time=defs.part_time,
                                method=defs.part_method_charging_ini,
                                content=sentence_instruction,
                                operator=defs.part_signature,
                                witness=defs.part_signature)


    def __put_temp_control(self, input: Input=None):
        if input.temp_control == temp_control_min:
            sentence = "仕込み中内温"+str(input.t_i_min)+"℃以上"
            self.flow_sheet.put_line(content=sentence, record=defs.part_record_temp_ini)
            self.flow_sheet.put_line(record=defs.part_record_temp_min)
            self.flow_sheet.put_line(record=defs.part_record_temp_end)

        elif input.temp_control == temp_control_max:
            sentence = "仕込み中内温"+str(input.t_i_max)+"℃以下"
            self.flow_sheet.put_line(content=sentence, record=defs.part_record_temp_ini)
            self.flow_sheet.put_line(record=defs.part_record_temp_max)
            self.flow_sheet.put_line(record=defs.part_record_temp_end)

        elif input.temp_control == temp_control_min_max:
            sentence = "仕込み中内温"+str(input.t_i_min)+'～'+str(input.t_i_max)+"℃"
            self.flow_sheet.put_line(content=sentence, record=defs.part_record_temp_ini)
            self.flow_sheet.put_line(record=defs.part_record_temp_min)
            self.flow_sheet.put_line(record=defs.part_record_temp_max)
            self.flow_sheet.put_line(record=defs.part_record_temp_end)

    def __put_end_of_dosing(self):
            self.flow_sheet.put_line(time=defs.part_time,
                                     method=defs.part_method_charging_end,
                                     record=defs.part_check_charged,
                                     operator=defs.part_signature,
                                     witness=defs.part_signature)

class Input:
    """This class is for each material charged, each instance correspnds to each dosage in a charging operation.
    """
    def __init__(self, mats_data: mats.Materials):
        self.mats_data = mats_data
        self.material_name = ""
        self.metrics_unit = ""
        self.metrics_val = None
        self.error_pct = None
        self.qty_kg = None
        self.error_kg = None
        self.method = ""
        self.time_control = None
        self.time_min = None
        self.time_max = None
        self.temp_control = None
        self.t_i_min = None
        self.t_i_max = None
    
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
        if defs.list_yesno[specif_yesno] == defs.tag_yes:
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
        if self.time_control == time_control_min or self.time_control == time_control_min_max:
            print("Charging time lower limit?: ", end='')
            self.time_min = input()
        if self.time_control == time_control_max or self.time_control == time_control_min_max:
            print("Charging time upper limit?: ", end='')
            self.time_max = input()
        
        print("Specicfy a temperature control method?: ")
        for idx in range(len(list_temp_control)):
            print(str(idx)+': '+list_temp_control[idx])
        print("> ", end='')
        choice_temp_control = int(input())
        self.temp_control = list_temp_control[choice_temp_control]
        if self.temp_control == temp_control_min or self.temp_control == temp_control_min_max:
            print("Charging temperature (℃) lower limit?: ", end='')
            self.t_i_min = float(input())
        if self.temp_control == temp_control_max or self.temp_control == temp_control_min_max:
            print("Charging temperature (℃) upper limit?: ", end='')
            self.t_i_max = float(input())
        
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
        self.material_name = ser[header_material_name]
        self.metrics_unit = ser[header_metrics_unit]
        self.metrics_val = ser[header_metrics_value]
        self.error_pct = ser[header_error]
        self.method  = ser[header_method]
        self.time_control = ser[header_time_control]
        if self.time_control == time_control_min or self.time_control == time_control_min_max:
            self.time_min = ser[header_time_min]
        if self.time_control == time_control_max or self.time_control == time_control_min_max:
            self.time_max = ser[header_time_max]
        self.temp_control = ser[header_temp_min]
        if self.temp_control == temp_control_min or self.temp_control == temp_control_min_max:
            self.t_i_min = ser[header_temp_min]
        if self.temp_control == temp_control_max or self.temp_control == temp_control_min_max:
            self.t_i_max = ser[header_temp_max]
        self.__calc_qty()

    def test_data_creation1(self):
        self.material_name = 'H2O'
        self.metrics_unit = defs.tag_metrics_vol
        self.metrics_val = 1.0
        self.error_pct = 5.0
        #self.qty_kg = None
        #self.error_kg = None
        self.method = charging_method_liq
        self.time_control = time_control_min
        self.time_min = '1h'
        self.time_max = None
        self.temp_control = temp_control_min_max
        self.t_i_min = 15
        self.t_i_max = 25
        self.__calc_qty()

    def test_data_creation2(self):
        self.material_name = 'NaCl'
        self.metrics_unit = defs.tag_metrics_equiv
        self.metrics_val = 2.0
        self.error_pct = 5.0
        #self.qty_kg = None
        #self.error_kg = None
        self.method = charging_method_pow
        self.time_control = time_control_none
        self.time_min = None
        self.time_max = None
        self.temp_control = temp_control_min_max
        self.t_i_min = 15
        self.t_i_max = 25
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
        if self.metrics_unit == defs.tag_metrics_equiv:
            self.qty_kg = self.mats_data.to_kilogram(material_name = self.material_name, equiv=self.metrics_val)
            self.error_kg = self.qty_kg * (self.error_pct/100.0)
        elif self.metrics_unit == defs.tag_metrics_vol:
            self.qty_kg = self.mats_data.to_kilogram(material_name = self.material_name, vol_per_weight=self.metrics_val)
            self.error_kg = self.qty_kg * (self.error_pct/100.0)
        else:
            raise ValueError('metrics_unit not defined')

