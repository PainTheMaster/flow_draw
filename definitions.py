import openpyxl as xl
from openpyxl.styles.borders import Border, Side
from openpyxl.styles import Alignment
from openpyxl.styles import Font

############################
#        Parameters        #
############################
#Batch IO
dflt_io_batch_num_procs = 100

#MATERIALS
dflt_mats_num_rows = 100



###############################################
#ITEMS FOR INTERNAL DATA PROCESSING: TAGS ETC #
###############################################

#general
tag_yes: str = 'Yes'
tag_no: str = 'No'
list_yesno: list[str]=[tag_no, tag_yes]

#unit_operations
tag_uo_line_clearance: str = "line_clearance"
"""Tag for an unit operation line clearance"""
part_uo_title_clearance_jp = "ラインクリアランス"
"""JP expression of line clearance"""

tag_uo_N2replace: str = "N2_placement"
"""Tag for an unit operation N2 replacement"""
part_uo_title_N2replace_jp = "窒素置換"
"""JP expression of N2 replacement"""

tag_uo_temp_ctrl: str = "temp_control"
"""Tag for an unit operation for temperature control"""
part_uo_title_temp_ctrl_jp = "温調"
"""JP expression of temperature control"""

tag_uo_charging: str = "charging"
"""Tag for an unit operation charging/dosing"""
part_uo_title_charging_jp = "仕込み"
"""JP expression of charging/dosing"""

tag_uo_agitation: str = "agitation"
"""Tag for an unit operation agitation/mixing"""
part_uo_title_agitation_jp = "攪拌"
"""JP expression of agitation"""

tag_uo_settling: str = "settling"
"""Tag for an unit operation settling"""
part_uo_title_settling_jp = "静置"
"""JP expression of settling"""

tag_uo_aq_discard: str = "aq_discard"
"""Tag for an unit operation discarding aqueous phase"""
part_uo_title_aq_discard_jp = "水層排出"
"""JP expression of discarding aqueous phase"""

tag_uo_evap: str = "evaporation"
"""Tag for an unit operation dietillation"""
part_uo_title_evap_jp = "濃縮" 
"""JP expression of """

tag_uo_cip: str = "cip"
"""Tag for in-process cleaning in place"""
part_uo_title_cip_jp = "工程内洗浄"
"""JP expression of in-process cleaning in place"""

tag_uo_transfer: str = "transfer"
"""Tag for an unit operation liquid transfer"""
part_uo_title_transfer_jp = "移送"
"""JP expression of liquid transfer"""

tag_uo_filt: str = "filtration"
"""Tag for an unit operation filtration of (normally) recrystallizaion slurry"""
part_uo_title_filt_jp = "ろ過"
"""JP expression of filtration"""

tag_uo_cake_rinse: str = "rinse"
"""Tag for an unit operation rinsing filter cake"""
part_uo_title_cake_rinse_jp = "湿性末リンス"
"""JP expression of rinsing filter cake rinsing"""

tag_uo_reslurry: str = "reslurry"
"""Tag for an unit operation reslurry washing of obtained crystals (wet cake)"""
part_uo_title_reslurry_jp = "結晶洗浄"
"""JP expression of reslurry wash of the obtained crystals (wet cake)"""

tag_uo_drying: str = "drying"
"""Tag for an unit operation drying wet filter cake"""
part_uo_title_drying_jp = "乾燥"
"""JP expression of product drying"""

tag_uo_tare_pkg: str = "tare"
"""Tag for an unit operation taring packaging material before discharge"""
part_uo_title_tare_pkg_jp = "風袋秤量"
"""JP expression of taring packaging material before ischarge"""

tag_uo_prod_disch: str = "prod_discharge"
"""Tag for an unit operation discharging finished product"""
part_uo_title_prod_disch_jp = "取出し"
"""JP expression of product discharge"""

tag_uo_prod_weigh: str = "prod_weighing"
"""Tag for an unit operation discharging finished product"""
part_uo_title_prod_weigh_jp = "秤量"
"""JP expression of product discharge"""

