import pandas as pd

from flow_draw import definitions as defs

op_list = None

header_material = defs.mats_header_material
header_mw = defs.mats_header_MW
header__density = defs.mats_header_density
header_conc_assay = defs.mats_header_conc_assay

header_key = "Key"
header_value = "Value"
header_remark = "Remark"
key_sm_name = "SM_name"
key_sm_kg = "SM_QTY_kg"
key_sm_mol = "SM_QTY_mol"

mol_main_sm = 1.0 #mol, placeholder
kg_main_sm = 10 #kg, placeholder

class Materials:
    def __init__(self, df_mats:pd.DataFrame):
        """
        Sets a pandas.DataFrame object containing data for all the chemical materials used in the process and quantity information of the starting material. 
        When all the necessary information is provided, the data sets are stored, the name and amount of the starting mterial (starting compound) in kg and mol are calculated and set to instance variables.
        
        Parameters
        -----------
        df_mats: pandas.DataFrame
            A DataFrame object for the materials (chemicals) used in the process.
            The table must hold:\n
                -Name
                -Molecular Weight
                -Density/specifc gravity (g/mL)
                -Concentration/assay (%)
                -Remark (opitonal)
            of the raw materials.\n
            The data frame must have a header aligned with the class chemistry.Chemistry.
        
        df_sm: pandas.DataFrame
            A DataFrame object retaining information on the quantity of the starting material. It shall have:\n
                -Name
                -Quantity in kg
                -Remark (optional)
            of the starting material.\n
        """
        self.df_mats: pd.DataFrame= df_mats
        #TODO please find the core building block (main raw material) from df_chem. It is marked with "*".
        #self.df_sm = df_sm
        # self.sm_name = df_sm[df_sm[header_key]==key_sm_name][header_value].item()
        # self.sm_kg = df_sm[df_sm[header_key]==key_sm_kg][header_value].item()
        # self.sm_mol = self.sm_kg * 1000 / df_chem[df_chem[header_material]==self.sm_name][header_mw].item()
               

    #TODO 2026/04/29 Pleae test me. I was modified to be consistent with the new input form header style.
    def to_kilogram(self, material_name:str = None, equiv: float = None, vol_per_weight:float = None) -> float:
        """
        Converts metrics value in equiv or volume/weight of a given material to kilogram.
        This method depends on the DataFrame objects for both all the raw materials and the main starting material.
        As long as they are set to the Chemistry instance beforehand, this method works.

        Parameters
        -------------
        material:str
            The name of a material whose input amount in kg is desired.
        
        equiv: float
            Molar equivalent of  \"material\" to the main starting compund. Put either this or \"vol_per_weight\".
        
        vol_per_weight:int
            Volue (liter) of \"material\" vs a kilogram of the main starting compound. Put either this or \"equiv\".
        
        Returns
        -------
            weight: float
            Amount of \"material\" in kg.

        """
        if not (equiv is None or vol_per_weight is None):
            raise ValueError(f"{self.__class__.__name__}.to_kilogram(): Dual input of equiv: {equiv} and vol_per_weight: {vol_per_weight}. A value for only one of those shall be provided.")
        if not self.df_mats[defs.mats_header_material].isin([material_name]).any():
            raise ValueError(f"{self.__class__.__name__}.to_kilogram(): A compound name \"{material_name}\" is not defined in the raw materials table.")
        conc_assay = self.df_mats[self.df_mats[defs.mats_header_material]==material_name][defs.mats_header_conc_assay].item()
        if not conc_assay or conc_assay==0.0:
            raise UserWarning(f"{self.__class__.__name__}.to_kilogram(): The concentration or assay for the material \"{material_name}\" is empty or zero.",
                              "For this run, 100%% is assumed.")
            conc_assay = 100.0
        mw = self.df_mats[self.df_mats[defs.mats_header_material]==material_name][defs.mats_header_MW].item()
        density = self.df_mats[self.df_mats[defs.mats_header_material]==material_name][defs.mats_header_density].item()
        weight = 0.0
        if equiv is not None:
            mol = self.sm_mol * equiv
            weight = mol * mw / (conc_assay/100.0) / 1000.0
        elif vol_per_weight is not None:
            liq_volume = self.sm_kg * vol_per_weight #unit = L
            weight = liq_volume * density / (conc_assay/100.0)
        else:
            raise ValueError(f"{self.__class__.__name__}.to_kilogram(): Both equiv:float and vol_per_weight:folat arguments are \"None\". Either must be given.")
        
        return weight


