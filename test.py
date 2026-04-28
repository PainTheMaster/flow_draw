import pandas as pd

import flow_draw.chemistry.chemistry as chem

xls_file = pd.ExcelFile('./input.xlsx')
xls_sheets = xls_file.sheet_names
print(xls_sheets)

print('--------------------------------------------')
df_op = pd.read_excel(io='./input.xlsx', sheet_name='Operations')
df_chem = pd.read_excel(io='./input.xlsx', sheet_name='Chemistry')
df_sm = pd.read_excel(io='./input.xlsx', sheet_name='SM')

print(df_op)
print('--------------------------------------------')
print(df_chem)
print('--------------------------------------------')
print(df_sm)
print('--------------------------------------------')
chem_data = chem.Chemistry(df_chem=df_chem, df_sm=df_sm)
h2okg = chem_data.to_kilogram(material="H2O", vol_per_weight=1.0)
print("H2O kg: "+str(h2okg))
