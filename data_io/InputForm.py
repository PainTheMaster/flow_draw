import openpyxl as xl
from openpyxl.worksheet.worksheet import Worksheet

base_file_name_input = "Input"
sheet_summary_input = "Summary"
sheet_detail_input = "DataInput"

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
        self.file_name =base_file_name_input+process_name+'.xlsx'
        self.wb.save(filename=self.file_name)
        self.current_line_summary = 1
        self.current_line_detail = 1
    
    def get_filename(self):
        return self.file_name

    #TODO: implement me!
    def put_summary_input_form(self):
        #This function makes the summary input form based on the number of the unit operations in the process.
        self.current_line_summary = 1
        self.summary_ws.cell(row = self.current_line_summary, column = summary_col_seq, value=header_summary_sequence)
        self.summary_ws.cell(row = self.current_line_summary, column = summary_col_uo, value=header_summary_uo)
        self.summary_ws.cell(row = self.current_line_summary, column = summary_col_editcomment, value=header_summary_edit_comment)
        self.current_line_summary += 1
        for i in range(self.count_unit_op):
            self.summary_ws.cell(row=self.current_line_summary, column=summary_col_seq, value=i+1)
            self.current_line_summary += 1
        self.wb.save(filename=self.file_name)
        

    
        #TODO: implement me!
    def put_detail_input_form(self):
        #This function makes the detail input form based on the number of the unit operations in the process.
        pass
