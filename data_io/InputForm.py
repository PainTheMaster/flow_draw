import openpyxl as xl

sheet_summary_input = "Summary"
sheet_data_input = "DataInput"

header_item_seq = 'Sequence'
header_item__operation = 'Operation'
header_item_precomment = 'Pre-comment'
header_item_postcomment = 'post-comment'
common_header = [
    header_item_seq,
    header_item__operation,
    header_item_precomment,
    header_item_postcomment 
]

class InputForm:
    def __init__(self):
        self.wb = xl.Workbook()
        self.summary_input_sheet = self.wb.create_sheet(title=sheet_summary_input)
        self.data_input_sheet = self.wb.create_sheet(title=sheet_data_input)
        self.current_line = 1