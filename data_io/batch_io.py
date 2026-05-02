import pandas as pd
import flow_draw.definitions as defs

outline_file_name:str = defs.src_io_batch_input_file_name
outline_ws_name:str = defs.src_io_batch_outline_ws
col_label_items:str = defs.col_label_io_batch_items
col_label_values:str = defs.col_label_io_batch_values

hedr_row:int = defs.row_hedr_io_batch_ouln_tab
item_col:int = defs.col_item_io_batch_ouln_tab
item_batch_name:str = defs.item_io_batch_batch_name
item_batch_remark:str = defs.item_io_batch_batch_remark
item_proc_name_stem:str = defs.item_io_batch_proc_name_stem
item_proc_count_stem:str = defs.item_io_batch_proc_count_uo_stem
item_proc_remark_stem:str = defs.item_io_batch_proc_remark_stem


class BatchIO:
    def __init__(self):
        self.outline_file_name = outline_file_name
        self.outline_ws_name = outline_ws_name 
    
    def load_outline(self) -> pd.DataFrame:
        """
        Read from the input file and transform it into a DataFrame. The header item is 
        """
        col_labels: list[int] = [col_label_items, col_label_values]
        df_batch = pd.read_excel(io=self.outline_file_name, sheet_name=self.outline_ws_name, header=hedr_row, index_col=item_col)
        return df_batch
        
    def generate_form(self):
        pass

