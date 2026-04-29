#from typing import List
import pandas as pd
import flow_draw.definitions as defs
from flow_draw.project.process.unit_operations import unit_operation
from flow_draw.project.process.unit_operations.unit_operation import UnitOperation as unitop
from flow_draw.data_io.process_io import ProcessIO as proc_io
from flow_draw.data_io.flowsheet import Flowsheet as fsht
from flow_draw.materials.materials import Materials as mats

from flow_draw.trait_def.trait_def import GetMats as GetMats

class Process(GetMats):
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
        self.mats_data: mats = None #TODO please put the right Materials object
        self.data_input = proc_io(process_name=process_name, num_unit_op=num_uo)
        self.list_uo: list[unitop] = []
        self.flowsheet: fsht = fsht()

        


    #TODO: Let the InputForm class create the summary input form.
    def put_summary_input_form(self):
        """
        Triggered by a method of the class Project, calls 
        """
        self.data_input.generate_proc_summary_form(list_unit_ops=unit_operation.list_unit_ops)




    #TODO: Please implement me! Load the process summary
    def load_uo_summary(self):
        """
        Loads summary data from a process summary DataFrame and creates a series of (partially filled) UnitOperation instances by interpreting a given process summary DataFrame. 
        After the run, the self.list_uo will hold a series of unit operation instances each of which knwos the category of the unit operation (the type(sub-class) itself), sequenc number, number of subitems, and edit comment.
        
        Parameters
        -----------
        None

        Returns
        ----------
        None
        """
        df_summary = self.data_input.load_process_summary()
        uo_reg = unit_operation.registry_uo_cls
        for _, row in df_summary.iterrows():
            seq = int(row[defs.header_summary_sequence])
            uo_title = str(row[defs.header_summary_uo])
            num_subitems = int(row[defs.header_summary_num_subitems])
            edit_comment = str(row[defs.header_summary_edit_comment])
        if not uo_title in uo_reg:
            raise RuntimeError(f"{self.__class__.__name__}: Unit operation name \"{uo_title}\" not in the registry.")
        
        new_uo_inst = uo_reg[uo_title](self, self.flowsheet, seq, num_subitems=num_subitems, edit_comment=edit_comment)
        self.list_uo.append(new_uo_inst)

    # def __prep_uo(self, df_summary: pd.DataFrame):
    #     """
    #     Creates a series of (partially filled) UnitOperation instances by interpreting a given process summary DataFrame.
    #     After the run, the self.list_uo will hold a series of unit operation instances each of which knwos the category of the unit operation (the type(sub-class) itself), sequenc number, number of subitems, and edit comment.
        
    #     Parameters
    #     -----------
    #     df_summary: pandas.DataFrame
    #         A DataFrame object containing a seiries of unit operations with sequence number, number of subitems, and edit comment for each. The header items shall be consistent with the definition in the definitions module.
        
    #     Returns:
    #         None
    #     """
    #     uo_reg = unit_operation.registry_uo_cls
    #     for _, row in df_summary.iterrows():
    #         seq = int(row[defs.header_summary_sequence])
    #         uo_title = str(row[defs.header_summary_uo])
    #         num_subitems = int(row[defs.header_summary_num_subitems])
    #         edit_comment = str(row[defs.header_summary_edit_comment])
    #     if not uo_title in uo_reg:
    #         raise RuntimeError(f"{self.__class__.__name__}: Unit operation name \"{uo_title}\" not in the registry.")
        
    #     new_uo_inst = uo_reg[uo_title](self, self.flowsheet, seq, num_subitems=num_subitems, edit_comment=edit_comment)
    #     self.list_uo.append(new_uo_inst)
        


    #TODO: Create the process detail input form

    #TODO Load the process detail\
    def load_unitop_detail(self):
        """
        Expected to be triggered by the Project class, this function loads unit operation details from self.data_input.
        Then, passes the details to the each unit operation objec that constitutes the process.

        Parameters
        -----------
        None

        Returns
        -----------
        None
        """
        df_uo_details: list[pd.DataFrame] = self.data_input.load_process_details()
        for i in range(len(self.list_uo)):
            temp_detail = df_uo_details[i]
            if self.list_uo[i].uo_name == (temp_detail)[defs.header_detail_uo].iloc[0]:
                self.list_uo[i].load_params_from_df(temp_detail)
            else:
                raise RuntimeError(f"{self.__class__.__name__}: Seq Nr-{self.list_uo[i].operation_seq} Unit operation name mismatch.",
                                   f"summary table: {self.list_uo[i].uo_name}",
                                   f"detail table: {temp_detail[defs.header_detail_uo].iloc[0]}")
                

    #TODO Let's implement self.prep_uo() to create a list of unit operations to be ready to receive detail data.


    def get_mats(self) -> mats:
        return self.mats_data

