from abc import ABC, abstractmethod
import pandas as pd
# import flow_draw.materials.materials as mats
from typing import Any
# if TYPE_CHECKING:
#     import flow_draw.batch.process.process as proc
#     import flow_draw.batch.process.unit_operations.material_input as matinput
from flow_draw.data_io.json_io import Objason
# from flow_draw.trait_def.trait_def import AbstInput


class MaterialsTrait(ABC):
    @abstractmethod
    def get_name_sm(self)->str:
        pass

    @abstractmethod
    def get_gross_kg_sm(self)->float:
        pass

    @abstractmethod
    def get_kg_net_sm(self)->float:
        pass

    @abstractmethod
    def get_mol_sm(self) -> float:
        pass

    @abstractmethod
    def get_name_tgt(self) -> str:
        pass

    @abstractmethod
    def get_kg_net_tgt_ideal(self) -> float:
        pass

    @abstractmethod    
    def get_list_mats(self) -> list[str]:
        pass

    @abstractmethod
    def get_mw(self, material_name:str) -> float|None:
        pass

    @abstractmethod
    def get_density(self, material_name:str) -> float|None:
        pass

    @abstractmethod
    def get_conc_assay(self, material_name:str) -> float|None:
        pass


    @staticmethod
    @abstractmethod
    def generate_mats_df()->pd.DataFrame:
        pass

    @staticmethod    
    @abstractmethod    
    def add_to_mats_df(mats_df:pd.DataFrame = None,
                       material:str = None,
                       main_star:bool = False,
                       mw:float = None,
                       density:float = None,
                       conc_assay:float=None,
                       kg_main:float=None,
                       remark:str=None)->pd.DataFrame:
        pass
        

class UniversalTrait(ABC):
    pass


class GetMats(UniversalTrait):
    """
    GetMats is an abstract class having get_mats() function returning flow_draw.materials.materials.Materials.
    By calling the object, the caller can acquire the information of materials used in the process.
    """
    @abstractmethod
    def get_mats(self)-> type[MaterialsTrait]:
        """
        Expected to return an instance of Materials, retaining information of materials used in the process.
        As materials are process-specific, an instance of Process and that of Materials are in one-on-one relationship.
        Process class shall have this trait.
        
        Parameters
        ----------
        None

        Returns
        ----------
        materials: type[MaterialsTrait]
            This shall have all the necessary information of the materials used in the process, including designation of the core building block and its quantity.
        """
        pass

class GetProcName(UniversalTrait):
    """
    GetProcName is an abstract class having get_proc_name() function returning the name of the process.
    By calling the object, the caller can acquire the name of the process.
    """
    @abstractmethod
    def get_proc_name(self)-> str:
        """
        Expected to return a string representing the name of the process.

        Parameters
        ----------
        None

        Returns
        ----------
        proc_name: str
            This shall be a string representing the name of the process.
        """
        pass



class InputTrait(ABC):
    @abstractmethod
    def load_params_from_series(self, ser: pd.Series):
        pass

    @staticmethod
    @abstractmethod
    def get_json_schema(caller: GetMats=None)-> Objason:
        pass

    @abstractmethod
    def load_from_json_dict(self, json_dict: dict[str, Any]):
        pass

    @abstractmethod
    def mark_as_tgt(self):
        pass

    @abstractmethod
    def calc_qty(self)->bool:
        pass

    @abstractmethod
    def get_basis_name(self)->str|None:
        pass

    @abstractmethod
    def put_material(self,
                    time=None,
                    method=None,
                    record=None,
                    operator=None,
                    witness=None):
        pass

    @abstractmethod
    def instruct_qty_range(self,
                time: str =None,
                method: str=None,
                record: str=None,
                operator: str=None,
                witness: str=None,
                line_mat:int=None)->int:
        pass

    @abstractmethod
    def link_inputs(self):
        pass




class GetInputs(UniversalTrait):
    """
    GetInputs is an abstract class having get_inputs() function returning the input values for the process.
    By calling the object, the caller can acquire the input values used in the process.
    """
    @abstractmethod
    def get_input(self, id_input: int = None) -> type[InputTrait]:
        """
        Expected to return an instance of InputTrait representing the input values for the process.

        Parameters
        ----------
        id_input: int, optional
            The identifier for the specific input to retrieve. If None, the default input is returned.

        Returns
        ----------
        inputs: InputTrait
            This shall be an instance of InputTrait containing all the necessary input values for the process.
        """
        pass


    # @abstractmethod
    # def get_dependencies(self) -> list[proc.Dependency]:
    #     pass

    @abstractmethod
    def get_id_input_sm(self) -> list[int]:
        """
        Expected to return a list of IDs for the starting material inputs in the process.

        Parameters
        ----------
        None

        Returns
        ----------
        list_id_input_sm: list[int]
            This shall be a list of integers representing the IDs of the starting material inputs.
        """
        pass

    @abstractmethod
    def get_assumed_yield_pct(self) -> float:
        """
        Expected to return the assumed yield for the process.

        Parameters
        ----------
        None

        Returns
        ----------
        assumed_yield: float
            This shall be a float representing the assumed yield of the process.
        """
        pass

    @abstractmethod
    def get_tgt_stoichiometry(self) -> float:
        """
        Expected to return the target stoichiometry for the process.

        Parameters
        ----------
        None

        Returns
        ----------
        tgt_stoichiometry: float
            This shall be a float representing the target stoichiometry of the process.
        """
        pass
