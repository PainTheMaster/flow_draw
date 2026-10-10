import pandas as pd
import math
import warnings
from flow_draw import definitions as defs


op_list = None

header_material = defs.hedr_io_mats_mat
header_sm_tgt = defs.hedr_io_mats_sm_tgt
header_tgt = defs.hedr_io_mats_sm_tgt
header_mw = defs.hedr_io_mats_mw
header_density = defs.hedr_io_mats_dnsty
header_assay_conc = defs.hedr_io_mats_concasy

desig_sm = defs.itm_io_mats_sm
desig_tgt = defs.itm_io_mats_tgt

# header_key = "Key"
# header_value = "Value"
# header_remark = "Remark"
# key_sm_name = "SM_name"
# key_sm_kg = "SM_QTY_kg"
# key_sm_mol = "SM_QTY_mol"

mol_main_sm = 1.0 #mol, placeholder
kg_main_sm = 10 #kg, placeholder

class Materials:
    def __init__(self,df_mats:pd.DataFrame=None):
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
        self.name_sm:str = None
        """The value is picked-up on the course of the process in __load_df_mats()"""
        self.gross_kg_sm:float = None
        self.net_kg_sm:float = None
        self.assay_sm:float = None
        self.mol_sm:float = None

        self.name_tgt:str = None
        self.kg_net_tgt_ideal:float = None
        
        if df_mats is not None:
            self.__load_df_mats()
        

    def __load_df_mats(self):
        """
        Extract the core building block, from the given DataFrame and sets its quantity information in self.kg_main_mat and self.mol_main_mat.
        """
        #Extraction of the starting material
        df_extrd_sm  = self.df_mats[self.df_mats[header_sm_tgt]==desig_sm] 
        if df_extrd_sm.empty:
            raise RuntimeError(f'{self.__class__.__name__}: No starting material is designated in the colum "{defs.hedr_io_mats_sm_tgt}".')
        elif len(df_extrd_sm) > 1:
            raise RuntimeError(f'{self.__class__.__name__}: More than one starting materials are designated in the colum "{defs.hedr_io_mats_sm_tgt}".')
        else:
            ser_sm = df_extrd_sm.iloc[0]

            temp_name_sm = ser_sm[defs.hedr_io_mats_mat]
            if pd.notna(temp_name_sm) and str(temp_name_sm).strip() != "":
                self.name_sm = str(temp_name_sm)
            else:
                raise ValueError(f'{self.__class__.__name__}: No name is assigned to the starting material.')
            temp_gross_kg_sm = ser_sm[defs.hedr_io_mats_kg_sm]
            if pd.isna(temp_gross_kg_sm):
                raise ValueError(f'{self.__class__.__name__}: No weight (kg) is assigned to the starting material "{self.name_sm}".')
            self.gross_kg_sm = float(temp_gross_kg_sm)
            
            temp_mw_sm = ser_sm[defs.hedr_io_mats_mw]
            if pd.isna(temp_mw_sm):
                raise ValueError(f'{self.__class__.__name__}: No molecular weight is assigned to the starting material "{self.name_sm}".')
            temp_mw_sm = float(temp_mw_sm)

            temp_assay_sm = ser_sm[defs.hedr_io_mats_concasy]
            if pd.isna(temp_assay_sm):
                temp_assay_sm = 100.0
                warnings.warn(f"{self.__class__.__name__}: The concentration or assay for the starting material is empty or zero. For this run, 100%% is assumed.", UserWarning)
            elif float(temp_assay_sm) == 0.0:
                raise ValueError(f'{self.__class__.__name__}: The concentration or assay for the starting material "{self.name_sm}" is zero.')
            self.assay_sm = float(temp_assay_sm)
            self.net_kg_sm = self.gross_kg_sm * (temp_assay_sm / 100)
            self.mol_sm = (self.net_kg_sm*1000)/temp_mw_sm


        df_extrd_tgt  = self.df_mats[self.df_mats[header_sm_tgt]==desig_tgt] 
        if df_extrd_tgt.empty:
            raise RuntimeError(f'{self.__class__.__name__}: No target material is designated in the colum "{defs.hedr_io_mats_sm_tgt}".')
        elif len(df_extrd_tgt) > 1:
            raise RuntimeError(f'{self.__class__.__name__}: More than one target materials are designated in the colum "{defs.hedr_io_mats_sm_tgt}".')
        else:
            ser_tgt = df_extrd_tgt.iloc[0]
            temp_name_tgt = ser_tgt[defs.hedr_io_mats_mat]
            if pd.notna(temp_name_tgt) and str(temp_name_tgt).strip() != "":
                self.name_tgt = str(temp_name_tgt)
            else:
                raise ValueError(f'{self.__class__.__name__}: No name is assigned to the target material.')

            temp_mw_tgt = ser_tgt[defs.hedr_io_mats_mw]
            if pd.isna(temp_mw_tgt):
                raise ValueError(f'{self.__class__.__name__}: No molecular weight is assigned to the target material "{self.name_tgt}".')
            temp_mw_tgt = float(temp_mw_tgt)

            self.kg_net_tgt_ideal = self.mol_sm * temp_mw_tgt / 1000


    def get_name_sm(self)->str:
        return self.name_sm

    def get_mol_sm(self) -> float:
        return self.mol_sm

    def get_name_tgt(self) -> str:
        return self.name_tgt

    def get_kg_net_tgt_ideal(self) -> float:
        return self.kg_net_tgt_ideal
               
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
        if equiv is not None and vol_per_weight is not None:
            raise ValueError(f"{self.__class__.__name__}.to_kilogram(): Both equiv: {equiv} and vol_per_weight: {vol_per_weight} are provided for the material \"{material_name}\". Only one of them should be provided.")
        
        if not self.df_mats[defs.hedr_io_mats_mat].isin([material_name]).any():
            raise ValueError(f"{self.__class__.__name__}.to_kilogram(): A compound name \"{material_name}\" is not defined in the raw materials table.")
        conc_assay_this = self.df_mats[self.df_mats[defs.hedr_io_mats_mat]==material_name][defs.hedr_io_mats_concasy].item()
        # if math.isnan(conc_assay_this) or conc_assay_this==0.0:
        if pd.isna(conc_assay_this) or conc_assay_this==0.0:
            conc_assay_this = 100.0
            warnings.warn(f"{self.__class__.__name__}.to_kilogram(): The concentration or assay for the material \"{material_name}\" is empty or zero.",
                          "For this run, 100%% is assumed.", UserWarning)
        
        mw_this = self.df_mats[self.df_mats[defs.hedr_io_mats_mat]==material_name][defs.hedr_io_mats_mw].item()
        # if math.isnan(mw_this):
        if equiv is not None and pd.isna(mw_this):
            raise ValueError(f"{self.__class__.__name__}.to_kilogram(): No molecular weight is assigned to the material \"{material_name}\".")
        density_this = self.df_mats[self.df_mats[defs.hedr_io_mats_mat]==material_name][defs.hedr_io_mats_dnsty].item()
        # if math.isnan(density_this):
        if vol_per_weight is not None and pd.isna(density_this):
            raise ValueError(f"{self.__class__.__name__}.to_kilogram(): No density is assigned to the material \"{material_name}\".")
        kg_this = 0.0
        if equiv is not None:
            mol_this = self.mol_sm * equiv
            kg_this = mol_this * mw_this / (conc_assay_this/100.0) / 1000.0
        elif vol_per_weight is not None:
            #liq_volume_this = self.gross_kg_main_mat * vol_per_weight #unit = L
            liq_volume_this = self.to_litre(vol_per_weight=vol_per_weight)
            kg_this = liq_volume_this * density_this / (conc_assay_this/100.0)
        else:
            raise ValueError(f"{self.__class__.__name__}.to_kilogram(): Both equiv:float and vol_per_weight:folat arguments are \"None\". Either must be given.")
        
        return kg_this

    def to_litre(self, vol_per_weight:float = None) -> float:
        litre:float = None
        if self.gross_kg_sm is None:
            raise ValueError(f"{self.__class__.__name__}.to_litre(): the weigt (kg) of the main material has not been assigned.")
        elif vol_per_weight is None:
            raise ValueError(f"{self.__class__.__name__}.to_litre(): the argument vol_per_weight:float is not put.")
        else:
            litre = self.gross_kg_sm * (self.assay_sm/100.0) * vol_per_weight
        return litre
    
    def get_list_mats(self) -> list[str]:
        mats_list = self.df_mats[header_material].to_list()
        return mats_list

    def get_mw(self, material_name:str) -> float|None:
        hits = self.df_mats.loc[self.df_mats[defs.hedr_io_mats_mat]==material_name, defs.hedr_io_mats_mw]
        if len(hits) != 1:
            raise ValueError(f'{self.__class__.__name__}.get_mw(): "{material_name}" matched {len(hits)} rows (expected 1).')
        mw_this = hits.item()
        if pd.isna(mw_this):
            return None
        return float(mw_this)

    def get_density(self, material_name:str) -> float|None:
        hits = self.df_mats.loc[self.df_mats[defs.hedr_io_mats_mat]==material_name, defs.hedr_io_mats_dnsty]
        if len(hits) != 1:
            raise ValueError(f'{self.__class__.__name__}.get_density(): "{material_name}" matched {len(hits)} rows (expected 1).')
        density_this = hits.item()
        if pd.isna(density_this):
            return None
        return float(density_this)

    def get_assay_conc(self, material_name:str) -> float|None:
        hits = self.df_mats.loc[self.df_mats[defs.hedr_io_mats_mat]==material_name, defs.hedr_io_mats_concasy]
        if len(hits) != 1:
            raise ValueError(f'{self.__class__.__name__}.get_assay_conc(): "{material_name}" matched {len(hits)} rows (expected 1).')
        conc_assay_this = hits.item()
        if pd.isna(conc_assay_this):
            return None
        return float(conc_assay_this)



    @classmethod
    def generate_mats_df(cls)->pd.DataFrame:
        """
        DataFrame generator for test. The header items of the new df is as follows.<br>
            defs.hedr_io_mats_mat<br>
            defs.hedr_io_mats_main<br>
            defs.hedr_io_mats_mw<br>
            defs.hedr_io_mats_dnsty<br>
            defs.hedr_io_mats_concasy<br>
            defs.hedr_io_mats_kgmain<br>
            defs.hedr_io_mats_remark<br>
        """
        hedr:list[str] = [defs.hedr_io_mats_mat,
                          defs.hedr_io_mats_sm_tgt,
                          defs.hedr_io_mats_mw,
                          defs.hedr_io_mats_dnsty,
                          defs.hedr_io_mats_concasy,
                          defs.hedr_io_mats_kg_sm,
                          defs.hedr_io_mats_remark]
        empty_df: pd.DataFrame = pd.DataFrame(columns=hedr)
        return empty_df
    

    @classmethod
    def add_to_mats_df(cls,
                       mats_df:pd.DataFrame = None,
                       material:str = None,
                       main_star:bool = False,
                       mw:float = None,
                       density:float = None,
                       conc_assay:float=None,
                       kg_main:float=None,
                       remark:str=None)->pd.DataFrame:
        star:str = None
        if main_star:
            star = desig_sm
        else:
            star = None
        s:pd.Series = pd.Series(data=[material, star, mw, density, conc_assay, kg_main, remark],
                                index=[defs.hedr_io_mats_mat,
                                       defs.hedr_io_mats_sm_tgt,
                                       defs.hedr_io_mats_mw,
                                       defs.hedr_io_mats_dnsty,
                                       defs.hedr_io_mats_concasy,
                                       defs.hedr_io_mats_kg_sm,
                                       defs.hedr_io_mats_remark])
        mats_df = pd.concat([mats_df, s.to_frame().T])
        mats_df.reset_index(inplace=True, drop=True)
        return mats_df
        





