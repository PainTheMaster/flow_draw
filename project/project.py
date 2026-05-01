import math
import pandas as pd
import flow_draw.definitions as defs
import flow_draw.project.process.process as proc

hedr_project_name: str = defs.hedr_io_proj_project_name
hedr_proC_name_stem: str = defs.hedr_io_proj_proC_name_stem
hedr_proC_num_uo_stem: str = defs.hedr_io_proj_proC_num_uo_stem
df_col_nr_items: int = defs.col_nr_io_proj_items
df_col_nr_values: int = defs.col_nr_io_proj_values
df_max_proc_search: int = 100

class Project:
    def __init__(self):
        self.proj_name: str = None
        self.num_procs: int = None
        self.list_proc: list[proc.Process]=[]
        

    #TODO please implement me!
    def load_process_summary(self):
        """
        Lets each process constituting the project load the summary data from a ProcessIO object.

        Parameters
        ------------
        None

        Returns
        ------------
        None
        """
        for proc in self.list_proc:
            proc.load_uo_summary()


    def load_outline(self, df_proj_outline: pd.DataFrame):
        self.proj_name = str(df_proj_outline.loc[hedr_project_name, df_col_nr_values])
        self.list_proc = []
        # for i in range(self.num_procs):
        #     temp_item_name = hedr_proC_name_stem.format(i+1)
        #     temp_item_num_subitems = hedr_proC_num_uo_stem.format(i+1)
        #     temp_proc_name:str = str(df_proj_outline.loc[temp_item_name, df_col_nr_values])
        #     temp_num_uo:int = int(df_proj_outline.loc[temp_item_num_subitems, df_col_nr_values])
        #     new_proc = proc.Process(project_name=self.proj_name, process_name=temp_proc_name, num_uo=temp_num_uo)
        #     self.list_proc.append(new_proc)
        for i in range(df_max_proc_search):
            temp_item_proc_name = hedr_proC_name_stem.format(i+1)
            temp_item_num_uo = hedr_proC_num_uo_stem.format(i+1)
            # unk = df_proj_outline[df_col_nr_values]
            if df_proj_outline[df_col_nr_items].isin([temp_item_proc_name]).any():
                proc_name = df_proj_outline.loc[temp_item_proc_name, df_col_nr_values]
                if (df_proj_outline[df_col_nr_items].isin([temp_item_num_uo]).any() and
                    not math.isnan(df_proj_outline.loc[temp_item_num_uo, df_col_nr_values])):
                    num_uo = df_proj_outline.loc[temp_item_num_uo, df_col_nr_values]
                else:
                    num_uo = None 
                    """
                    When the field for the num of unit operations is not found or when it's brank. The process contineus anyway to allow some flexibility.
                    Anyway, the fact shall be clear and the subsequent data process shall be aware of that and put some assumption.
                    """
                new_proc = proc.Process(project_name=self.proj_name, process_name=proc_name, num_uo=num_uo)
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