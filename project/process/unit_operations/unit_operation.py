import pandas as pd


from flow_draw import definitions as defs
from flow_draw import chemistry as chem
from flow_draw.flow_output import Flowsheet as fsht
from typing import List
import re


op_line_clearance = "line_clearance"
op_N2_replace = "N2_placement"
op_temp_control = "temp_control"
op_charging = "charging"
op_agitation = "agitation"
op_settling = "settling"
op_aq_discharge = "aq_discharge"
op_distillation = "distillation"
op_cip = "cip"
op_transfer = "transfer"
op_filtration = "filtration"
op_rinse = "rinse"
op_reslurry = "reslurry"
op_drying = "drying"
op_tare = "tare"
op_prod_discharge = "prod_discharge"
op_placeholder = "placeholder"

list_unit_ops =[
    op_line_clearance,
    op_N2_replace,
    op_temp_control,
    op_charging,
    op_agitation,
    op_settling,
    op_aq_discharge,
    op_distillation,
    op_cip,
    op_transfer,
    op_filtration,
    op_rinse,
    op_reslurry,
    op_drying,
    op_tare,
    op_prod_discharge,
    op_placeholder
]


class UnitOperation:
    """
    The base class of various unit operations.

    Attributes
    -------------
    chem_data: flow_draw.chemistry.Chemistry
        This instance contains the chemical information, e.g., molecular weight and density, and methods, e.g., volume to weight and vice versa, for the materials used in the process.

    flow_sheet: flow_draw.flow_output
        Flow sheet object bound to this process. This object handles output.
    
    unit_operation: str
        The unit operation name, e.g., line clearance, charging, agitation, etc. Just a string.
    
    operation_seq: int
        The sequence number of the unit operation of interest.
    
    pre_comment: str
        An optional pre-comment for the unit operation.

    post_comment: str
        An optional post-comment for the unit operation.
    """

    def __init__(self, chem_data:chem.Chemistry, flow_sheet:fsht.Flowsheet, unit_operation: str=None, operation_seq: int=None):
        """
        Set the necessary items in the instance variables.
        
        Parameters
        ------------
        chem_data: flow_draw.chemistry.Chemistry
            The chem_data object should include the data of chemical materials used in the process.
        
        flow_sheet: flow_draw.flow_output.Flowsheet
            Flowsheet object takes care of the output. The object should hold an OpenPyXL Workbook object. The class is responsible for formatting the output.
        
        unit_operation: str
            The name of the unit operation. This must be recognizable by this modue. These are defined in the modolue. 

        operation_seq: int
            The sequence number of the operation. 

        Returns
        ------------
            None
        """
        
        self.chem_data:chem.Chemistry = chem_data
        self.flow_sheet: fsht.Flowsheet = flow_sheet
        self.unit_operation: str = unit_operation
        self.operation_seq: int = operation_seq
        self.pre_comment: str = ''
        self.post_comment: str = ''


    # @classmethod 
    # def set_chemdata(cls, chem_data:chem.Chemistry):
    #     self.chem_data = chem_data


    # @classmethod 
    # def set_flowsheet(cls, flow_sheet:fsht.Flowsheet):
    #     cls.flow_sheet = flow_sheet
    

    # def put_comment(self,
    #                 comments: str,
    #                 list_col_time: List[str],
    #                 list_col_method: List[str],
    #                 list_col_content: List[str],
    #                 list_col_record: List[str],
    #                 list_col_operator: List[str],
    #                 list_col_witness: List[str]):
        
    #     cmt_brkdwn = re.split('[\n;]', comments)
    #     for single_cmt in cmt_brkdwn:
    #         list_col_time.append(None)
    #         list_col_method.append(None)
    #         list_col_content.append(single_cmt)
    #         list_col_record.append(None)
    #         list_col_operator.append(None)
    #         list_col_witness.append(None)
    
    def get_detail_header(self) -> List[str]:
        """
        Returns the header elements specific to the unit operation as a List[str].
        The UnitOperation class provides only skelton. Each derived class must override the method.

        Parameters
        --------------
        None

        Returns
        --------------
        unit_operation_specific_buffer:List[str]
            The header items for the data input form.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
        """
        raise NotImplementedError()
    
    def load_from_df(self, df: pd.DataFrame):
        """
        Loads necessary parameters from a DataFrame object. The header items must be recognizable by the UnitOperation object.
        The header items can be given by the get_detail_header().
        The UnitOperation class provides only skelton. Each derived class must override the methd.
        
        Parameters
        --------------
        df: pandas.DataFrame
            A wide table consists of header items recognizable by the UnitOperation object, and parameters.

        Returns
        --------------
        None
        """
        raise NotImplementedError()


    def output_unit_operation(self):
        """
        Outputs the items for the unit operation.
        Before calling this function, chem_data, flow_sheet, unit_operation, operation_seq must be set, and parameters must be loaded, normally by using load_from_df().
        The UnitOperation class provides only a skelton of the method. The method must be overloaded in each derived class.

        Parameters
        ------------
        None

        Returns
        ------------
        None    
        """
        raise NotImplementedError()



        