tag_uo_placeholder: str = "placeholder"
"""Tag for a placeholder for an undefined unit operation..."""
part_uo_title_placeholder = "<Op. place holder>"
"""JP expression of place holder"""

dict_jp_part_uo_titles = {tag_uo_line_clearance : part_uo_title_clearance_jp,
                          tag_uo_N2replace : part_uo_title_N2replace_jp,
                          tag_uo_temp_ctrl : part_uo_title_temp_ctrl_jp,
                          tag_uo_charging : part_uo_title_charging_jp,
                          tag_uo_agitation : part_uo_title_agitation_jp,
                          tag_uo_settling : part_uo_title_settling_jp,
                          tag_uo_aq_discard : part_uo_title_aq_discard_jp,
                          tag_uo_evap : part_uo_title_evap_jp,
                          tag_uo_cip : part_uo_title_cip_jp,
                          tag_uo_transfer : part_uo_title_transfer_jp,
                          tag_uo_filt : part_uo_title_filt_jp,
                          tag_uo_cake_rinse : part_uo_title_cake_rinse_jp,
                          tag_uo_reslurry : part_uo_title_reslurry_jp,
                          tag_uo_drying : part_uo_title_drying_jp,
                          tag_uo_tare_pkg : part_uo_title_tare_pkg_jp,
                          tag_uo_prod_disch : part_uo_title_prod_disch_jp,
                          tag_uo_prod_weigh : part_uo_title_prod_weigh_jp,
                          tag_uo_placeholder : part_uo_title_placeholder}


################################################################
#               PARTS FOR BATCH  OUTLINE WORKSHEET             #
################################################################

#>>>>>>>>>>>>>>>>>> file and sheet name <<<<<<<<<<<<<<<<<<<<#
src_io_batch_input_file_name:str = "batch_outline.xlsx"
src_io_batch_outline_ws:str = "batch outline"
"""Worksheet name for the batch outline"""


#>>>>>>>>>>>>>>>>>> header items for batch and some process summary <<<<<<<<<<<<<<<<<<#
hedr_io_batch_item:str ='Item'
"""Header for the item column in the batch outline table"""
hedr_io_batch_value:str='Value'
"""Header for the value column in the batch outline table"""
item_io_batch_batch_name:str = 'Batch Name'
"""Item for the batch name"""
item_io_batch_batch_remark:str = 'Remark for batch'
"""Item for the batch comment"""
item_io_batch_proc_name_stem:str = 'Name, Process-{}'
"""Item for the name of each process. The numbers 1, 2, 3... follow for each step."""
item_io_batch_proc_count_uo_stem:str = 'Count Subitems, Process-{}'
"""Item stem for the count of each process sub-items. The numbers 1, 2, 3 follow for each step"""
item_io_batch_proc_remark_stem:str = 'Remark, Process-{}' 
"""Ietm stem for the comment of each process. The numbers 1, 2, 3 follow for each step"""


#>>>>>>>>>>>>>>>>>> table schema of the process outline worksheet<<<<<<<<<<<<<<<<<<#
row_io_batch_hedr_ouln_tab:int = 0
"""Column number for the items in the table"""
col_io_batch_item_ouln_tab:int = 0
"""Column number for the items in the table"""
col_io_batch_value_ouln_tab:int = 1
"""Column number for the items in the table"""

################################################################
#PARTS FOR PROCESS DATA IO: HEADER ITEMS, DROP-DOWN OPTIONS ETC#
################################################################

        #>>>>>>>>>>>>>> file name, sheet name <<<<<<<<<<<<<<<<<<#

src_io_filebasename = "_process_input"
"""Base name for process input Excel file"""
src_io_sfx_sumry_ws = "_summary"
"""suffix for summary input worksheet (tab)"""
src_io_sfx_mats_ws:str = "_materials"
"""Suffix for raw material information input worksheet"""
src_io_sfx_detail_ws = "_detail"
"""suffix for detail input worksheet (tab)"""



        #>>>>>>>>>>> header items for summary worksheet <<<<<<<<<<<<<<#

