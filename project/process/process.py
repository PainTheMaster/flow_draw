from typing import List
from flow_draw.project.process.unit_operations import unit_operation
from flow_draw.project.process.unit_operations.unit_operation import UnitOperation as uo
from flow_draw.data_io.input_form import InputForm as inpt
from flow_draw.flow_output.flowsheet import Flowsheet as fsht

class Process:
    """
    The Process is for a process, which consists of many unit operations. The class holds a name, an instance of InputForm class, a sries of UnitOperation(s).

    Attributes
    -----------
    name: str
        Simply the name of the process. Note that this will be passed to the InputForm class to create an instance. Thie will be eventually included in the file name for the input form.
    num_uo:int
        Number of unit operations
    data_input: flow_draw.data_io.InputForm
        Data input form. This class manages process data input. The object holds the path to an input form (Excel file), creates it, load the data. The name of the input form is associated with the process name. 
    list_uo: List[flow_draw.project.process.unit_operations.UnitOperation]
        A list of unit operations that constitute the process. The sequence in this list is identical to that on the flowsheet in the real world.
    flowsheet: flow_draw.flow_output.Flowsheet
        A Flowsheet object that manages the flowsheet output.
    """
    def __init__(self, process_name:str, num_uo: int):
        """
        Patameters
        --------------
        name: string
            The name of the process. The name is incorporated in the name of the input file (Excel).
        num_uo: int
            The number of unit operations that constitutes the process. This parameter will be passed to the InputForm class in order to generate the summary input form with the proper number of input rows.
        
        Returns
        --------------
        None
        """
        self.process_name = process_name
        self.num_uo = num_uo
        self.data_input = inpt(process_name=process_name, num_unit_op=num_uo)
        self.list_uo: List[uo] = []
        self.flowsheet: fsht = fsht()


    #TODO: Let the InputForm class create the summary input form.
    def put_summary_input_form(self):
        self.data_input.put_summary_input_form(list_unit_ops=unit_operation.list_unit_ops)

    #TODO 


