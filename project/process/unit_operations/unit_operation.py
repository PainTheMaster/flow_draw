from __future__ import annotations
from abc import ABC, abstractmethod
import pandas as pd


#from flow_draw import definitions as defs
#from flow_draw import chemistry as chem
from flow_draw.data_io import flowsheet as fsht
from flow_draw.trait_def import trait_def as trdf



#TODO please delete this list when the automatic registration by __init_subclass__() is fully fully functional
# list_unit_ops =[
#     op_line_clearance,
#     op_N2_replace,
#     op_temp_control,
#     op_charging,
#     op_agitation,
#     op_settling,
#     op_aq_discharge,
#     op_distillation,
#     op_cip,
#     op_transfer,
#     op_filtration,
#     op_rinse,
#     op_reslurry,
#     op_drying,
#     op_tare,
#     op_prod_discharge,
#     op_placeholder
# ]
"""
This list covers the names of all unit operations.
"""


registry_uo_cls: dict[str, type[UnitOperation]] = {}
"""
This dictionary hols pairs of unit operation key (string) and unit operation class object (type[UnitOperation]).
The pairs are automatically registered by unit_operation.UniotOperation.__init_subclass_() everytime a new unit operation class becomes available (imported)
Therefore, this dictionaly represnts all the available unit operation at that moment.
"""

list_unit_ops: list[str] = []
"""
Simply, this is a list of key to unit operations. Like registry_uo_cls, this list is also automatically extended.
"""


class UnitOperation(ABC):
    """
    The base class of various unit operations.

    Attributes
    -------------
    flow_sheet: flow_draw.flow_output
        Flow sheet object bound to this process. This object handles output.
    
    uo_name: str
        The unit operation name, e.g., line clearance, charging, agitation, etc. Just a string.
    
    operation_seq: int
        The sequence number of the unit operation of interest.
    
    pre_comment: str
        An optional pre-comment for the unit operation.

    post_comment: str
        An optional post-comment for the unit operation.
    """
    def __init_subclass__(cls,*, uo_name: str|None = None, **kwargs):
        """
        Automatically triggered everytime each unit operation-derived class (not an instance!) is created.
        This method compells each unit operation class to register itself to registry_uo_cls[str, type[UnitOperation]] and .

        Parameters
        --------------
        op_key: str
            Keyword corresponding to each unit operation. This shoudl be defined in each unit operation module. 
        """
        super().__init_subclass__(**kwargs)
        if cls is UnitOperation:
            return
        if not uo_name:
            raise RuntimeError(f"Class {cls.__name__}: An empty op_key is not allowed.")
        if uo_name in registry_uo_cls:
            raise RuntimeError(f"Class {cls.__name__}: op_key \"{uo_name}\" already exists.")
        cls.uo_name:str = uo_name
        registry_uo_cls[uo_name] = cls
        list_unit_ops.append(uo_name)

    def __init__(self,
                 caller: type[trdf.UniversalTrait] =None,
                 flow_sheet:fsht.Flowsheet=None,
                 operation_seq: int=None,
                 num_subitems: int = None,
                 edit_comment:str=None):    
        """
        Set the necessary items in the instance variables.
        
        Parameters
        ------------
        caller: type[flow_draw.trait_def.trait_def.UniversalTrait]
            The caller object of the this method. Each derived class expect different traits (derived class of UniversalTrait). Normally, \"self\" when the function is called is expected. 
        
        flow_sheet: flow_draw.flow_output.Flowsheet
            Flowsheet object takes care of the output. The object should hold an OpenPyXL Workbook object. The class is responsible for formatting the output.

        operation_seq: int
            The sequence number of the operation. 

        Returns
        ------------
         None
        """
        self.caller: type[trdf.UniversalTrait] = caller
        self.flow_sheet: fsht.Flowsheet = flow_sheet
        #TODO: please remove the comment-out part below after a test.
        #self.unit_operation: str = unit_operation
        self.operation_seq: int = operation_seq
        self.num_subitems: int = num_subitems
        self.edit_comment:str = edit_comment
        self.pre_comment: str = ''
        self.post_comment: str = ''
    
    @abstractmethod
    def get_detail_header(self) -> list[str]:
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
    
    @abstractmethod
    def load_params_from_df(self, df: pd.DataFrame):
        """
        Loads necessary parameters from a DataFrame object.
        The header items must be in line with the definition in the UnitOperation-derived classes.
        The header items can be passed  by the get_detail_header().
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

    @abstractmethod
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



        
