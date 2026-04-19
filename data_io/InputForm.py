import openpyxl as xl
import pandas as pd
import flow_draw.definitions as defs
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.worksheet.datavalidation import DataValidation
from typing import List, Dict

base_file_name_input = "input_"
sheet_summary_input = "summary"
sheet_detail_input = "sataInput"

summary_col_seq = 1
summary_col_uo = 2
summary_col_editcomment = 3

header_summary_sequence = 'Sequence'
header_summary_uo = 'Unit Operation'
header_summary_edit_comment = 'Edit Comment'

header_detail_seq = 'Sequence'
header_detail_operation = 'Operation'
header_detail_edit_comment = header_summary_edit_comment
header_detail_precomment = 'Pre-comment'
header_detail_postcomment = 'post-comment'

common_header_detail = [
    header_detail_seq,
    header_detail_operation,
    header_detail_edit_comment,
    header_detail_precomment,
    header_detail_postcomment 
]

class InputForm:
    def __init__(self, process_name: str, count_unit_op: int):
        self.process_name = process_name
        self.count_unit_op = count_unit_op
        self.wb = xl.Workbook()
        self.summary_ws:Worksheet = self.wb.create_sheet(title=sheet_summary_input)
        self.detail_ws: Worksheet = self.wb.create_sheet(title=sheet_detail_input)
        self.wb.remove(worksheet=self.wb['Sheet'])
        self.file_path =base_file_name_input+process_name+'.xlsx'
        self.current_line_summary = 1
        self.current_line_detail = 1
    
    def save_summary_form(self):
        self.wb.save(filename=self.file_path)

    def get_filename(self):
        return self.file_path

    def put_summary_input_form(self, list_unit_ops: List[str]):
        options_dv: str = '"'
        for item in list_unit_ops:
            options_dv += (item+',')
        options_dv = options_dv[:-1]
        options_dv = options_dv+'"'

        dv_unitops = DataValidation(
            type='list',
            formula1=options_dv,
            allow_blank=False
        )

        self.summary_ws.add_data_validation(dv_unitops)

        #This function makes the summary input form based on the number of the unit operations in the process.
        self.current_line_summary = 1
        self.summary_ws.cell(row = self.current_line_summary, column = summary_col_seq, value=header_summary_sequence)
        self.summary_ws.cell(row = self.current_line_summary, column = summary_col_seq).border = defs.xl_border_around
        self.summary_ws.cell(row = self.current_line_summary, column = summary_col_uo, value=header_summary_uo)
        self.summary_ws.cell(row = self.current_line_summary, column = summary_col_uo).border = defs.xl_border_around
        self.summary_ws.cell(row = self.current_line_summary, column = summary_col_editcomment, value=header_summary_edit_comment)
        self.summary_ws.cell(row = self.current_line_summary, column = summary_col_editcomment).border = defs.xl_border_around
        self.current_line_summary += 1
        for i in range(self.count_unit_op):
            self.summary_ws.cell(row=self.current_line_summary, column=summary_col_seq, value=i+1)
            self.summary_ws.cell(row=self.current_line_summary, column=summary_col_seq).border = defs.xl_border_around
            self.summary_ws.cell(row = self.current_line_summary, column = summary_col_uo).border = defs.xl_border_around
            dv_unitops.add(self.summary_ws.cell(row = self.current_line_summary, column = summary_col_uo))
            self.summary_ws.cell(row = self.current_line_summary, column = summary_col_editcomment).border = defs.xl_border_around
            self.current_line_summary += 1
        

    def load_process_summary(self) -> pd.DataFrame:
        df = pd.read_excel(io = self.file_path, sheet_name=sheet_summary_input, header=0)
        return df

    
        #TODO: implement me!
    def put_detail_input_form(self, seq: int,specif_header: List[str], menu_dict: Dict[str, List[str]], sub_items: int=1):
        #This function makes the detail input form based on the number of the unit operations in the process.
        #Prepare options for drop down list(s) called data validation.
        local_menu_dict: Dict[str, DataValidation] = {}
        for key in local_menu_dict:
            options = '"'
            for item in local_menu_dict[key]:
                options += (item+',')
            options = options[:-1]
            options += '"'
            dv_unitops = DataValidation(
                type='list',
                formula1=options,
                allow_blank=True
            )
            local_menu_dict[key]=dv_unitops
            self.detail_ws.add_data_validation(dv_unitops)

        header = [None]+common_header_detail+specif_header
        for col in range(start=1, stop=len(header), step=1):
            self.detail_ws.cell(row = self.current_line_detail, column = col, value=header[col])
            self.detail_ws.cell(row = self.current_line_detail, column = col).border = defs.xl_border_around
            self.detail_ws.cell(row = self.current_line_detail, column = col).font = defs.xl_font_bold
        self.current_line_detail += 1

        for _ in range(sub_items):
            #TODO: implement the logic to put the neceesary items in the body of the table
            pass
        
        





                



        