hedr_io_sumry_seq = 'Seq Nr'
"""Header item for sequence number in the process summary worksheet"""
hedr_io_summary_uo = 'Unit Operation'
"""Header item for unit operations in the process summary worksheet"""
hedr_io_sumry_num_subitms = 'Number of Subitems'
"""Header item for number of subitems for each unit operation in the process summary worksheet"""
hedr_io_sumry_edt_cmnt = 'Edit Comment'
"""Header item for edit comment in the process summary worksheet"""

col_nr_io_sumry_seq = 1
"""Column number designator of sequence numbers in the summary worksheet"""
col_nr_io_sumry_uo = 2
"""Column number designator of unit operations in the summary worksheet"""
col_nr_io_sumry_num_subitms = 3
"""Column number designator of number of subitems for each unit operation in the summary worksheet"""
col_nr_io_sumry_edt_cmnt = 4
"""Column number designator of edit comment in the summary worksheet"""



        #>>>>>>>>>>>> header items for material worksheets <<<<<<<<<<<<#

hedr_io_mats_mat:str = "Material"
"""header item for the column for raw material names"""
hedr_io_mats_main = "Main(*)"
"""Header item for the column to identify the core raw materials"""
hedr_io_mats_mw:str = "MW (g/mol)"
"""Header item for the column for molecular weight"""
hedr_io_mats_dnsty:str = "Density (g/mL)"
"""The header for the density/specific gravity of the raw material"""
hedr_io_mats_concasy:str = "Conc/Assay(%)"
"""The header for the concentration or assay of the raw material"""
hedr_io_mats_kgmain:str = "Weight Main (kg)"
"""Header item for the weight of core building block weight (kg)"""
hedr_io_mats_remark:str = "Remark"
"""The header for optional remarks"""

col_nr_io_mats_mat:int = 1
"""Column number for material names"""
col_nr_io_mats_main:int = 2
"""Column number for the main material star (*)"""
col_nr_io_mats_mw : int= 3
"""Column number for molecular weights"""
col_nr_io_mats_dnsty: int = 4
"""Comlumn number for density"""
col_nr_io_mats_concasy: int = 5
"""Column number for concentration or assay"""
col_nr_io_mats_kgmain:int = 6
"""Column number for weight of the core building block"""
col_nr_io_mats_remark: int = 7
"""Column number for comment"""

list_hedr_mats_io: list[str] = [hedr_io_mats_mat,
                               hedr_io_mats_main,
                               hedr_io_mats_mw,
                               hedr_io_mats_dnsty,
                               hedr_io_mats_concasy,
                               hedr_io_mats_kgmain,
                               hedr_io_mats_remark]

itm_io_mats_desig_star:str = "*"
"""Star (*) marker to indicate the core raw material"""



            ##### header items for detail worksheet######

hedr_cmn_io_dtil_seq = hedr_io_sumry_seq
"""Header item for <> in the process detail worksheet"""
hedr_cmn_io_dtil_uo = hedr_io_summary_uo
"""Header item for <> in the process detail worksheet"""
hedr_cmn_io_dtil_edt_cmnt = hedr_io_sumry_edt_cmnt
"""Header item for <> in the process detail worksheet"""
hedr_cmn_io_dtil_precmnt = 'Pre-comment'
"""Header item for <> in the process detail worksheet"""
hedr_cmn_io_dtil_postcmnt = 'Post-comment'
"""Header item for <> in the process detail worksheet"""

list_hedr_cmn_io_dtil = [
    hedr_cmn_io_dtil_seq,
    hedr_cmn_io_dtil_uo,
    hedr_cmn_io_dtil_edt_cmnt,
    hedr_cmn_io_dtil_precmnt,
    hedr_cmn_io_dtil_postcmnt 
]

itm_cmn_io_nocmnt_instr = '(No comment here)'



######################################################
#

                        ####CHARGING HEADER ITEMS####

