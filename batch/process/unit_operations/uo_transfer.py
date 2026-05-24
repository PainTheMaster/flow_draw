#########################################################
# imports
#########################################################
import pandas as pd
import flow_draw.definitions as defs
import flow_draw.data_io.flowsheet as fsht
from typing import Optional
from flow_draw.batch.process.unit_operations import unit_operation as uo
from flow_draw.data_io import process_io as procio
from flow_draw.materials import materials as mats
from flow_draw.trait_def import trait_def as trdef
#from flow_draw.trait_def.trait_def import GetMats



#########################################################
# Common items: headers etc
#########################################################
hedr_precomment:str = defs.hedr_cmn_io_dtil_precmnt #Don't include this in the specific header list!!!
"""A common header item: header for unit operation precomment"""
hedr_postcomment:str = defs.hedr_cmn_io_dtil_postcmnt #Don't include this in the specific header list!!!
"""A common header item: header for unit operation postcomment"""

        #### Common option items for the detail input table #####
opt_yes:str = defs.opt_yes
"""Affirmative option for various user choice."""
opt_no: str = defs.opt_no
"""Negative option for various user coice"""

opt_time_unit_second:str = defs.tag_flow_cmn_time_unit_second
"""Tag for a common flowsheet component for an unit of time: second"""
opt_time_unit_minute:str = defs.tag_flow_cmn_time_unit_minute
"""Tag for a common flowsheet component for an unit of time: minute"""
opt_time_unit_hour:str = defs.tag_flow_cmn_time_unit_hour
"""Tag for a common flowsheet component for an unit of time: hour"""

#########################################################
# UO-specific hader items and list thereof
#########################################################
#hedr_<something> = defs.hedr_<unit operation>_<specification item>
#list_hedr = defs.list_hedr_<list of header items for the uo>
#dict_dtil_drpdwn = defs.dict_opt_<unit operation>
hedr_operation = "line set-up/transfer"
"""Header item: origin of the discarded lower phase, e.g., reaction vessel, etc."""
hedr_origin = "origin"
"""Header item: origin of the discarded lower phase, e.g., reaction vessel, etc."""
hedr_via = "via"
"""Header item : way point of the discarded lower phase, e.g., multiplexer, etc"""
hedr_destin = "destination"
"""Header item: destination of the discarded lower phase, e.g., wate liqour tank, etc"""
hedr_filter_typ = "filter type"
"""Header item: filter type; if empty, related flowsheet components are omitted"""

list_hedr = [hedr_operation,
             hedr_origin,
             hedr_via,
             hedr_destin,
             hedr_filter_typ]
"""list of  hader fields for the unit operation phase discharge"""


opt_operation_setup = "line set-up"
"""Option for the item operation: only setting up the line before transfer"""
opt_operation_transfer = "set-up and transfer"
"""Option for the item operation: set-up and transfer"""
list_opt_operation = [opt_operation_setup, opt_operation_transfer]
"""List of options for the operation"""

dict_drop_down = {hedr_operation : list_opt_operation}
"""diction onary of header items vs list of options"""

#########################################################
# UO-specific options, list, header_item: list dictionry thereof (for data input and internalsignaling)
#########################################################


"""No options"""



#########################################################
# signal -> local language dictionary and tags for it
#########################################################
lang_dict_uo_titles = defs.dict_jp_part_uo_titles


        ##### Tags (keys) for translation of common parts ####
tag_flow_cmn_rec_time:str = defs.tag_flow_cmn_rec_time
"""The key to the time-recording field for the flowsheet, a common item."""
tag_flow_cmn_rec_sign:str = defs.tag_flow_cmn_rec_sign
"""The key to the ignature field for the flowsheet, a common item."""
tag_flow_cmn_time_unit_second = opt_time_unit_second
"""Tag for a common flowsheet component for an unit of time: second"""
tag_flow_cmn_time_unit_minute = opt_time_unit_minute
"""Tag for a common flowsheet component for an unit of time: minute"""
tag_flow_cmn_time_unit_hour = opt_time_unit_hour
"""Tag for a common flowsheet component for an unit of time: hour"""
lang_dict_cmn:dict[str, str] = defs.dict_jp_part_flow_cmn
"""
Language dictionary for common parts.
    tag_flow_cmn_rec_time : part_flow_cmn_rec_time_jp,
    tag_flow_cmn_rec_sign : part_flow_cmn_rec_sign_jp
    tag_flow_cmn_time_unit_second : part_flow_cmn_time_unit_second,
    tag_flow_cmn_time_unit_minute : part_flow_cmn_time_unit_minute,
    tag_flow_cmn_time_unit_hour : part_flow_cmn_time_unit_hour
"""

tag_part_flow_uo_title_transfer = "title transfer"
"""tag for a flowsheet component: title for the unit operation, transfer"""
part_flow_uo_title_transfer_jp = "移送"
"""A flowsheet component: title for the unit operation, transfer"""

tag_part_flow_uo_title_setup = "title set-up"
"""tag for a flowsheet component: title for the unit operation, set-up only"""
part_flow_uo_title_set_up_jp = "ライン構築"
"""A flowsheet component: title for the unit operation, set-up only"""

