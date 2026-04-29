import openpyxl as xl
from openpyxl.styles.borders import Border, Side
from openpyxl.styles import Alignment
from openpyxl.styles import Font

############################
#        Parameters        #
############################
#Chem
chem_default_num_rows = 100


###############################################
#ITEMS FOR INTERNAL DATA PROCESSING: TAGS ETC #
###############################################

#general
tag_yes: str = 'Yes'
tag_no: str = 'No'
list_yesno: list[str]=[tag_no, tag_yes]

#unit_operations
op_line_clearance: str = "line_clearance"
"""Tag for an unit operation line clearance"""

op_N2_replace: str = "N2_placement"
"""Tag for an unit operation N2 replacement"""

op_temp_control: str = "temp_control"
"""Tag for an unit operation for temperature control"""

op_charging: str = "charging"
"""Tag for an unit operation charging/dosing"""

op_agitation: str = "agitation"
"""Tag for an unit operation agitation/mixing"""

op_settling: str = "settling"
"""Tag for an unit operation settling"""

op_aq_discharge: str = "aq_discharge"
"""Tag for an unit operation discharging aqueous phase"""

op_distillation: str = "distillation"
"""Tag for an unit operation dietillation"""

op_cip: str = "cip"
"""Tag for an unit operation cleaning in place"""

op_transfer: str = "transfer"
"""Tag for an unit operation liquid transfer"""

op_filtration: str = "filtration"
"""Tag for an unit operation filtration of (normally) recrystallizaion slurry"""

op_rinse: str = "rinse"
"""Tag for an unit operation rinsing filter cake"""

op_reslurry: str = "reslurry"
"""Tag for an unit operation reslurry washing of obtained crystal"""

op_drying: str = "drying"
"""Tag for an unit operation drying wet filter cake"""

op_tare: str = "tare"
"""Tag for an unit operation taring packaging material before discharge"""

op_prod_discharge: str = "prod_discharge"
"""Tag for an unit operation discharging finished product"""

op_placeholder: str = "placeholder"
"""Tag for a placeholder for an undefined unit operation..."""



################################################################
#PARTS FOR PROCESS DATA IO: HEADER ITEMS, DROP-DOWN OPTIONS ETC#
################################################################

####PROCESS_IO####
inputfile_base_name = "_process_input"
"""Base name for process input Excel file"""

suffix_summary_input_ws = "_summary"
"""suffix for summary input worksheet (tab)"""

suffix_detail_input_ws = "_detail"
"""suffix for detail input worksheet (tab)"""

header_summary_sequence = 'Sequence'
header_summary_uo = 'Unit Operation'
header_summary_num_subitems = 'Number of Subitems'
header_summary_edit_comment = 'Edit Comment'

summary_col_seq = 1
summary_col_uo = 2
summary_col_num_subitems = 3
summary_col_editcomment = 4

header_detail_seq = header_summary_sequence
header_detail_uo = header_summary_uo
header_detail_edit_comment = header_summary_edit_comment
header_detail_precomment = 'Pre-comment'
header_detail_postcomment = 'Post-comment'

common_header_detail = [
    header_detail_seq,
    header_detail_uo,
    header_detail_edit_comment,
    header_detail_precomment,
    header_detail_postcomment 
]

no_comment_instr = '(No comment here)'


####CHEMISTRY####
mats_suffix_ws:str = "_materials"
"""Suffix for raw material information input worksheet"""

mats_header_material:str = "Material"
"""header item for the column for raw material names"""
mats_col_material:int = 1
"""Column number for material names"""

mats_header_main = "Main(*)"
"""Header item for the column to identify the core raw materials"""
mats_col_main:int = 2
"""Column number for the main material star (*)"""

mats_header_MW:str = "MW (g/mol)"
"""Header item for the column for molecular weight"""
chem_col_MW : int= 3
"""Column number for molecular weights"""

mats_header_density:str = "Density (g/mL)"
"""The header for the density/specific gravity of the raw material"""
mats_col_density: int = 4
"""Comlumn number for density"""

mats_header_conc_assay:str = "Conc/Assay(%)"
"""The header for the concentration or assay of the raw material"""
mats_col_conc_assay: int = 5
"""Column number for concentration or assay"""

mats_header_weight_main:str = "Weight Main (kg)"
"""Header item for the weight of core building block weight (kg)"""
mats_col_weight_main:int = 6
"""Column number for weight of the core building block"""

mats_header_remark:str = "Remark"
"""The header for optional remarks"""
mats_col_remark: int = 7
"""Column number for comment"""

mats_list_header: list[str] = [mats_header_material,
                               mats_header_main,
                               mats_header_MW,
                               mats_header_density,
                               mats_header_conc_assay,
                               mats_header_weight_main,
                               mats_header_remark]

mats_component_option_star:str = "*"
"""Star (*) marker to indicate the core raw material"""


####CHARGING####
tag_metrics_equiv = "equiv"
tag_metrics_vol = "v/w"
list_metrics_unit = [tag_metrics_equiv, tag_metrics_vol]
"""For process.unit_operations.charging.Charging. This is for drop-down list in the detail input form."""


################################################################
#                      PARTS FLOW SHEETS                       #
################################################################

#####COMMON####
part_time = '___:___' 
"""Common flowsheet component to record a point of time some action is taken."""
part_signature = '   /  /  _____'
"""Common flowsheet component for a signature"""



####CHARGING####
part_method_charging_ini = '仕込み開始'
"""Flowseet component for class Charging. An action item of commencement of charging/dosing"""

part_method_charging_end = '仕込み終了'
"""Flowseet component for class Charging. An action item of end of charging/dosing"""

part_record_input = '仕込み量__________kg'
"""Flowseet component for class Charging. A recording element for dispensed amount"""

part_record_lot = 'ロット番号__________'
"""Flowseet component for class Charging. A recording element for the lot number of a material"""

part_record_flex ='溶媒用フレキID__________'
"""Flowseet component for class Charging. A recording element for the ID of flexible tube for solvents"""

part_record_temp_ini = '開始時内温_______℃'
"""Flowseet component for class Charging. A recording element for initial temperature of a certain action"""

part_record_temp_max = '仕込み時最高内温_______℃'
"""Flowseet component for class Charging. A recording element for the maximum temperature"""

part_record_temp_min = '仕込み時最低内温_______℃'
"""Flowseet component for class Charging. A recording element for the minimum"""

part_record_temp_end = '終了時内温_______℃'
"""Flowseet component for class Charging. A recording element for the terminal temperature"""

part_check_charged ='□ 仕込み実施'
"""Flowseet component for class Charging. A check box for complete charging/dosing"""



#OpenPyXL styles
xl_line_thin = Side(style="thin")

xl_border_left = Border(left=xl_line_thin)
xl_border_right = Border(right=xl_line_thin)
xl_border_top = Border(top=xl_line_thin)
xl_border_bottom = Border(bottom=xl_line_thin)
xl_border_around = Border(left=xl_line_thin, right=xl_line_thin, top=xl_line_thin, bottom=xl_line_thin)

xl_alignment_center = Alignment(horizontal='center')
xl_alignment_left = Alignment(horizontal='left')

xl_font_bold = Font(bold=True)