hedr_uo_chgng_mat = 'Material Name'
hedr_uo_chgng_mtrcs_val = 'Metrics Value'
hedr_uo_chgng_mtrcs_unit = 'Metrics Unit'
hedr_uo_chgng_errperm = 'Permissible Error (%)'
hedr_uo_chgng_method = 'Charging Method'
hedr_uo_chgng_timctrl = 'Time Control'
hedr_uo_chgng_timmin = 'Minimum Time (min)'
hedr_uo_chgng_timmax = 'Maximum Time (min)'
hedr_uo_chgng_tempctrl = 'Temp Control'
hedr_uo_chgng_tempmin = 'Minimum Temp (deg-C)'
hedr_uo_chgng_tempmax = 'Maximum Temp (deg-C)'

list_hedr_uo_chgng = [hedr_uo_chgng_mat,
                      hedr_uo_chgng_mtrcs_val,
                      hedr_uo_chgng_mtrcs_unit,
                      hedr_uo_chgng_errperm,
                      hedr_uo_chgng_method,
                      hedr_uo_chgng_timctrl,
                      hedr_uo_chgng_timmin,
                      hedr_uo_chgng_timmax,
                      hedr_uo_chgng_tempctrl,
                      hedr_uo_chgng_tempmin,
                      hedr_uo_chgng_tempmax]

####CHARGING OPTIONS####
opt_uo_chgng_mtrcs_eq = "equiv"
opt_uo_chgng_mtrcs_vol = "v/w"
list_opt_uo_chgng_mtrcs = [opt_uo_chgng_mtrcs_eq, opt_uo_chgng_mtrcs_vol]
"""For process.unit_operations.charging.Charging. This is for drop-down list in the detail input form."""

opt_uo_chgng_method_liq = 'liquid_port'
opt_uo_chgng_method_shower = 'shower'
opt_uo_chgng_method_prssvesl = 'press_vessel'
opt_uo_chgng_method_pwdr ='powder_port'
opt_uo_chgng_method_method_plchldr = 'placeholder'
list_opt_uo_chgng_method =[opt_uo_chgng_method_liq,
                           opt_uo_chgng_method_shower,
                           opt_uo_chgng_method_prssvesl,
                           opt_uo_chgng_method_pwdr,
                           opt_uo_chgng_method_method_plchldr]


opt_uo_chgng_timctrl_none = "No time control"
opt_uo_chgng_timctrl_min="Time control with minimum"
opt_uo_chgng_timctrl_max="Time control with maximum"
opt_uo_chgng_timctrl_min_max='Time control with minimum and maximum'
opt_uo_chgng_timctrl_plchldr = 'Placeholder'
list_opt_uo_chgng_timctrl=[opt_uo_chgng_timctrl_none,
                           opt_uo_chgng_timctrl_min,
                           opt_uo_chgng_timctrl_max,
                           opt_uo_chgng_timctrl_min_max,
                           opt_uo_chgng_timctrl_plchldr]


opt_uo_chgng_temprctrl_none = "No temp control"
opt_uo_chgng_temprctrl_min="Temp control with minimum"
opt_uo_chgng_temprctrl_max="Temp control with maximum"
opt_uo_chgng_temprctrl_min_max='Temp control with minimum and maximum'
opt_uo_chgng_temprctrl_plchldr = 'Placeholder'
list_opt_uo_chgne_temprctrl = [opt_uo_chgng_temprctrl_none,
                               opt_uo_chgng_temprctrl_min,
                               opt_uo_chgng_temprctrl_max,
                               opt_uo_chgng_temprctrl_min_max,
                               opt_uo_chgng_temprctrl_plchldr]


opt_uo_chgng_err_rng_plchldr='place holder'

################################################################
#                      PARTS FLOW SHEETS                       #
################################################################

#####COMMON####
tag_flow_cmn_rec_time = "tag_flow_cmn_time"
part_flow_cmn_rec_time_jp = '___:___' 
"""Common flowsheet component to record a point of time some action is taken."""

tag_flow_cmn_rec_sign = "tag_flow_cmn_sign"
part_flow_cmn_rec_sign_jp = '   /  /  _____'
"""Common flowsheet component for a signature"""

