import pandas as pd

from flow_draw import definitions as defs

op_list = None

header_material = "Material"
header_mw = "MW"
header__density = "Density"
header_conc = "Conc(%)"

header_key = "Key"
header_value = "Value"
header_remark = "Remark"
key_sm_name = "SM_name"
key_sm_kg = "SM_QTY_kg"
key_sm_mol = "SM_QTY_mol"

mol_main_sm = 1.0 #mol, placeholder
kg_main_sm = 10 #kg, placeholder

class Chemistry:
    def __init__(self, df_chem:pd.DataFrame, df_sm:pd.DataFrame):
        """
        Sets a pandas.DataFrame object containing data for all the chemical materials used in the process and quantity information of the starting material. 
        When all the necessary information is provided, the data sets are stored, the name and amount of the starting mterial (starting compound) in kg and mol are calculated and set to instance variables.
        
        Parameters
        -----------
        df_chem: pandas.DataFrame
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
        self.df_chem: pd.DataFrame= df_chem
        self.df_sm = df_sm
        self.sm_name = df_sm[df_sm[header_key]==key_sm_name][header_value].item()
        self.sm_kg = df_sm[df_sm[header_key]==key_sm_kg][header_value].item()
        self.sm_mol = self.sm_kg * 1000 / df_chem[df_chem[header_material]==self.sm_name][header_mw].item()   

    def to_kilogram(self, material:str = None, equiv: float = None, vol_per_weight:float = None) -> float:
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
            raise ValueError(f"chemistry.Chemistry.to_kilogram(): Dual input of equiv: {equiv} and vol_per_weight: {vol_per_weight}. A value for only one of those shall be provided.")
        if not self.df_chem[header_material].isin([material]).any():
            raise ValueError(f"chemistry.Chemistry.to_kilogram(): A compound name \"{material}\" is not defined in the raw materials table.")
        mw = self.df_chem[self.df_chem[header_material]==material][header_mw].item()
        density = self.df_chem[self.df_chem[header_material]==material][header__density].item()
        conc = self.df_chem[self.df_chem[header_material]==material][header_conc].item()
        weight = 0.0
        if equiv is not None:
            mol = self.sm_mol * equiv
            weight = mol * mw * (conc/100) / 1000
        elif vol_per_weight is not None:
            liq_volume = self.sm_kg * vol_per_weight #unit = L
            weight = liq_volume * density
        else:
            raise ValueError("chemistry.Chemistry.to_kilogram(): Both equiv:float and vol_per_weight:folat arguments are \"None\". Either must be given.")
        
        return weight


