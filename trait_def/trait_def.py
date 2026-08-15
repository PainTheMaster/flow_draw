from abc import ABC, abstractmethod
import flow_draw.materials.materials

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