dict_jp_part_flow_cmn = {tag_flow_cmn_rec_time : part_flow_cmn_rec_time_jp,
                         tag_flow_cmn_rec_sign : part_flow_cmn_rec_sign_jp}

####CHARGING####
# tag_part_flow_chgng_title = "tag_chgng_title"
# part_flow_chgng_title_jp = '仕込み'
"""JP title for charging"""

tag_part_flow_chgng_instr_ini = "tag_chgng_instr_ini"
part_flow_chgng_instr_ini_jp = '仕込み開始'
"""Flowseet component for class Charging. An action item of commencement of charging/dosing"""

tag_part_flow_chgng_instr_end = "tag_chgng_instr_end"
part_flow_chgng_instr_end_jp = '仕込み終了'
"""Flowseet component for class Charging. An action item of end of charging/dosing"""

tag_part_flow_chgng_rec_input = "tag_chgng_rec_input"
part_flow_chgng_rec_input_jp = '仕込み量__________kg'
"""Flowseet component for class Charging. A recording element for dispensed amount"""

tag_part_flow_chgng_rec_lot= "tag_chgng_rec_lot"
part_flow_chgng_rec_lot_jp = 'ロット番号__________'
"""Flowseet component for class Charging. A recording element for the lot number of a material"""

tag_part_flow_chgng_rec_hose = "tag_chgng_rec_hose"
part_flow_chgng_rec_hose_jp ='溶媒用フレキID__________'
"""Flowseet component for class Charging. A recording element for the ID of flexible tube for solvents"""

tag_part_flow_chgng_rec_temprini = "tag_chgng_rec_temprini"
part_flow_chgng_rec_temprini_jp = '開始時内温_______℃'
"""Flowseet component for class Charging. A recording element for initial temperature of a certain action"""

tag_part_flow_chgng_rec_temprmax = "tag_chgng_rec_temprmax"
part_flow_chgng_temprmax_jp = '仕込み時最高内温_______℃'
"""Flowseet component for class Charging. A recording element for the maximum temperature"""

tag_part_flow_chgng_rec_temprmin = "tag_chgng_rec_temprmin"
part_flow_chgng_temprmin_jp = '仕込み時最低内温_______℃'
"""Flowseet component for class Charging. A recording element for the minimum"""

tag_part_flow_chgng_rec_temprend = "tag_chgng_rec_temprend"
part_flow_chgng_temprend_jp = '終了時内温_______℃'
"""Flowseet component for class Charging. A recording element for the terminal temperature"""

tag_part_flow_chgng_rec_cmpltd = "tag_chgng_rec_cmpltd"
part_flow_chgng_cmpltd_jp ='□ 仕込み実施'
"""Flowseet component for class Charging. A check box for complete charging/dosing"""

tag_part_flow_chgng_mthd_liq = opt_uo_chgng_method_liq
part_flow_chgng_mthd_liq = "液体投入口"
"""Flowsheet component for class Charging. Charging through liquid charging port. An ption for Liquid charging."""

tag_part_flow_chgng_mthd_shower = opt_uo_chgng_method_shower
part_flow_chgng_mthd_shower = "常設シャワー"
"""Flowsheet component for class Charging. Charging through the fixed shower. An ption for Liquid charging."""

tag_part_flow_chgng_mthd_prssvesl = opt_uo_chgng_method_prssvesl
part_flow_chgng_mthd_prssvesl = "圧送容器"
"""Flowsheet component for class Charging. Charging from a pressure vessel. An ption for Liquid charging."""

tag_part_flow_chgng_mthd_pwdr = opt_uo_chgng_method_pwdr
part_flow_chgng_mthd_pwdr = "粉体投入口"
"""Flowsheet component for class Charging. Charging through the power port. An ption for powder charging."""

tag_part_flow_chgng_mthd_plchldr = opt_uo_chgng_method_method_plchldr
part_flow_chgng_mthd_plchldr = "<Placeholder: charging method>"
"""Flowsheet component for class Charging. A place holder. An ption for Liquid charging."""

