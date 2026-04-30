import pandas as pd

from flow_draw.project.process.unit_operations import unit_operation as uo
from flow_draw.project.process.unit_operations import Charging as chg
from flow_draw.materials import materials as mats

#from flow_draw.flow_output.Flowsheet import Flowsheet as fs
from flow_draw.flow_output import Flowsheet as fs

from flow_draw.data_io import process_io as ipt



# xls_file = pd.ExcelFile('flow_draw/input.xlsx')

#df_op = pd.read_excel(io='flow_draw/input.xlsx', sheet_name='Operations')
df_chem = pd.read_excel(io='flow_draw/input.xlsx', sheet_name='Chemistry')
df_sm = pd.read_excel(io='flow_draw/input.xlsx', sheet_name='SM')

chem_data = mats.Materials(df_chem=df_chem, df_sm=df_sm)
test_sheet = fs.Flowsheet()

test_charging = chg.Charging(chem_data=chem_data, flow_sheet=test_sheet, operation_seq=1)
test_charging.test_data_creation()

test_charging.output_unit_operation()


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

test_sheet.save('test_output_20260423.xlsx')

# input_form = ipt.InputForm(process_name='test_process', num_unit_op=2)
# input_form.put_summary_input_form(list_unit_ops=uo.list_unit_ops)
# input_form.save_summary_form()

# summary_df = input_form.load_process_summary()
# print(summary_df)

# input_form.put_detail_input_form(
#     seq=2,
#     specif_header=chg.list_header_items,
#     menu_dict=chg.menu_dict
# )

# input_form.save_summary_form()

# flsheet = fs.Flowsheet()
# flsheet.put_line(time='Time')
# flsheet.put_line(method='Method')
# flsheet.put_line(content='Content')
# flsheet.put_line(record='Record')
# flsheet.put_line(operator='Operator')
# flsheet.put_line(witness='Witness, blank below')
# flsheet.put_line(witness='')
# flsheet.save('line_output_test.xlsx')


