#########################################################
# imports
#########################################################
import pandas as pd
import flow_draw.definitions as defs
from typing import Optional
from flow_draw.batch.process.unit_operations import unit_operation as uo
from flow_draw.data_io import process_io as procio
from flow_draw.materials import materials as mats
from flow_draw.data_io.flowsheet import Flowsheet as fsht
from flow_draw.trait_def import trait_def as trdef
from flow_draw.data_io.json_io import Objason, Array, Primitive



#########################################################
# Common items: headers etc
#########################################################
header_precomment = defs.hedr_cmn_io_dtil_precmnt #Don't include this in the specific header list!!!
header_postcomment = defs.hedr_cmn_io_dtil_postcmnt #Don't include this in the specific header list!!!


#########################################################
# UO-specific hader items and list thereof
#########################################################
hedr_lines = "Lines"
list_hedr = [hedr_lines]


#########################################################
# UO-specific options, list, header_item: list dictionry thereof (for data input and internalsignaling)
#########################################################

"No parts for the unit operation 'placeholder'"




#########################################################
# signal -> local language dictionary and tags for it
#########################################################

lang_dict_uo_titles = defs.dict_jp_part_uo_titles
lang_dict_cmn = defs.dict_jp_part_flow_cmn



#########################################################
# Class (uo.UnitOperation, uo_name=defs.tag_uo_<UO_NAME>)
#------------------------------------------
# Mandatory methods
# -__init__(self,
#           caller: type[trdef.UniversalTrait] =None,
#           flowsheet:fsht.Flowsheet=None,
#           operation_seq: int=None,
#           num_subitems: int = None,
#           edit_comment:str=None)
# -get_detail_header(self) -> list[str]
# -load_papams_from_df(self, df: pd.DataFrame)
# -output_unit_operation(self)
#
#########################################################

class Placeholder(uo.UnitOperation, uo_tag=defs.tag_uo_placeholder):

    def __init__(self,
                 caller:type[trdef.UniversalTrait]=None,
                 flowsheet:fsht.Flowsheet = None,
                 operation_seq:int = None,
                 num_subitems:int = None,
                 edit_comment:str = None):
        super().__init__(caller=caller, flowsheet=flowsheet, operation_seq=operation_seq, num_subitems=1, edit_comment=edit_comment)
        self.num_lines: int = 0

    def get_detail_header(self) -> list[str]:
        return list_hedr

    
    def get_detail_option_menu(self) -> Optional[dict[str, list[str]]]:
        return None

    def get_json_schema(caller: trdef.UniversalTrait=None)->Objason:
        seq_uo = Primitive(prim_type="integer",
                            key=defs.hedr_cmn_io_dtil_seq,
                            description="Sequence number (1, 2, 3...) in a series of unit operations in the process",
                            required=True)
        name_uo = Primitive(prim_type="string",
                            key=defs.hedr_cmn_io_dtil_uo,
                            description="Unit operation name in the process detail worksheet",
                            const=Placeholder.uo_tag,
                            required=True)
        edtcmnt = Primitive(prim_type="string",
                            key=defs.hedr_cmn_io_dtil_edt_cmnt,
                            description="An optional editorial comment. This comment will not be printed on the flowsheet.",
                            required=True,
                            nullable=True)
        precmnt = Primitive(prim_type="string",
                            key=defs.hedr_cmn_io_dtil_precmnt,
                            description=f"If {Placeholder.uo_tag} is selected, please be sure to make a brief commnt on the the step, such as intended activity or anticipated outcome.",
                            required=True,
                            nullable=False)
        postcmnt = Primitive(prim_type="string",
                            key=defs.hedr_cmn_io_dtil_postcmnt,
                            description="An optional short instructional comment placed at the end of the instruction block for the unit operation in the process workflow",
                            required=True,
                            nullable=True)
        uo_schema = Objason(key = Placeholder.uo_tag,
                            props = [seq_uo, name_uo, edtcmnt, precmnt, postcmnt],
                            description = "A placeholder unit operation for a process workflow. This unit operation is used to indicate that a step in the process is not yet defined or is intentionally left blank.")
        return uo_schema

    def load_params_from_df(self, df: pd.DataFrame):
        """
        Loads necessary parameters from the DataFrame object.
        The header items must be in line with the definition the module "definitions".
        The header items can be passed from get_detail_header() of each UnitOperation-derived class.
        This is the overriding mehtod in the class Placeholder.
        """
        first_row = df.iloc[0]
        if not pd.isna(first_row[header_precomment]):
            self.pre_comment = first_row[header_precomment]
        if not pd.isna(first_row[header_postcomment]):
            self.post_comment = first_row[header_postcomment]
        for _, subitem in df.iterrows():
            self.num_lines+=subitem[hedr_lines]

    #TODO: please test me!
    def load_from_json_dict(self, json_dict: dict[str:any]=None):
        super().load_from_json_dict(json_dict)
        self.num_lines = 1


    def output_unit_operation(self):
        self.flowsheet.header_organizer(op_nr=self.operation_seq, title=lang_dict_uo_titles[self.uo_tag])
        if not (self.pre_comment == None or self.pre_comment == ''):
            self.flowsheet.put_body_comments(self.pre_comment)
            self.flowsheet.linefeed()

        for _ in range(self.num_lines-1):
            self.flowsheet.linefeed()

        if not (self.post_comment == None or self.post_comment == ''):
            self.flowsheet.put_body_comments(self.post_comment)
            self.flowsheet.linefeed()
        
        
        

        


