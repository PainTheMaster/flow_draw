
from flow_draw import definitions as defs
from flow_draw import chemistry as chem
from flow_draw.flow_output import Flowsheet as fsht
from typing import List
import re


op_line_clearance = "line_clearance"
op_N2_replace = "N2_placement"
op_temp_control = "temp_control"
op_charging = "charging"
op_agitation = "agitation"
op_settling = "settling"
op_aq_discharge = "aq_discharge"
op_distillation = "distillation"
op_cip = "cip"
op_transfer = "transfer"
op_filtration = "filtration"
op_rinse = "rinse"
op_reslurry = "reslurry"
op_drying = "drying"
op_tare = "tare"
op_prod_discharge = "prod_discharge"
op_placeholder = "placeholder"


class UnitOperation:
    chem_data = None
    flow_sheet: fsht.Flowsheet = None
    def __init__(self, unit_operation: str=None, operation_seq: int=None):
        self.unit_operation = unit_operation
        self.operation_seq = operation_seq
        self.pre_comment = ''
        self.post_comment = ''


    @classmethod 
    def set_chemdata(cls, chem_data:chem.Chemistry):
        cls.chem_data = chem_data


    @classmethod 
    def set_flowsheet(cls, flow_sheet:fsht.Flowsheet):
        cls.flow_sheet = flow_sheet
    

    def put_comment(self,
                    comments: str,
                    list_col_time: List[str],
                    list_col_method: List[str],
                    list_col_content: List[str],
                    list_col_record: List[str],
                    list_col_operator: List[str],
                    list_col_witness: List[str]):
        # cmt_brkdwn = comments.split(sep='[\n;]')
        cmt_brkdwn = re.split('[\n;]', comments)
        for single_cmt in cmt_brkdwn:
            list_col_time.append(None)
            list_col_method.append(None)
            list_col_content.append(single_cmt)
            list_col_record.append(None)
            list_col_operator.append(None)
            list_col_witness.append(None)
        

    def output_unit_operation(self):
        raise NotImplementedError()
    
    def input_form_generator(self, sub_items: int):
        raise NotImplementedError()
    




        
