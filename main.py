import pandas as pd

from flow_draw.data_input import UnitOperation as uo
from flow_draw.data_input import Charging as chg
from flow_draw import chemistry as chem

import os
print("FILE:", __file__)
print("CWD:", os.getcwd())

print("ここ通る1？")
xls_file = pd.ExcelFile('flow_draw/input.xlsx')

df_op = pd.read_excel(io='flow_draw/input.xlsx', sheet_name='Operations')
df_chem = pd.read_excel(io='flow_draw/input.xlsx', sheet_name='Chemistry')
df_sm = pd.read_excel(io='flow_draw/input.xlsx', sheet_name='SM')

print("ここ通る2？")
chem_data = chem.Chemistry(df_chem=df_chem, df_sm=df_sm)
# uoClassInit = uo.UnitOperation()
# uoClassInit.set_chemdata(chem_data=chem_data)
uo.UnitOperation.set_chemdata(chem_data=chem_data)
inst_charge = chg.Charging(1)