dict_jp_part_flow_chgng ={tag_part_flow_chgng_instr_ini : part_flow_chgng_instr_ini_jp,
                         tag_part_flow_chgng_instr_end : part_flow_chgng_instr_end_jp,
                         tag_part_flow_chgng_rec_input : part_flow_chgng_rec_input_jp,
                         tag_part_flow_chgng_rec_lot : part_flow_chgng_rec_lot_jp,
                         tag_part_flow_chgng_rec_hose : part_flow_chgng_rec_hose_jp,
                         tag_part_flow_chgng_rec_temprini : part_flow_chgng_rec_temprini_jp,
                         tag_part_flow_chgng_rec_temprmax : part_flow_chgng_temprmax_jp,
                         tag_part_flow_chgng_rec_temprmin : part_flow_chgng_temprmin_jp,
                         tag_part_flow_chgng_rec_temprend : part_flow_chgng_temprend_jp,
                         tag_part_flow_chgng_rec_cmpltd : part_flow_chgng_cmpltd_jp,
                         tag_part_flow_chgng_mthd_liq : part_flow_chgng_mthd_liq,
                         tag_part_flow_chgng_mthd_shower : part_flow_chgng_mthd_shower,
                         tag_part_flow_chgng_mthd_prssvesl : part_flow_chgng_mthd_prssvesl,
                         tag_part_flow_chgng_mthd_pwdr : part_flow_chgng_mthd_pwdr,
                         tag_part_flow_chgng_mthd_plchldr : part_flow_chgng_mthd_plchldr}


tag_stc_flow_chgng_qty = "tag_stc_qty"
stc_flow_chgng_qty_err_jp = '{qty}±{err} kg'

tag_stc_flow_chgng_time_min = opt_uo_chgng_timctrl_min
stc_flow_chgng_time_min_jp = '*滴下時間{min}以上'
"""Flowsheet component for class Charging. Charging instruction with minimum time"""

tag_stc_flow_chgng_time_max = opt_uo_chgng_timctrl_max
stc_flow_chgng_time_max_jp = '*滴下時間{max}以内'
"""Flowsheet component for class Charging. Charging instruction with maximum time"""

tag_stc_flow_chgng_time_min_max = opt_uo_chgng_timctrl_min_max
stc_flow_chgng_time_min_max_jp = '*滴下時間{min}～{max}以内'
"""Flowsheet component for class Charging. Charging instruction with minimum and maximum time range"""

tag_stc_flow_chgng_temp_min = opt_uo_chgng_temprctrl_min
stc_flow_chgng_temp_min = "仕込み中内温{min}℃以上"
"""Flowsheet component for class Charging. Charging instruction with lower temeperature limit"""

tag_stc_flow_chgng_temp_max = opt_uo_chgng_temprctrl_max
stc_flow_chgng_temp_max ="仕込み中内温{max}℃以下"
"""Flowsheet component for class Charging. Charging instruction with upper temeperature limit"""

tag_stc_flow_chgng_temp_min_max = opt_uo_chgng_temprctrl_min_max
stc_flow_chgng_temp_min_max = "仕込み中内温{min}～{max}℃"
"""Flowsheet component for class Charging. Charging instruction with temeperature range"""

dict_jp_stcs_flow_chgng = {tag_stc_flow_chgng_qty : stc_flow_chgng_qty_err_jp,
                          tag_stc_flow_chgng_time_min : stc_flow_chgng_time_min_jp,
                          tag_stc_flow_chgng_time_max : stc_flow_chgng_time_max_jp,
                          tag_stc_flow_chgng_time_min_max : stc_flow_chgng_time_min_max_jp,
                          tag_stc_flow_chgng_temp_min : stc_flow_chgng_temp_min,
                          tag_stc_flow_chgng_temp_max : stc_flow_chgng_temp_max,
                          tag_stc_flow_chgng_temp_min_max : stc_flow_chgng_temp_min_max}
"""Language dictionary for instruction SENTENCES with place holders 'min' and/or 'max'. Use str.format()"""



####################################################
#                 STYLE FOR OPEN PYXL              #
####################################################

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




