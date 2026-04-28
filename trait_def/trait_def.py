from abc import ABC, abstractmethod
import flow_draw.chemistry.chemistry

class UniversalTrait(ABC):
    pass

class GetChem(UniversalTrait):
    @abstractmethod
    def get_chem(self)-> flow_draw.chemistry.chemistry.Chemistry:
        pass