tag_part_flow_method_instr_line_setup = "method instr line set-up"
"""tag for a flowsheet component: line set-up instruction for the method column"""
part_flow_method_instr_line_setup_jp = "ライン構築"
"""A flowsheet component: line set-up instruction for the method column"""

tag_part_flow_chk_setup = "check-box for set-up"
"""tag for a flowsheet component: check-box for line set-up"""
part_flow_chk_setup_jp = "□ライン構築確認"
"""A flowsheet component: check-box for line set-up"""

tag_part_flow_rec_typ_filter = "rec filter type"
"""tag for a flowsheet component: record field for filter type"""
part_flow_rec_typ_filter_jp = "フィルター型式:________________"
"""A flowsheet component: record field for filter type"""

tag_part_flow_rec_lot_filter = "rec filter lot"
"""tag for a flowsheet component: record field for filter lot"""
part_flow_rec_lot_filter_jp = "フィルターロット:________________"
"""A flowsheet component: record field for filter lot"""

tag_part_flow_method_instr_transf = "method instr transfer"
"""tag for a flowsheet component: trasfer instruction for the method column"""
part_flow_method_instr_transf_jp = "移送"
"""A flowsheet component: transfer instruction for the method column"""

tag_part_flow_chk_transf_compl = "check-box for transf completion"
"""tag for a flowsheet component: check-box for transfer completion"""
part_flow_chk_stransf_compl_jp = "□ 移送実施確認"
"""A flowsheet component: check-box for transfer completion"""

tag_stc_origin = "part origin vessel"
"""tag for an instruction sentence to specify an origin vessel, includes a tag {origin}"""
stc_origin_jp = "移送元:{origin}"
"""an instruction sentence to specify an origin vessel, includes a tag {origin}"""

tag_stc_via = "part transf via"
"""tag for an instruction sentence to specify a way-point, includes a tag {via}"""
stc_via_jp = "経由:{via}"
"""an instruction sentence to specify a way-point, includes a tag {via}"""

tag_stc_destin_with_filter = "stc destin with filter"
"""tag for an instruction sentence to specify a destination with a filter, includes a tag {destin}"""
stc_destin_with_filt_jp = "移送先:{destin}(フィルター設置)"
"""an instruction sentence to a destination with a filter, includes a tag {destin}"""

tag_stc_destin_no_filter = "stc destin no filter"
"""tag for an instruction sentence to specify a destination, no filter; includes a tag {destin}"""
stc_destin_no_filt_jp = "移送先:{destin}"
"""an instruction sentence to a destination, no filter; includes a tag {destin}"""

tag_stc_content_typ_filt = "stc filter typ instruction"
"""tag for an instruction sentence to specify a filter type; includes a tag {typ_filt}"""
stc_stc_content_typ_filt_jp = "フィルター型式:{typ_filt}"
"""an instruction sentence to specify a filter type; includes a tag {typ_filt}"""

dict_component_jp = {tag_part_flow_uo_title_transfer : part_flow_uo_title_transfer_jp,
                    tag_part_flow_uo_title_setup : part_flow_uo_title_set_up_jp,
                    tag_part_flow_method_instr_line_setup : part_flow_method_instr_line_setup_jp,
                    tag_part_flow_chk_setup : part_flow_chk_setup_jp,
                    tag_part_flow_rec_typ_filter : part_flow_rec_typ_filter_jp,
                    tag_part_flow_rec_lot_filter : part_flow_rec_lot_filter_jp,
                    tag_part_flow_method_instr_transf : part_flow_method_instr_transf_jp,
                    tag_part_flow_chk_transf_compl : part_flow_chk_stransf_compl_jp,
                    tag_stc_origin : stc_origin_jp,
                    tag_stc_via : stc_via_jp,
                    tag_stc_destin_with_filter : stc_destin_with_filt_jp,
                    tag_stc_destin_no_filter : stc_destin_no_filt_jp,
                    tag_stc_content_typ_filt : stc_stc_content_typ_filt_jp}

dict_component = dict_component_jp


#########################################################
# Class (uo.UnitOperation, uo_tag=defs.tag_uo_<UO_NAME>)
#------------------------------------------
# Mandatory methods
# __init__(self,
#           caller: type[trdef.UniversalTrait] =None,
#           flowsheet:fsht.Flowsheet=None,
#           operation_seq: int=None,
#           num_subitems: int = None,
#           edit_comment:str=None)
# get_detail_header(self) -> list[str]

