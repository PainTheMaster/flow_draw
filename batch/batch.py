import math
import pandas as pd
import flow_draw.definitions as defs
import flow_draw.batch.process.process as proc

item_batch_name: str = defs.item_io_batch_batch_name
item_batch_comment: str = defs.item_io_batch_batch_remark
item_proc_name_stem: str = defs.item_io_batch_proc_name_stem
item_proc_num_uo_stem: str = defs.item_io_batch_proc_count_uo_stem
item_proc_comment_stem: str = defs.item_io_batch_proc_remark_stem
# df_col_nr_items: int = defs.col_label_io_batch_items
# df_col_nr_values: int = defs.col_label_io_batch_values
col_item = defs.hedr_io_batch_item
col_val = defs.hedr_io_batch_value


max_search_proc_df: int = 100

class Batch:
    def __init__(self):
        self.batch_name: str = None
        self.batch_comment: str = None
        self.num_procs: int = None
        self.list_proc: list[proc.Process]=[]
        

    #TODO please implement me!
    def load_process_summary(self):
        """
        Lets each process constituting the batch load the summary data from a ProcessIO object.

        Parameters
        ------------
        None

        Returns
        ------------
        None
        """
        for proc in self.list_proc:
            proc.load_uo_summary()


    def load_outline(self, df_batch_outline: pd.DataFrame):
        self.batch_name = str(df_batch_outline.at[item_batch_name, col_val])
        self.batch_comment = df_batch_outline.at[item_batch_comment, col_val]
        if pd.isna(self.batch_comment):
            self.batch_comment = None
        self.list_proc = []
        for i in range(max_search_proc_df):
            temp_item_proc_name = item_proc_name_stem.format(i+1)
            temp_item_num_uo = item_proc_num_uo_stem.format(i+1)
            temp_item_comment_uo = item_proc_comment_stem.format(i+1)
            # if df_batch_outline[hedr_item].isin([temp_item_proc_name]).any():
            # if (df_batch_outline[col_item].isin([temp_item_proc_name]).any() and
            if (temp_item_proc_name in df_batch_outline.index and
                not pd.isna(df_batch_outline.at[temp_item_proc_name, col_val])):
                proc_name = df_batch_outline.at[temp_item_proc_name, col_val]
                if (temp_item_num_uo in df_batch_outline.index and 
                    not pd.isna(df_batch_outline.at[temp_item_num_uo, col_val])):
                    num_uo = int(df_batch_outline.at[temp_item_num_uo, col_val])
                else:
                    num_uo = None 
                    """
                    It is possible that the field for the num of unit operations is not found or is brank evne though the subsequent processing is needed.
                    The program allows the user to carry on for some flexibility.
                    The fact shall be kept clear and the subsequent data process shall be aware of that and put some assumption.
                    """
                temp_comment_uo:str = None
                if (temp_item_comment_uo in df_batch_outline.index and
                    not pd.isna(df_batch_outline.at[temp_item_comment_uo, col_val])):
                    temp_comment_uo = df_batch_outline.at[temp_item_comment_uo, col_val]

                new_proc = proc.Process(batch_name=self.batch_name, process_name=proc_name, num_uo=num_uo, comment=temp_comment_uo)
                self.list_proc.append(new_proc)
            else:
                break
        self.num_procs = len(self.list_proc)
        


    def load_process_details(self):
        """
        Just trigger load_unitop_detail() of all items in the list self.list_proc.

        Parameters
        ---------
        None

        Returns
        ---------
        None
        """
        for p in self.list_proc:
            p.load_unitop_detail()