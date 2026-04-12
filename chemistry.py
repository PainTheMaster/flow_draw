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
        self.df_chem = df_chem
        self.df_sm = df_sm
        self.sm_name = df_sm[df_sm[header_key]==key_sm_name][header_value].item()
        self.sm_kg = df_sm[df_sm[header_key]==key_sm_kg][header_value].item()
        self.sm_mol = self.sm_kg * 1000 / df_chem[df_chem[header_material]==self.sm_name][header_mw].item()   

    def to_kilogram(self, material = "", equiv=-1.0, vol=-1.0) -> float:
        mw = self.df_chem[self.df_chem[header_material]==material][header_mw].item()
        density = self.df_chem[self.df_chem[header_material]==material][header__density].item()
        conc = self.df_chem[self.df_chem[header_material]==material][header_conc].item()
        weight = 0.0
        if equiv > 0.0:
            mol = self.sm_mol * equiv
            weight = mol * mw * (conc/100) / 1000
        elif vol > 0.0:
            liq_volume = self.sm_kg * vol #unit = L
            weight = liq_volume * density
        else:
            print("等量も容量重量倍率も指定しないとかおかしいだろ。ふざけんな！")
        
        return weight