# load_papams_from_df(self, df: pd.DataFrame)
# output_unit_operation(self)
#
#########################################################
class Transfer(uo.UnitOperation, uo_tag=defs.tag_uo_transfer):
    def __init__(self,
                 caller: type[trdef.UniversalTrait] =None,
                 flowsheet:fsht.Flowsheet=None,
                 operation_seq: int=None,
                 num_subitems: int = None,
                 edit_comment:str=None):
        super().__init__(caller=caller, flowsheet=flowsheet, operation_seq=operation_seq, num_subitems=num_subitems, edit_comment=edit_comment)
        self.operation:str = None
        self.origin:str = None
        self.via:str = None
        self.destination:str = None
        self.typ_filter:str = None
    
    def load_params_from_df(self, df: pd.DataFrame):
        """
        Loads necessary parameters from a DataFrame object.
        The header items must be in line with the definition the class Charging.
        The header items can be passed from the get_detail_header() of each UnitOperation-drived class.
        This is the overriding mehtod in the class Charging..
        """
        first_row = df.iloc[0]
        if not pd.isna(first_row[hedr_precomment]):
            self.pre_comment = first_row[hedr_precomment]
        if not pd.isna(first_row[hedr_postcomment]):
            self.post_comment = first_row[hedr_postcomment]
        if not pd.isna(first_row[hedr_operation]):
            self.operation = first_row[hedr_operation]
        else:
            raise ValueError(f"{self.__class__.__name__} Op. Seq. {self.operation_seq}: No operation, \
                             {opt_operation_setup} or {opt_operation_transfer}, selected in the flow detail form.")
        if not pd.isna(first_row[hedr_origin]):
            self.origin = first_row[hedr_origin]
        if not pd.isna(first_row[hedr_via]):
            self.via = first_row[hedr_via]
        if not pd.isna(first_row[hedr_destin]):
            self.destination = first_row[hedr_destin]
        else:
            raise ValueError(f"{self.__class__.__name__} Op. Seq. {self.operation_seq}: No destination provided in the flow detail form.")
        if not pd.isna(first_row[hedr_filter_typ]):
            self.typ_filter = first_row[hedr_filter_typ]

    def get_detail_header(self) -> list[str]:
        return list_hedr

    def get_detail_option_menu(self) -> Optional[dict[str, list[str]]]:
        return dict_drop_down
    
    def output_unit_operation(self):
        custom_uo_title:str = None
        if self.operation == opt_operation_transfer:
            custom_uo_title = dict_component[tag_part_flow_uo_title_transfer]
        elif self.operation == opt_operation_setup:
            custom_uo_title = dict_component[tag_part_flow_uo_title_setup]
        self.flowsheet.header_organizer(op_nr=self.operation_seq, title=custom_uo_title)
        if not (self.pre_comment == None or self.pre_comment == ''):
            self.flowsheet.put_body_comments(self.pre_comment)
            self.flowsheet.linefeed()        
            
        self.put_setup()

        if not (self.post_comment == None or self.post_comment == ''):
            self.flowsheet.put_body_comments(self.post_comment)
            self.flowsheet.linefeed()
    
    def put_setup(self):
        col_content:list[str] = []
        use_filter:bool = (self.typ_filter is not None)
        col_rec:list[str] = [None]

        if self.origin is not None:
            col_content.append(dict_component[tag_stc_origin].format(origin=self.origin))
        if self.via is not None:
            col_content.append(dict_component[tag_stc_via].format(via=self.via))
        if use_filter:
            col_content.append(dict_component[tag_stc_destin_with_filter].format(destin=self.destination))
            col_content.append(dict_component[tag_stc_content_typ_filt].format(typ_filt = self.typ_filter))
            col_rec.append(dict_component[tag_part_flow_rec_typ_filter])
            col_rec.append(dict_component[tag_part_flow_rec_lot_filter])
        else:
            col_content.append(dict_component[tag_stc_destin_no_filter].format(destin=self.destination))

        
        #1st line in the segment
        self.flowsheet.put_line(time=lang_dict_cmn[tag_flow_cmn_rec_time],
                                method=dict_component[tag_part_flow_method_instr_line_setup],
                                content= col_content[0],
                                record=dict_component[tag_part_flow_chk_setup],
                                operator=lang_dict_cmn[tag_flow_cmn_rec_sign],
                                witness=lang_dict_cmn[tag_flow_cmn_rec_sign])
        #2nd line in the segment
        if len(col_content) > len(col_rec):
            col_rec += [None]*(len(col_content)-len(col_rec))
        elif len(col_content) < len(col_rec):
            col_content += [None]*(len(col_rec)-len(col_content))
        
        for i in range(1,len(col_content)):
            self.flowsheet.put_line(content=col_content[i],
                                    record=col_rec[i])
        
        self.flowsheet.linefeed()
                               

    @classmethod
    def generate_test_df(cls,
                       operation:str = None,
                       origin:str = None,
                       via:str = None,
                       destination:str = None,
                       filter:str = None)->pd.DataFrame:
        hedr:list[str] = defs.list_hedr_cmn_io_dtil + list_hedr
        content: list[any] = [None]*len(hedr)
        s:pd.Series = pd.Series(data=content, index=hedr)
        df = s.to_frame().T
        df.at[df.index[0], hedr_operation]=operation
        df.at[df.index[0], hedr_origin]=origin
        df.at[df.index[0], hedr_via]=via
        df.at[df.index[0], hedr_destin]=destination
        df.at[df.index[0], hedr_filter_typ]=filter

        return df
    
