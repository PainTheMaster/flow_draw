from typing import List
from flow_draw.project.process.unit_operations.unit_operation import UnitOperation as uo

class Process:
    """
    The Process is for a process, which consists of many unit operations. The class holds a name, an instance of InputForm class, a sries of UnitOperation(s).

    Attributes
    -----------
    name: str
        Simply the name of the process. Note that this will be passed to the InputForm class to create an instance. Thie will be eventually included in the file name for the input form.

    list_uo: List[flow_draw.project.process.unit_operations.UnitOperation]
        A list of unit operations that constitute the process. The sequence in this list is identical to that on the flowsheet in the real world.

    """
    def __init__(self, name:str):
        self.name = name
        self.list_uo: List[uo] = []