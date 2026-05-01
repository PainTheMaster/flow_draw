import pandas as pd
import math
from flow_draw import definitions as defs

op_list = None

header_material = defs.hedr_io_mats_mat
header_main = defs.hedr_io_mats_main
header_mw = defs.hedr_io_mats_mw
header_density = defs.hedr_io_mats_dnsty
header_conc_assay = defs.hedr_io_mats_concasy

desig_star = defs.itm_io_mats_desig_star

# header_key = "Key"
# header_value = "Value"
# header_remark = "Remark"
# key_sm_name = "SM_name"
# key_sm_kg = "SM_QTY_kg"
# key_sm_mol = "SM_QTY_mol"

mol_main_sm = 1.0 #mol, placeholder
kg_main_sm = 10 #kg, placeholder

class Materials:
    def __init__(self,df_mats:pd.DataFrame):
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
            The data frame must have a header aligned with the class materials.Materials.
        """
        self.df_mats: pd.DataFrame= df_mats
        self.kg_main_mat = 0.0
        self.mol_main_mat = 0.0
        #TODO please find the core building block (main raw material) from df_mats. It is marked with "*".
        #self.df_sm = df_sm
        # self.sm_name = df_sm[df_sm[header_key]==key_sm_name][header_value].item()
        # self.sm_kg = df_sm[df_sm[header_key]==key_sm_kg][header_value].item()
        # self.sm_mol = self.sm_kg * 1000 / df_mats[df_mats[header_material]==self.sm_name][header_mw].item()
        df_extrd_main  = self.df_mats[self.df_mats[header_main]==desig_star]
        if len(df_extrd_main) == 0:
            raise RuntimeError(f"{self.__class__.__name__}: No core building block ({defs.hedr_io_mats_main}) is designated.")
        elif len(df_extrd_main) >= 2:
            raise RuntimeError(f"{self.__class__.__name__}: More than two (2) core building blocks ({defs.hedr_io_mats_main}) are designated.")
        else:
            ser_main_mat = df_extrd_main.iloc[0]
            
            self.kg_main_mat = float(ser_main_mat[defs.hedr_io_mats_kgmain])
            if math.isnan(self.kg_main_mat):
                raise ValueError(f"{self.__class__.__name__}: No weight (kg) is assigned to the main material \"{self.kg_main_mat}\".")
            
            temp_mw_main_mat = float(ser_main_mat[defs.hedr_io_mats_mw])
            if math.isnan(temp_mw_main_mat):
                raise ValueError(f"{self.__class__.__name__}: No molecular weight is assigned to the main material \"{temp_mw_main_mat}\".")

            temp_assay_main_mat = float(ser_main_mat[defs.hedr_io_mats_concasy])
            if math.isnan(temp_assay_main_mat):
                temp_assay_main_mat = 100.0
                raise UserWarning(f"{self.__class__.__name__}: The concentration or assay for the main material is empty or zero.",
                              "For this run, 100%% is assumed.")
            
            self.mol_main_mat = (self.kg_main_mat*1000)/temp_mw_main_mat*(temp_assay_main_mat/100)
            # self.mol_main_mat = self.kg_main_matser_main_mat[defs]

               

    #TODO 2026/04/29 Pleae test me. I was modified to be consistent with the new input form header style.
    def to_kilogram(self, material_name:str = None, equiv: float = None, vol_per_weight:float = None) -> float:
        """
        Converts metrics value in equiv or volume/weight of a given material to kilogram.
        This method depends on the DataFrame objects for both all the raw materials and the main starting material.
        As long as they are set to the Materials instance beforehand, this method works.

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
            raise ValueError(f"{self.__class__.__name__}.to_kilogram(): Dual input of equiv: {equiv} and vol_per_weight: {vol_per_weight} detected for the material \"{material_name}\". A value for only one of those shall be provided.")
        if not self.df_mats[defs.hedr_io_mats_mat].isin([material_name]).any():
            raise ValueError(f"{self.__class__.__name__}.to_kilogram(): A compound name \"{material_name}\" is not defined in the raw materials table.")
        conc_assay_this = self.df_mats[self.df_mats[defs.hedr_io_mats_mat]==material_name][defs.hedr_io_mats_concasy].item()
        if math.isnan(conc_assay_this) or conc_assay_this==0.0:
            conc_assay_this = 100.0
            raise UserWarning(f"{self.__class__.__name__}.to_kilogram(): The concentration or assay for the material \"{material_name}\" is empty or zero.",
                              "For this run, 100%% is assumed.")
        mw_this = self.df_mats[self.df_mats[defs.hedr_io_mats_mat]==material_name][defs.hedr_io_mats_mw].item()
        if math.isnan(mw_this):
            raise ValueError(f"{self.__class__.__name__}.to_kilogram(): No molecular weight is assigned to the material \"{material_name}\".")
        density_this = self.df_mats[self.df_mats[defs.hedr_io_mats_mat]==material_name][defs.hedr_io_mats_dnsty].item()
        if math.isnan(density_this):
            raise ValueError(f"{self.__class__.__name__}.to_kilogram(): No density is assigned to the material \"{material_name}\".")
        kg_this = 0.0
        if equiv is not None:
            mol_this = self.mol_main_mat * equiv
            kg_this = mol_this * mw_this / (conc_assay_this/100.0) / 1000.0
        elif vol_per_weight is not None:
            liq_volume_this = self.kg_main_mat * vol_per_weight #unit = L
            kg_this = liq_volume_this * density_this / (conc_assay_this/100.0)
        else:
            raise ValueError(f"{self.__class__.__name__}.to_kilogram(): Both equiv:float and vol_per_weight:folat arguments are \"None\". Either must be given.")
        
        return kg_this


