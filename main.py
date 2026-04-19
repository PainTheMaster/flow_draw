import pandas as pd

from flow_draw.process import UnitOperation as uo
from flow_draw.process import Charging as chg
from flow_draw import chemistry as chem

#from flow_draw.flow_output.Flowsheet import Flowsheet as fs
from flow_draw.flow_output import Flowsheet as fs

from flow_draw.data_io import InputForm as ipt


# xls_file = pd.ExcelFile('flow_draw/input.xlsx')

# df_op = pd.read_excel(io='flow_draw/input.xlsx', sheet_name='Operations')
# df_chem = pd.read_excel(io='flow_draw/chemistry.xlsx', sheet_name='Chemistry')
# df_sm = pd.read_excel(io='flow_draw/chemistry.xlsx', sheet_name='SM')

# chem_data = chem.Chemistry(df_chem=df_chem, df_sm=df_sm)
# uo.UnitOperation.set_chemdata(chem_data=chem_data)
# test_charging = chg.Charging(1)
# test_charging.test_data_creation()


# test_sheet = fs.Flowsheet()
# uo.UnitOperation.set_flowsheet(test_sheet)
# test_charging.output_unit_operation()
# test_sheet.header_organizer(op_nr=1, title="test operation")

# list_col_time=['time1', 'time2']
# list_col_method=['method1', None, 'method2']
# list_col_content=['content1', 'content2', 'content3', 'content4']
# list_col_record=[None,'Record________']
# list_col_operator=[None, "OP__________"]
# list_col_witness=[None, "Witness__________"]
# test_sheet.body_organizer(list_col_time=list_col_time,
#                           list_col_method=list_col_method,
#                           list_col_content=list_col_content,
#                           list_col_record=list_col_record,
#                           list_col_operator=list_col_operator,
#                           list_col_witness=list_col_witness)

# test_sheet.body_organizer(list_col_time=list_col_time,
#                           list_col_method=list_col_method,
#                           list_col_content=list_col_content,
#                           list_col_record=list_col_record,
#                           list_col_operator=list_col_operator,
#                           list_col_witness=list_col_witness)

# test_sheet.test_save()

input_form = ipt.InputForm(process_name='test_process', count_unit_op=5)
input_form.put_summary_input_form(list_unit_ops=uo.list_unit_ops)
input_form.save_summary_form()

# summary_df = input_form.load_summary()
# print(summary_df)
