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
from flow_draw.batch.process.unit_operations.material_input import Input  # Input and its constants; kept importable as chgng.<name> for existing callers


header_precomment = defs.hedr_cmn_io_dtil_precmnt #Don't include this in the specific header list!!!
header_postcomment = defs.hedr_cmn_io_dtil_postcmnt #Don't include this in the specific header list!!!


#List below
# list_header_items = [hedr_material_name,
#                      hedr_metrics_value,
#                      hedr_metrics_unit,
#                      hedr_error_pct,
#                      hedr_method,
#                      hedr_time_control,
#                      hedr_time_min,
#                      hedr_time_max,
#                      hedr_temp_control,
#                      hedr_temp_min,
#                      hedr_temp_max]

arry_inputs_json = 'arr_charging_input_entry'
"""The key to a list of material input entries."""

# obj_charging_json = 'charging_stage'
"""The key to the unit operation of charging."""


# dict_dtil_drpdwn = {hedr_metrics_unit : list_metrics_unit,
#                     hedr_method : list_charging_method,
#                     hedr_time_control : list_time_control,
#                     hedr_temp_control : list_temp_control}
"""The dict[str, list[str]] for drop-down lists for detail input"""


#Language dictionary for unit operation title. Although only 'charging is needed'
lang_dict_uo_titles = defs.dict_jp_part_uo_titles


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
        hedr_input = Input.get_detai_header()
        return hedr_input
    
    def get_detail_option_menu(self) -> Optional[dict[str, list[str]]]:
        opt_menu_input = Input.get_detail_option_menu()
        return opt_menu_input

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
            new_input = Input(get_mats=self.caller, get_inputs=self.caller, flowsheet=self.flowsheet)
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
            new_input = Input(get_mats=self.caller, get_inputs=self.caller, flowsheet=self.flowsheet)
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

        if not (self.post_comment == None or self.post_comment == ''):
            self.flowsheet.put_body_comments(self.post_comment)
            self.flowsheet.linefeed()
