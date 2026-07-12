#from typing import List
import pandas as pd
import flow_draw.definitions as defs
# from flow_draw.batch.process.unit_operations import unit_operation
#from flow_draw.batch.process.unit_operations.unit_operation import UnitOperation as unitop
import flow_draw.batch.process.unit_operations.unit_operation as uo
import flow_draw.batch.process.unit_operations.uo_charging as chgng
import flow_draw.batch.process.unit_operations.uo_sampling as smplng
import flow_draw.batch.process.unit_operations.uo_cip as cip
import flow_draw.batch.process.unit_operations.uo_agitation as agit
import flow_draw.batch.process.unit_operations.uo_placeholder as plchldr

from flow_draw.data_io import process_io as proc_io
from flow_draw.data_io import flowsheet as fsht
from flow_draw.materials.materials import Materials as mats

from flow_draw.trait_def.trait_def import GetMats as GetMats

from flow_draw.data_io import json_io
from flow_draw.data_io.json_io import JsonEntity, Array, Objason, Primitive

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
    list_uo: List[flow_draw.batch.process.unit_operations.UnitOperation]
        A list of unit operations that constitute the process. The sequence in this list is identical to that on the flowsheet in the real world.
    flowsheet: flow_draw.flow_output.Flowsheet
        A Flowsheet object that manages the flowsheet output.
    """
    def __init__(self, batch_name:str = None, process_name:str=None, num_uo: int = None, comment: str = None):
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
        self.batch_name:str = batch_name
        self.process_name:str = process_name
        self.num_uo:int = None
        if(num_uo is not None):
            self.num_uo = num_uo
        else:
            self.num_uo = 1
        self.comment: str = comment
        if not(batch_name is None or process_name is None):
            self.data_input: proc_io.ProcessIO = proc_io.ProcessIO(batch_name=batch_name, process_name=process_name, num_unit_op=num_uo)
            """
            Please note that self.data_input has only the information provided as the arguments above (batch name, process name, and number of unit operations). The object doesn't hold even the sequnce of unit operations.
            Hence the object is like a collection of placeholders for unit operations. A specific sequence is knwon when self.load_uo_summary() is called. The details for each unit operation is loaded when load_unitop_detail() is called.
            """
        
        #self.str_json_proc: str = self.data_input.json_uo(caller=self, )
        self.mats_data: mats = None #mats_data is stored when load_materials_data() is called.
        self.seq_uo: list[uo.UnitOperation] = []
        """Sequene of the constituting unit operations. This will be populated when self.load_uo_summary() is called."""
        self.flowsheet: fsht.Flowsheet = fsht.Flowsheet()

        


    #TODO: Let the InputForm class create the summary input form.
    def generate_summary_mats_input_form(self):
        """
        This function generates forms for <b>process summary</b> and <b>material data</b> by calling ProcessIO.generate_proc_summary_form() and ProcessIO.generate_mats_form(). The forms are saved as sheets in the Excel file.
        
        Parameters
        ------------
        None

        Returns
        ------------
        None
            Returns nothing. The results are stored in self.data_input.
        """
        self.data_input.generate_proc_summary_form(list_unit_ops=uo.list_unit_ops)
        #At the time of process summary creation, the material information should be available. Plus, it is neceesary before loading the detail.
        self.data_input.generate_mats_form()
        #self.data_input.save_form()


    def generate_mats_form_for_ai(self):
        """
        The function invokes material form generation. This is intended for work with AI. 
        In that case, process summary form can be skipped, whereas material form is needed.
        
        Params
        -----------
        None

        Returns
        -----------
        None
        
        """
        self.data_input.generate_mats_form()
        #self.data_input.save_form()




    def load_uo_summary(self):
        """
        Loads summary data from a process summary DataFrame and creates a series of (partially filled) UnitOperation instances by interpreting a given process summary DataFrame. 
        After the run, the self.list_uo will hold a series of unit operation instances each of which knows the category of the unit operation (the type(sub-class) itself), sequenc number, number of subitems, and edit comment.
        
        Parameters
        -----------
        None

        Returns
        ----------
        None
        """
        df_summary = self.data_input.load_process_summary()
        uo_reg = uo.registry_uo_cls
        for _, row in df_summary.iterrows():
            seq = int(row[defs.hedr_io_sumry_seq])
            uo_title = str(row[defs.hedr_io_summary_uo])
            num_subitems = int(row[defs.hedr_io_sumry_num_subitms])
            edit_comment = str(row[defs.hedr_io_sumry_edt_cmnt])
            if not uo_title in uo_reg:
                raise RuntimeError(f"{self.__class__.__name__}: Unit operation name \"{uo_title}\" not in the registry.")
            new_uo_inst = uo_reg[uo_title](caller=self,
                                        flowsheet=self.flowsheet,
                                        operation_seq=seq,
                                        num_subitems=num_subitems,
                                        edit_comment=edit_comment)
            self.seq_uo.append(new_uo_inst)

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
        

    def load_materials_data(self):
        """
        Reads the input Excel form (material worksheet) and loads data from it. This method is intended to be called by a method belonging to the class Batch.
        The acquired data is stored at self.mats_data. Hence, the method returns no value.

        Parameters
        ------------
        None

        Returns
        ------------
        None
        """
        self.mats_data = self.data_input.load_mats()

    #TODO: Create the process detail input form, for each unit operation in teh list_uo, get the uo-specific header and feed it to ProcessIO.generate_proc_detail_form()

    #TODO: Load the process detail\
    def load_unitop_detail(self):
        """
        Expected to be triggered by the Batch class, this function loads unit operation details from self.data_input.
        Then, passes the details to the each unit operation objec that constitutes the process.

        Parameters
        -----------
        None

        Returns
        -----------
        None
        """
        
        df_uo_details: list[pd.DataFrame] = self.data_input.load_process_details()
        for i in range(len(self.seq_uo)):
            temp_detail = df_uo_details[i]
            if self.seq_uo[i].uo_tag == (temp_detail)[defs.hedr_cmn_io_dtil_uo].iloc[0]:
                self.seq_uo[i].load_params_from_df(temp_detail)
            else:
                raise RuntimeError(f"{self.__class__.__name__}: Seq Nr-{self.seq_uo[i].operation_seq} Unit operation name mismatch.",
                                   f"summary table: {self.seq_uo[i].uo_tag}",
                                   f"detail table: {temp_detail[defs.hedr_cmn_io_dtil_uo].iloc[0]}")
                

    #TODO Let's implement self.prep_uo() to create a list of unit operations to be ready to receive detail data.


    

    def ai_load_process_details(self):
        self.load_materials_data()
        #lit_uo = list(unitop.registry_uo_cls.values())
        list_uo: list[type[uo.UnitOperation]] = [chgng.Charging, agit.Agitation, cip.CIP, smplng.Sampling]
        self.data_input.ai_load_process_details()

        



    def get_mats(self) -> mats:
        return self.mats_data



        
