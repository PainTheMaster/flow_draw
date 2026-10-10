from abc import ABC, abstractmethod
import flow_draw.materials.materials
import flow_draw.batch.process.unit_operations.uo_charging as chgng

class UniversalTrait(ABC):
    pass

class GetMats(UniversalTrait):
    """
    GetMats is an abstract class having get_mats() function returning flow_draw.materials.materials.Materials.
    By calling the object, the caller can acquire the information of materials used in the process.
    """
    @abstractmethod
    def get_mats(self)-> flow_draw.materials.materials.Materials:
        """
        Expected to return an instance of Materials, retaining information of materials used in the process.
        As materials are process-specific, an instance of Process and that of Materials are in one-on-one relationship.
        Process class shall have this trait.
        
        Parameters
        ----------
        None

        Returns
        ----------
        materials: flow_draw.materials.materials.Materials
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

class GetInputs(UniversalTrait):
    """
    GetInputs is an abstract class having get_inputs() function returning the input values for the process.
    By calling the object, the caller can acquire the input values used in the process.
    """
    @abstractmethod
    def get_inputs(self, id_input: int = None) -> chgng.Input:
        """
        Expected to return an instance of chgng.Input representing the input values for the process.

        Parameters
        ----------
        id_input: int, optional
            The identifier for the specific input to retrieve. If None, the default input is returned.

        Returns
        ----------
        inputs: chgng.Input
            This shall be an instance of chgng.Input containing all the necessary input values for the process.
        """
        pass


    @abstractmethod
    def get_depended(self):
        pass