import pandas as pd
import flow_draw.definitions as defs


class ProcessIO:
    def __init__(self):
        self.outline_file_name = "campaign_outline.xlsx"
        
    
    def load_outline(self) -> pd.DataFrame:
        
        df_camp_outline = pd.read_excel(self.outline_file_name)

