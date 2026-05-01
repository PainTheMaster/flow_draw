import pandas as pd
import flow_draw.definitions as defs
import flow_draw.project.process.process as proc

hedr_project_name: str = defs.hedr_io_proj_project_name
hedr_proC_name_stem: str = defs.hedr_io_proj_proC_name_stem
hedr_proC_num_uo_stem: str = defs.hedr_io_proj_proC_num_uo_stem
df_col_nr_items: int = defs.col_nr_io_proj_items
df_col_nr_values: int = defs.col_nr_io_proj_values

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


    def prep_process(self, df_proj_outline: pd.DataFrame):
        for i in range(self.num_procs):
            temp_item_name = hedr_proC_name_stem.format(i+1)
            temp_item_num_subitems = hedr_proC_num_uo_stem.format(i+1)
            temp_proc_name:str = str(df_proj_outline.loc[temp_item_name, df_col_nr_values])
            temp_num_uo:int = int(df_proj_outline.loc[temp_item_num_subitems, df_col_nr_values])
            new_proc = proc.Process(project_name=self.proj_name, process_name=temp_proc_name, num_uo=temp_num_uo)
            self.list_proc.append(new_proc)



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